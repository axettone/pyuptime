class WebSite:
	def __init__(self, url, notifyemail, laststatus="UNCHECKED", id=0, created_at=0, updated_at=0):
		self.url = url
		self.notifyemail = notifyemail
		self.id=id
		self.laststatus = laststatus
		self.created_at = created_at
		self.updated_at = updated_at