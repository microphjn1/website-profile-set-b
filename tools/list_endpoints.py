from main import app

with app.app_context():
    eps = sorted(r.endpoint for r in app.url_map.iter_rules())
    for e in eps:
        print(e)
