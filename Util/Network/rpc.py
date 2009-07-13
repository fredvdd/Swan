from Util.Network import valve, connector
from Util.meta import CallAggregator

class RPCValve(valve.Valve):

  def __init__(self, port, target, log):
    valve.Valve.__init__(self, port, log)
    self.__target = target
    
  def incoming(self, methodclass):
    try:
      method = getattr(self.__target, methodclass.method)
    except AttributeError:
      raise RPCException('Target object does not have method - ' + methodclass.method)
    if not callable(method):
      raise RPCException("Method (%s) is not callable on target" % methodclass.method)
    ret = method(*methodclass.args)
    if (ret == None):
      ret = 'NONE'
    return ret


class RPCException(Exception):
  def __init__(self, msg):
    Exception.__init__(self, msg)

class MethodCall(object):
  def __init__(self, method, args):
    self.method = method
    self.args = args

class RPCConnector(connector.Connector):
  def __init__(self, address):
    self.address = address
    connector.Connector.__init__(self, address)
    
  def connect(self):
    conn = connector.Connector(self.address)
    conn.connect()
    return RPCProxy(conn)
     
class RPCProxy(CallAggregator):
  
  def __init__(self, connector):
    self.__connector = connector
  
  def disconnect(self):
    self.__connector.disconnect()
  
  def method_called(self, method, args):
    self.__connector.send(MethodCall(method, args))
    reply = self.__connector.receive()
    if isinstance(reply, Exception):
      raise reply
    return reply
