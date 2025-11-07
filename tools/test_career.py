import sys
import os
# ensure project root is on sys.path when running from tools/
proj_root = os.path.dirname(os.path.dirname(__file__))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from main import app

with app.test_client() as c:
    try:
        rv = c.get('/career')
        print('STATUS', rv.status_code)
        print(rv.data.decode('utf-8')[:500])
    except Exception as e:
        import traceback
        traceback.print_exc()
