from Actors.keywords import *
from Demo.HTTP.naming import NameServer
from Demo.HTTP.Browser.errorpages import *
from Demo.HTTP.Common.statuscodes import * 
from Actors.Common.theatre import TheatreList
from Demo.HTTP.Browser.browserwindow import BrowserWindow
from Actors.Common.events import EventBroker
from Demo.HTTP.util import parts

class Browser(MobileActor):
  
  def birth(self):
    print 'Browser Born'
    self.events = EventBroker()
    self.sessions = dict()
    self.window = BrowserWindow(self.events)
    self.window.set_size(700, 700)
    self.current_host = None
    self.events.subscribe('url_requested', self.parse_url)
  
  def parse_url(self, url):
    if url[:5] == 'meta:':
      items =  url[5:].split('?')
      if len(items) == 1:
        items.append('') 
      return self.meta(*items)
    # Split the URL into parts
    ps = parts(url)
    if not ps:
      # The URL was malformed
      self.error(MALFORMED_URL)
      return
    (host, path) = ps
    httpserver = sync(NameServer().lookup(host))
    if not httpserver:
      # Host not found, display error message
      self.error(BAD_HOST)
      return
    self.current_host = host
    httpserver.get(self, self.session_for(host), path)
    
  def meta(self, action, args):
    if action == 'migrate':
      self.listhosts()
    if action == 'goto':
      migrate_to(args)
    if action == 'home':
      self.events.publish('render', SPLASHSCREEN)
      
  def listhosts(self):
    formatted_theatres = ""
    for theatre in TheatreList().theatres():
      formatted_theatres += """<a href="meta:goto?%s">%s</a><br>""" % (theatre, theatre.split(":")[0])
      self.events.publish('render', MIGRATION_TEMPLATE % formatted_theatres)
      
  def friends(self):
    return [self.window, self.events]
    
  def session_for(self, host):
    if host in self.sessions:
      return self.sessions[host]
    return None
    
  def error(self, errorhtml):
    self.events.publish('render', errorhtml)
    
  def incoming_page(self, status,  session, page):
   self.sessions[self.current_host] = session
   if status == OK:
     self.events.publish('render', page)
   if status == NOT_FOUND:
     self.error(PAGE_NOT_FOUND)