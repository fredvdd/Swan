from Util.logger import TerminalLogger, NullLogger, FileLogger
import sys

#log = TerminalLogger()

if  sys.platform == 'symbian_s60':
  file_loc = 'E:\\python\\vis.log'
else: 
  file_loc = '/tmp/vis.log'
log = FileLogger(file_loc) 
