from Util.logger import FileLogger

file_loc = '/tmp/swandb.log'
log = FileLogger(file_loc)

from Swan.db.static import init_db_models
from Swan.db.relation import ForeignRelation
from Swan.db.query import Query, RelationSet
from Swan.db.constraints import less_than, greater_than, equals
from Swan.db.model import Model, PotentialModelInstance, ModelInstance
from Swan.db.fields import Field, IntegerField, TextField, EmailField, ForeignKey, TimeField












