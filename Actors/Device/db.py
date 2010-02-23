from Actors.keywords import *
import sqlite3

class Database(MobileActor):
	
	def birth(self, connection):
		self.connection = connection
		self.cursor = connection.cursor()
	
	def execute(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()
		return self.cursor.fetchall()