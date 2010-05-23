from Actors.keywords import *
import sqlite3, inspect

class Database(MobileActor):
	
	def birth(self, connection):
		self.cursors = dict()
		self.ids = 0
		self.connection = connection
		self.cursor = connection.cursor()
	
	def execute(self, sql, *params):
		self.cursor.execute(sql, *params)
		self.connection.commit()
		rows = self.cursor.fetchall()
		result = (self.cursor.description, rows)
		return result
	
	def get_cursor(self):
		cid = self.ids
		self.ids += 1
		self.cursors[cid] = self.connection.cursor()
		return CursorReference(self, cid)
	
	def _cursor_call(self, cid, name, *args, **kwds):
		attr = getattr(self.cursors[cid], name)
		if inspect.isbuiltin(attr):
			res = attr.__call__(*args, **kwds)
			self.connection.commit()
			if isinstance(res, sqlite3.Cursor):
				cid = self.ids
				self.ids += 1
				self.cursors[cid] = res
				res = CursorReference(self, cid)
			return res
		return attr
		
class SwanCursor(sqlite3.Cursor):
	
	def _description(self):
		return self.description

	def _lastrowid(self):
		return self.lastrowid
	
	def _rowcount(self):
		return self.rowcount
	
class CursorReference(object):
	
	def __init__(self, ref, cid):
		self.__actor = ref
		self.__cursor= cid
	
	def __deepcopy__(self, memo):
		return CursorReference(self.__actor.__deepcopy__(memo),self.__cursor)
	
	def __getstate__(self):
		return (self.__actor, self.__cursor)
	
	def __setstate__(self, state):
		self.__actor, self.__cursor = state
	
	def __hash__(self):
		return self.__actor.__hash__()
	
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		return CursorReferenceCall(self.__actor, self.__cursor, name)
			
class CursorReferenceCall(object):
	
	def __init__(self, actor, cid, name):
		self.actor = actor
		self.cid = cid
		self.name = name
	
	def __call__(self, *args, **kwds):
		return self.actor._cursor_call(self.cid, self.name, *args, **kwds)
	
class SqliteDatabase(Database):
	
	def birth(self, filepath):
		connection = sqlite3.connect(filepath, detect_types=sqlite3.PARSE_COLNAMES)
		Database.birth(self, connection)
		