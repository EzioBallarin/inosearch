# create the database for INO searcher
import sqlite3

def create_db():
	conn = sqlite3.connect('ino_locations.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE ino_locations (store_num INTEGER, state TEXT, city TEXT, address TEXT, zip INTEGER)''')
	conn.commit()
	conn.close()