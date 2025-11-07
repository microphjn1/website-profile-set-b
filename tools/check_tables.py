import sqlite3
conn = sqlite3.connect('instance/students.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('tables:', tables)
for t in ['Student','students']:
    try:
        cnt = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"{t}: {cnt}")
    except Exception as e:
        print('no', t, e)
conn.close()
