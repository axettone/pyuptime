#!/usr/bin/env python
import sqlite3
import urllib
import website
import yaml

config = yaml.safe_load(open("config.yml"))

def init_db(conn):
	conn.execute('''CREATE TABLE IF NOT EXISTS websites (
		id INTEGER PRIMARY KEY AUTOINCREMENT, 
		url text NOT NULL, 
		notifyemail text NOT NULL, 
		lastcheck timestamp DEFAULT current_timestamp,
		laststatus text default 'UNCHECKED',
		created_at timestamp NOT NULL DEFAULT current_timestamp,
		updated_at timestamp NOT NULL DEFAULT current_timestamp)''')
	conn.execute('''
		CREATE TRIGGER IF NOT EXISTS tg_websites_updated_at
		AFTER UPDATE
		ON websites FOR EACH ROW
		BEGIN
			UPDATE websites SET updated_at = current_timestamp
				WHERE id = old.id;
		END
		''')
	conn.execute('''CREATE TABLE IF NOT EXISTS checks (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		website_id INTEGER,
		status text,
		created_at timestamp DEFAULT current_timestamp
		)''')
	conn.commit()

def get_websites(conn):
	ret = []
	for row in conn.execute('''SELECT * FROM websites'''):
		ret.append(website.WebSite(row[1],row[2],row[4],row[0],row[3],row[5]))
	return ret

def put_website(conn, website):
	conn.execute('''INSERT INTO websites (url,notifyemail) VALUES (?,?)''', (website.url, website.notifyemail))
	conn.commit()
def report_incident(website,status):
	global config
	print "Sending an email to %s from %s"%(website.notifyemail, config["notifications"]["n_email_from"])

def update_website(conn, website, newstatus):
	cursor = conn.execute('''SELECT laststatus FROM websites WHERE id=?''', (website.id,))
	last_status = cursor.fetchone()
	last_status=last_status[0]

	if (last_status == "OK" and newstatus != "OK"):
		print "New incident"
		report_incident(website, newstatus)
	elif (last_status != "OK" and newstatus == "OK"):
		print "Incident closed"
		report_incident(website, newstatus)
	else:
		print "Nothing special"

	conn.execute('''
		UPDATE websites
		SET laststatus = ?, lastcheck=current_timestamp
		WHERE id=?''', (newstatus, website.id))
	conn.execute('''
		INSERT INTO checks (website_id,status) VALUES (?,?)''', (website.id, newstatus))
	conn.commit()
def check_website(conn, website):
	try:
		code = urllib.urlopen(website.url).getcode()
		if code == 200:
			update_website(conn, website, "OK")
		else:
			update_website(conn, website, "ERROR")
	except:
		update_website(conn, website, "ERROR")

conn = sqlite3.connect('websites.db')
init_db(conn)
sites = get_websites(conn)
for item in sites:
	check_website(conn, item)

conn.close()