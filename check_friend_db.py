import sqlite3
import os

DB = "friend_db.sqlite3"

if not os.path.exists(DB):
    print(f"ERROR: {DB} not found in {os.getcwd()}")
    raise SystemExit(1)

print(f"File: {DB}")
print(f"Size: {os.path.getsize(DB) / 1024:.1f} KB")
print("---")

conn = sqlite3.connect(DB)
cur = conn.cursor()
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"Total tables: {len(tables)}")
print("---")

for (name,) in tables:
    if name.startswith('sqlite_'):
        continue    
    try:
        count = cur.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        print(f"  {name}: {count} rows")
    except Exception as e:
        print(f"  {name}: ERROR - {e}")

conn.close()