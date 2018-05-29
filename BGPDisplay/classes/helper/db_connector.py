import sqlite3

class SQLiteConnector(object):
	"""docstring for SQLiteConnector"""
	def __init__(self, path_to_db="bgp.db"):
		self.connection = sqlite3.connect(path_to_db)

	def __del__(self):
		self.connection.close()
		
	def init_db(self):
		"""Creates all the tables needed"""
		pass

	def bgp_update(self, record):
		pass

	def bgp_reset(self):
		"""
		Every 2 or 8 hours we get a hard reset to get on the current state
		"""
		pass