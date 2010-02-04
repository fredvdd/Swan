from Util.logger import TerminalLogger, NullLogger, FileLogger
import sys
import os

#log = TerminalLogger()

if  sys.platform == 'symbian_s60':
  file_loc = 'E:\\python\\manager.log'
else: 
  file_loc = '%s/manager.log' % os.getcwd()
log = FileLogger(file_loc) 
