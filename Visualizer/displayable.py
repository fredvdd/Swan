import Util.ids as ids
from Visualizer.svgfig import *
import threading

sep = 5
bsep = 5
ssep = 2
pad = 5
text_height = 11
text_heading = 13

def place_hoz(items, x, y):
  x_max = x
  y_max = y
  for item in items:
    (x_max, y1_max) = item.draw(x_max, y)
    y_max = max(y1_max, y_max)
  return (x_max, y_max)
  
def place_vert(items, x, y):
    x_max = x
    y_max = y
    for item in items:
      (x1_max, y_max) = item.draw(x, y_max)
      x_max = max(x1_max, x_max)
    return (x_max, y_max)
    

class VisSystem(object):
  collector = []
  continue_cond = threading.Lock()
  self.breaked = True
  
  def __init__(self):
    self.nodes = dict()

  def add_manager(self, loc):
    ip = ids.ip_from_loc(loc)
    if ip not in self.nodes:
      self.nodes[ip] = VisNode(ip)
    self.nodes[ip].add_manager(loc)
    self.draw()

  def add_host(self, loc):
    ip = ids.ip_from_loc(loc)
    if ip not in self.nodes:
      self.nodes[ip] = VisNode(ip)
    self.nodes[ip].add_host(loc)
    self.draw()

  def add_actor(self, id):
    ip = ids.ip(id)
    self.nodes[ip].add_actor(id)
    self.draw()
  
  def store_name(self, name, actor, manager):
    ip = ids.ip_from_loc(manager)
    self.nodes[ip].store_name(name, actor, manager)
    self.draw()

  def store_type(self, actor, manager):
    ip = ids.ip_from_loc(manager)
    self.nodes[ip].store_type(actor, manager)
    self.draw()
  
  def draw(self):
    VisSystem.collector = []
    nodes = list(self.nodes.values())
    (x_max, y_max) = place_vert(nodes, 5, 5)
    svg = SVG('g', *VisSystem.collector)
    self.wait()
    svg.save('test.svg')
  
  def wait(self):
    if breaked:
      self.continue_cond.acquire()
      if not breaked:
        self.step()
  
  def step(self):
    try:
      self.continue_cond.release()
    except:
      pass

  def func_break(self):
    self.breaked = True
  
  def start(self):
    self.breaked = False
    self.step()
      
class VisNode(object):
  
  num = 1
  
  @staticmethod
  def swap():
    VisNode.num = 1 - VisNode.num
    if VisNode.num:
      return "node1"
    else:
      return "node2"
  
  def __init__(self, ip):
    self.ip = ip
    self.managers = dict()
    self.hosts = dict()

  def add_manager(self, ip):
    port = str(ids.port_from_loc(ip))
    self.managers[port] = VisManager(port)
  
  def store_name(self, name, actor, manager):
    port = str(ids.port_from_loc(manager))
    self.managers[port].store_name(name, actor)
    
  def store_type(self, actor, manager):
    port = str(ids.port_from_loc(manager))
    self.managers[port].store_type(actor)

  def add_host(self, ip):
    port = str(ids.port_from_loc(ip))
    self.hosts[port] = VisHost(port)

  def add_actor(self, id):
    port = str(ids.port(id))
    host = self.hosts[port]
    host.add_actor(id)

  def draw(self, x, y):
    y_max = y + text_heading + pad
    x_start = x + pad + 45
    VisSystem.collector.append(SVG('text', 'Node ' + self.ip, **{'class':'header', 'x':x_start, 'y':y_max}))

    hosts = list(self.hosts.values())
    (x_max, y1_max) = place_hoz(hosts, x_start, y_max + pad)

    x_max += bsep
    y2_max = y + sep
    x_max = max(x + 250, x_max)
    managers = list(self.managers.values())
    (x_max, y2_max) = place_hoz(managers, x_max, y2_max)
    y_max = max(y1_max, y2_max) + pad
    x_max += pad

    x_max = max(x + 290, x_max)
    VisSystem.collector.insert(0, SVG('rect', **{'class':self.swap(), 'x':x, 'y':y, 'width':(x_max - x), 'height':(y_max - y)}))

    mid = (y + y_max)/2 - 20
    VisSystem.collector.append(SVG('image', **{'xlink:href':'comp.png', 'x':x + sep, 'y':mid, 'width':40, 'height':40}))
    return (x_max, y_max)


