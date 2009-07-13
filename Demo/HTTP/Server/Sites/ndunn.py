from Actors.keywords import *
from Demo.HTTP.Server.http import WebServer, WebServerSlave
from Demo.HTTP.Server.Sites.pages import NDUNN
from Demo.HTTP.Common.statuscodes import OK

class NDunnWebServer(WebServer):
  
  def hostname(self):
    return 'www.ndunn.com'

  def createslave(self):
    return NDunnSlave()

class NDunnSlave(WebServerSlave):
  
  def get(self, source, session, page):
    # Single static page - always return static data
    source.incoming_page(OK, session, NDUNN)