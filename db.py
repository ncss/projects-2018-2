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
    Usage: 'query' is a line (or multiple) of sql code. Substitute args as '?' into the query. 
    Args must be a tuple.
    E.g. call_query('SELECT * FROM people WHERE fname = ?',('Barry',))
    '''
    db = conn.cursor()
    db.execute(query, args)
    results = db.fetchall()
    conn.commit()
    db.close()
        
    return results 

def call_insert_users(username, password, email):
    '''
    Inserts the given data into the users table as a new value.
    '''
    db = conn.cursor()
    db.execute("""
        SELECT MAX(id)
        FROM users;
        """)
    a = db.fetchall()
    print(a)
    newid = a[0][0] + 1

    call_query("""
        INSERT INTO users(id,username,pword,fname,sname,email)
        VALUES (?, ?, ?, '', '', ?);""", (newid, username, password, email,))

    return newid




        








