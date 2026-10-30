import datetime
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

name, *cmd = sys.argv[1:]
root = Path(__file__).resolve().parents[2]
path = root / 'docs/evidence/commands' / (name + '.txt')
print('$ ' + shlex.join(cmd), flush=True)
proc = subprocess.Popen(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env={**os.environ, 'NO_COLOR': '1', 'TERM': 'dumb', 'PYTHONUNBUFFERED': '1'})
with path.open('w') as out:
    out.write('Captured UTC: ' + datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n')
    out.write('$ ' + shlex.join(cmd) + '\n\n')
    for line in iter(proc.stdout.readline, b''):
        text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', line.decode('utf-8', 'replace')).replace('\r', '')
        out.write(text)
        out.flush()
        print(text, end='', flush=True)
    rc = proc.wait()
    out.write(f'\nExit code: {rc}\n')
sys.exit(rc)
