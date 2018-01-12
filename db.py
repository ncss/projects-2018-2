import sqlite3
import os

# try to connect to the database, and create a new one if it does not exist
if os.path.exists('database.db'): 
	conn = sqlite3.connect('database.db')
else:
	conn = sqlite3.connect('database.db')
	conn.executescript(open('init.sql').read()) # read from file if the database does not exist


def call_query(query, args):
	'''
	Takes a sql query and arguments to insert into said query, returning the result.
	'''
	db = conn.cursor()
	db.execute(query, args)
	results = db.fetchall()
	conn.commit()
	db.close()

	return results
	
def search_db():
	'''
	Returns the contents of the database.
	'''



