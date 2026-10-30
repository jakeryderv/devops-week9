"""Build the submission PDF only after all ten real screenshots are present.

Requires ReportLab. Run from any directory with: python3 docs/evidence/build-report.py
"""
from pathlib import Path
import html
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

folder = Path(__file__).resolve().parent
source = folder.parent / 'evidence-template.md'
output = folder.parent / 'week9-evidence.pdf'
stems = ['01-baseline','02-env','03-dependabot','04-scout','05-recommendations',
         '06-dockerfile','07-uid','08-workflow','09-security-checks','10-pull-request']
missing = [stem for stem in stems if not (folder/'screenshots'/f'{stem}.png').is_file()]
if missing:
    raise SystemExit('Cannot build submission PDF; missing screenshots: ' + ', '.join(missing))
markdown = source.read_text()
if 'Screenshot pending:' in markdown or 'not yet submission-ready' in markdown:
    raise SystemExit('Finish the Markdown evidence report before exporting.')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyEvidence',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=colors.black))
styles.add(ParagraphStyle(name='Milestone',fontName='Helvetica-Bold',fontSize=18,leading=22,spaceAfter=12,textColor=colors.black))
styles.add(ParagraphStyle(name='Question',fontName='Helvetica-Bold',fontSize=11,leading=15,spaceBefore=8,spaceAfter=6,textColor=colors.black))
styles.add(ParagraphStyle(name='SmallEvidence',fontName='Helvetica',fontSize=9,leading=12,spaceAfter=6,textColor=colors.HexColor('#455464')))
page_w, page_h = landscape(A4)
margin = 0.48*inch
width = page_w - 2*margin
story=[]

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m: '<link href="'+html.escape(m[2] if m[2].startswith('https://') else 'https://github.com/jakeryderv/devops-week9/blob/security/week9-devsecops/docs/'+m[2],quote=True)+'" color="#315f91">'+m[1]+'</link>',text)
    text=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    return text.replace('\n','<br/>')

parts=re.split(r'^## (Milestone \d+[^\n]*)\n',markdown,flags=re.M)
intro=parts[0]
story.append(Paragraph('Week 9 DevSecOps Evidence',styles['Title']))
for para in intro.split('\n\n'):
    if para.startswith('# '): continue
    if para.strip(): story.append(Paragraph(inline(para.strip()),styles['BodyEvidence']))
story.append(PageBreak())
for i in range(1,len(parts),2):
    title, body=parts[i],parts[i+1]
    number=int(re.search(r'Milestone (\d+)',title)[1])
    story.append(Paragraph(inline(title),styles['Milestone']))
    before_reflection = body.split('### ', 1)[0]
    text_height = 0
    for paragraph in before_reflection.split('\n\n'):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith('!['):
            continue
        style = styles['SmallEvidence'] if paragraph.startswith('[') else styles['BodyEvidence']
        text_height += Paragraph(inline(paragraph.removeprefix('Caption: ')), style).wrap(width, page_h)[1] + style.spaceAfter
    image=Image(str(folder/'screenshots'/f'{stems[number-1]}.png'))
    max_height = page_h - 2*margin - 60 - text_height
    ratio=min(width/image.imageWidth, max_height/image.imageHeight)
    image.drawWidth=image.imageWidth*ratio
    image.drawHeight=image.imageHeight*ratio
    image.hAlign='LEFT'
    story.append(image)
    story.append(Spacer(1,10))
    reflection_started=False
    for para in body.split('\n\n'):
        para=para.strip()
        if not para: continue
        if para.startswith('!['):
            if 'pr-files.png' in para:
                story.append(PageBreak())
                story.append(Paragraph('Milestone 10 - Files changed', styles['Milestone']))
                supporting = Image(str(folder/'screenshots'/'pr-files.png'))
                scale = min(width/supporting.imageWidth, (page_h-2*margin-80)/supporting.imageHeight)
                supporting.drawWidth = supporting.imageWidth*scale
                supporting.drawHeight = supporting.imageHeight*scale
                supporting.hAlign = 'LEFT'
                story.extend([supporting, Spacer(1,10), Paragraph('The pull request includes Dependabot, the security workflow, Dockerfile hardening, the PostgreSQL volume correction, and the supporting evidence.', styles['BodyEvidence'])])
            continue
        if para.startswith('### '):
            if number==10 and not reflection_started:
                story.append(PageBreak())
                story.append(Paragraph('Milestone 10 - Reflection',styles['Milestone']))
                reflection_started=True
            story.append(Paragraph(inline(para[4:]),styles['Question']))
        else:
            style=styles['SmallEvidence'] if para.startswith('[') else styles['BodyEvidence']
            story.append(Paragraph(inline(para.removeprefix('Caption: ')),style))
    if number<10: story.append(PageBreak())

def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(colors.HexColor('#56616e'))
    canvas.drawString(margin,18,'SDI 4213 | Week 9 | jakeryderv/devops-week9')
    canvas.drawRightString(page_w-margin,18,str(doc.page))
    canvas.restoreState()

SimpleDocTemplate(str(output),pagesize=landscape(A4),rightMargin=margin,leftMargin=margin,topMargin=margin,bottomMargin=margin,title='Week 9 DevSecOps Evidence',author='jakeryderv').build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
