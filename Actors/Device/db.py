from Actors.keywords import *
import sqlite3

class Database(MobileActor):
	
	def birth(self, connection):
		self.connection = connection
		self.cursor = connection.cursor()
	
	def execute(self, sql, *params):
		self.cursor.execute(sql, *params)
		self.connection.commit()
		rows = self.cursor.fetchall()
		result = (self.cursor.description, rows)
		return result
	
class SqliteDatabase(Database):
	
	def birth(self, filepath):
		connection = sqlite3.connect(filepath, detect_types=sqlite3.PARSE_COLNAMES)
		Database.birth(self, connection)
		