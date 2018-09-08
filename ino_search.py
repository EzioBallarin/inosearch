import os.path
import urllib2 
from bs4 import BeautifulSoup
import sqlite3
from db_create import create_db

def main():
	conn = sqlite3.connect('ino_locations.db')
	c = conn.cursor()
    
	print ("connected to ino_locations.db")

	base_url = 'http://locations.in-n-out.com/'
	next = 1 
	print("starting search...")
	while next < 334:

		# Since INO's website has a website for each store number,
		# and each store number increments by one, 
		# we can visit a new unique store page by appending the 
		# current count to the base url
		url = base_url + str(next)
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')

		address_box = soup.find('h3', attrs={'class':'street-address'})
		addr = address_box.text.strip()
		addr = addr.partition('-')
		
		#Split string into city/state
		cityState = addr[0].strip()
		state = cityState[len(cityState) - 2: len(cityState)]
		city = cityState.replace(state, '').strip()
		
		#Split string into address/zip
		addrZip = addr[2].strip()
		zip = addrZip[len(addrZip) - 5: len(addrZip)]
		street = addrZip.replace(zip, '').replace('\'', '').strip()
		street =  street[:-1]
		
		#Create tuple from all of th extracted data, then put it into our ino_locations database
		inoinfo = (next, state, city, street, zip)
		conn.execute("INSERT INTO ino_locations VALUES (?, ?, ?, ?, ?)", inoinfo)
		
		print ("added " + str(next))
		next = next + 1
		
	conn.commit()
	conn.close()

if __name__ == "__main__":
	if not os.path.isfile('./ino_locations.db'):
		print ("ino_locations.db not found, creating...")
		create_db()
	main()
