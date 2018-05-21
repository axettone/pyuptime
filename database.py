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