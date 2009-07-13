from Util.logger import TerminalLogger, FileLogger, NullLogger
import sys

#log = TerminalLogger()  
if sys.platform == 'symbian_s60':
  file_loc = 'E:\\python\\theatre.log'
else: 
  file_loc = '/tmp/theatre.log'
log = FileLogger(file_loc) 


#log = NullLogger()

theatre_data = dict()

def set_local_theatre(local_theatre):
  theatre_data['localint'] = local_theatre
  
def local_theatre():
  global theatre_data
  return theatre_data['localint']