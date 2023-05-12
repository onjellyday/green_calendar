import sqlite3
from sqlalchemy import select


def create()
con = sqlite3.connect('plant.db',isolation_level=None)

cur = con.sursor()

sql = f"INSERT INTO plant (Name, illuminance, humidity, temperatur) VALUES (산세베리아, 20,30,50)"

cur.execute(sql)



