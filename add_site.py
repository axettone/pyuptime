#!/usr/bin/env python
import database
import sqlite3
import sys
import website

def put_website(conn, website):
	conn.execute('''INSERT INTO websites (url,notifyemail,title) VALUES (?,?,?)''', (website.url, website.notifyemail,website.title))
	conn.commit()

if (len(sys.argv)<4):
	print "Usage %s %s %s"%(sys.argv[0], "http://www.myexample.com", "alarm@mywebagency.com" "Site Title")
	exit(-1)

conn = sqlite3.connect('websites.db')
database.init_db(conn)
put_website(conn,website.WebSite(sys.argv[1],sys.argv[2], sys.argv[3]))