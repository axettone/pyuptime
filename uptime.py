#!/usr/bin/env python
import database
import smtplib
import sqlite3
import urllib
import website
import yaml

config = yaml.safe_load(open("config.yml"))
def send_email(to, message):
	global config
	print "Trying to send email"
	server = smtplib.SMTP("%s:%s"%(config["notifications"]["n_email_smtp"],config["notifications"]["n_email_port"]))
	server.ehlo()
	if(config["notifications"]["n_email_tls"] == "yes"):
		server.starttls()
		server.ehlo()
	print "Connected to mail server %s"%(config["notifications"]["n_email_smtp"])
	server.login(config["notifications"]["n_email_user"],config["notifications"]["n_email_pass"])
	print "Login successful"
	ret = server.sendmail(config["notifications"]["n_email_from"], to, message)
	server.quit()

def get_websites(conn):
	ret = []
	for row in conn.execute('''SELECT * FROM websites'''):
		ret.append(website.WebSite(row[1],row[2],row[4],row[0],row[3],row[5]))
	return ret

def put_website(conn, website):
	conn.execute('''INSERT INTO websites (url,notifyemail) VALUES (?,?)''', (website.url, website.notifyemail))
	conn.commit()

def report_incident(website,oldstatus,status):
	global config
	print "Sending an email to %s from %s"%(website.notifyemail, config["notifications"]["n_email_from"])
	message = "Website %s passed from %s to %s"%(website.url,oldstatus,status)
	send_email(website.notifyemail, message)

def update_website(conn, website, newstatus):
	cursor = conn.execute('''SELECT laststatus FROM websites WHERE id=?''', (website.id,))
	last_status = cursor.fetchone()
	last_status=last_status[0]

	if (last_status == "OK" and newstatus != "OK"):
		print "New incident"
		report_incident(website, last_status, newstatus)
	elif (last_status != "OK" and newstatus == "OK"):
		print "Incident closed"
		report_incident(website, last_status, newstatus)
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
database.init_db(conn)
sites = get_websites(conn)
for item in sites:
	check_website(conn, item)

conn.close()