from Util.logger import TerminalLogger, NullLogger, FileLogger
import sys

#log = TerminalLogger()

if  sys.platform == 'symbian_s60':
  file_loc = 'E:\\python\\manager.log'
else: 
  file_loc = '/Users/fred/Swan/manager.log'
log = FileLogger(file_loc) 
