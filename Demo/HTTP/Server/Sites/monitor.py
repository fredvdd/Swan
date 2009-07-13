from Actors.keywords import *
from Demo.HTTP.Server.http import WebServer, WebServerSlave
from Demo.HTTP.Server.Sites.pages import MONITOR_TEMPLATE
from Demo.HTTP.Common.statuscodes import * 
from Actors.Common.theatre import TheatreList
from Demo.HTTP.Server.Sites.probe import Probe

class MonitorWebServer(WebServer):
  
  def hostname(self):
    return 'www.monitor.com'

  def createslave(self):
    return MonitorSlave()

class MonitorSlave(WebServerSlave):
  
  def birth(self):
    # Ties each active probe to its request
    self.probes = dict()
  
  def get(self, source, session, page):
   parts = page.split('?')
   task = parts[0]
   if task == '/':
     return self.list(source, session)
   if task == '/visit':
     return self.visit(source, session, parts[1])
   # No pages matched - return 404
   source.incoming_page(NOT_FOUND, session, MONITOR_TEMPLATE)
   
  def list(self, source, session):
   theatres = TheatreList().theatres()
   body = "<h1>List of available hosts</h1>"
   for theatre in theatres:
     body += """<div><font size="200%%">%s</font> <a href="http://www.monitor.com/visit?%s">visit</a></div>""" % (theatre.split(":")[0], theatre)
     data = sync(session.get(theatre))
     if data:
       body += """<div bgcolor="#FFF68F">%s</div>""" % data
   source.incoming_page(OK, session, MONITOR_TEMPLATE % body)
  
  def visit(self, source, session, query):
    probe = Probe(self, here(), query) 
    self.probes[probe] = (source, session)
      
  def processed(self, probe, target, data):
    print 'processed'
    (source, session) = self.probes[probe]
    del self.probes[probe]
    formatted = "<table>\n"
    for dataitem in data:
      formatted += "<tr><td><b>%s</b></td><td>%s</td></tr>\n" % dataitem
    formatted += "</table>"
    session.put(target, formatted)
    source.incoming_page(OK, session, MONITOR_TEMPLATE % ("""<h1>Visited host...</h1><p>%s</p>""" % formatted))