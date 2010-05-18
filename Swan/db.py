import sys,sqlite3 as sql
from inspect import isclass
from Swan.handlers import DatabaseHandler
from Swan.fields import Field

def get_sql(modelpath):
	models = __import__(modelpath, globals(), locals(), [''])
	tables = [(x,models.__dict__[x]) for x in dir(models) if isclass(models.__dict__[x]) 
														 and issubclass(models.__dict__[x], DatabaseHandler)
														 and not x == 'DatabaseHandler']
	creates = []
	for (name,definition) in tables:
		fields = definition.__dict__
		create = 'CREATE TABLE %s (\n\t"id" serial NOT NULL PRIMARY KEY,\n' % name
		for x in fields:
			if isinstance(fields[x], Field):
				create += '\t"%s" %s,\n' % (x,fields[x].field_type())
		create = create[:-2] + "\n);\n"
		creates.append(create)
	return creates

def sync(sitepath):
	modelpath = sitepath.replace('/','.') + ("models" if sitepath.endswith("/") else ".models") 
	queries = get_sql(modelpath)
	databasepath = sitepath + ("database" if sitepath.endswith("/") else "/database")
	conn = sql.connect(databasepath)
	c = conn.cursor()
	for query in queries:
		print query
		c.execute(query)
	conn.commit()
	c.close()

if __name__ == '__main__':
	sitepath = sys.argv[1]
	sync(sitepath)