import sys, sqlite3 as sql
from Swan.db.fields import Field, IntegerField
from Swan.db.static import extract_models

def get_sql(table_definitions):
	creates = []
	for name in table_definitions:
		fields = table_definitions[name].__dict__
		create = 'CREATE TABLE %s (\n\t"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,\n' % name
		for x in fields:
			if isinstance(fields[x], Field):
				create += '\t"%s" %s,\n' % (x,fields[x].field_type())
		create = create[:-2] + "\n);\n"
		creates.append(create)
	return creates

def sync(sitepath):
	modelpath = sitepath.replace('/','.') + ("models" if sitepath.endswith("/") else ".models") 
	queries = get_sql(extract_models(modelpath))
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
