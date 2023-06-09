import sqlite3
import datetime
con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS calendar (
    date TEXT PRIMARY KEY,
    temperature TEXT,
    humidity TEXT,
    lux TEXT
)
''')
default_start_date = datetime.date(2023, 1, 1)
default_end_date = datetime.date(2023, 12, 31)
default_current_date = default_start_date

while default_current_date <= default_end_date:
    # 날짜와 이벤트 정보(기본값은 None)를 삽입
    cur.execute("INSERT INTO calendar (date, temperature, humidity, lux) VALUES (?, ?, ?, ?)", (default_current_date, None,None,None))
    default_current_date += datetime.timedelta(days=1)
con.commit()
con.close()