class VisManager(object):
  def __init__(self, port):
    self.port = port
    self.name_store = list()
    self.type_store = list()
    
  def store_name(self, name, actor):
    ref = VisActorRef("'" + name + "'", ids.loc(actor))
    self.name_store.append(ref)

  def store_type(self, actor):
    ref = VisActorRef(ids.type(actor), ids.loc(actor))
    self.type_store.append(ref)
        
  def draw(self, x, y):
    y_max = y + text_heading
    VisSystem.collector.append(SVG('text', 'Manager ' + self.port, **{'class':'header', 'x':x, 'y':y_max}))

    y_max = y_max + pad
    
    (x_max, y1_max) = self.draw_store(x, y_max, self.type_store, 'Type Store')
    (x_max, y2_max) = self.draw_store(x_max, y_max, self.name_store, 'Name Store')
    
    
    x_max = max(x_max, x + 160)
    y_max = max(y1_max, y2_max)
    return (x_max, y_max)
    
    
  def draw_store(self, x, y, store, name):
    x_max = x + sep
    y_max = y + sep
    VisSystem.collector.append(SVG('image', **{'xlink:href':'store.png', 'x':x_max, 'y':y_max, 'width':15, 'height':14}))
    y_max = y_max + text_heading
    VisSystem.collector.append(SVG('text', name, **{'class':'header', 'x':x_max + 18, 'y':y_max}))
    (x_max, y_max) = place_vert(store, x_max, y_max)
    x_max = max(x + 180, x_max)
    x_max += sep
    y_max += sep
    VisSystem.collector.append(SVG('rect', **{'class':'host', 'x':x, 'y':y, 'width':(x_max - x), 'height':(y_max - y)}))
    return (x_max, y_max)
    
class VisHost(object):
  def __init__(self, port):
    self.port = port
    self.actors = dict()
    
  def add_actor(self, id):
    to_store = ids.type(id) + '-' + str(ids.num(id))
    self.actors[to_store] = VisActor(to_store)
    
  def draw(self, x, y):
    x_max = x + sep
    y_max = y + sep
    VisSystem.collector.append(SVG('image', **{'xlink:href':'core.png', 'x':x_max, 'y':y_max, 'width':15, 'height':14}))
    y_max = y_max + text_heading
    VisSystem.collector.append(SVG('text', 'Host ' + self.port, **{'class':'header', 'x':x_max + 18, 'y':y_max}))
    actors = list(self.actors.values())
    (x_max, y_max) = place_vert(actors, x_max, y_max)
    x_max += sep
    y_max += sep
    VisSystem.collector.append(SVG('rect', **{'class':'host', 'x':x, 'y':y, 'width':(x_max - x), 'height':(y_max - y)}))
    return (x_max, y_max) 


class VisActor(object):
  text_length = 120
  
  def __init__(self, id):
    self.id = id
    
  def draw(self, x, y):
    VisSystem.collector.append(SVG('text', self.id, x = x, y = y + text_height + ssep))
    return (x + VisActor.text_length, y + text_height + ssep)
    
    
class VisActorRef(object):
  text_length = 250

  def __init__(self, lookup, actor_loc):
    self.lookup = lookup
    self.actor_loc = actor_loc

  def draw(self, x, y):
    string = self.lookup + ' @ ' + self.actor_loc
    VisSystem.collector.append(SVG('text', string, x = x, y = y + text_height + ssep))
    return (x + VisActorRef.text_length, y + text_height + ssep)



  

    
    