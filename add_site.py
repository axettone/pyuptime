#!/usr/bin/env python
import sqlite3
import sys
import website

def put_website(conn, website):
	conn.execute('''INSERT INTO websites (url,notifyemail) VALUES (?,?)''', (website.url, website.notifyemail))
	conn.commit()

if (len(sys.argv)<3):
	print "Usage %s %s %s"%(sys.argv[0], "http://www.myexample.com", "alarm@mywebagency.com")
	exit(-1)
conn = sqlite3.connect('websites.db')
put_website(conn,website.WebSite(sys.argv[1],sys.argv[2]))