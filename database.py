from os import walk

class Database:
	def __init__(self, conn):
		self.conn = conn
	def migrate(self):
		f = []
		for (_,_, filenames) in walk("migrations"):
			for (fname) in filenames:
				filename = fname[:-3]
				print filename
				exec("import %s"%filename)
				mod = sys.modules[filename]
				for k in mod.__dict__:
					mod.__dict__[up]()
def init_db(conn):
	conn.execute('''CREATE TABLE IF NOT EXISTS websites (
		id INTEGER PRIMARY KEY AUTOINCREMENT, 
		title text NOT NULL,
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
		wait_ms REAL,
		created_at timestamp DEFAULT current_timestamp
		)''')
	conn.execute('''CREATE TABLE IF NOT EXISTS migrations (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		filename INTEGER,
		created_at timestamp DEFAULT current_timestamp
		)''')
	conn.commit()