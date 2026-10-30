from streamlit.testing.v1 import AppTest
import sys
sys.path.insert(0, '/app/app')
app = AppTest.from_file('/app/app/main.py', default_timeout=30).run()
assert not app.exception, app.exception
assert app.title[0].value == '🛠️ Service Request Tracker'
print('PASS: Help Desk app renders against PostgreSQL')
from db import get_engine, list_requests
engine = get_engine()
previous_ids = {r['id'] for r in list_requests(engine)}
app.text_input[0].set_value('Week 9 security verification')
app.text_area[0].set_value('Verify request creation and status updates after container setup.')
next(b for b in app.button if b.label == 'Submit Request').click().run()
assert not app.exception, app.exception
rows = list_requests(engine)
new_rows = [r for r in rows if r['id'] not in previous_ids]
assert len(new_rows) == 1
row = new_rows[0]
assert row['title'] == 'Week 9 security verification'
assert row['status'] == 'Open'
print('PASS: Request created in PostgreSQL, id=' + str(row['id']))
next(s for s in app.selectbox if s.label == 'Select request to update').set_value(row['id'])
next(s for s in app.selectbox if s.label == 'New status').set_value('Closed')
next(b for b in app.button if b.label == 'Update Status').click().run()
assert not app.exception, app.exception
assert next(r for r in list_requests(engine) if r['id'] == row['id'])['status'] == 'Closed'
print('PASS: Request status updated to Closed through the application')
