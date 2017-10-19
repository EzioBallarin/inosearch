import os
import sqlite3

conn = sqlite3.connect('ino_locations.db')
c = conn.cursor()

c.execute('SELECT * FROM ino_locations')
for r in c.fetchall():
	print r


raw_input()
conn.close()
