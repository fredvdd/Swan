def parts(url):
  """Utility function which splits the parts of a URL into
     a (host, page) pair.  Returns None if there is a error
     encountered whilst parsing"""
  protocol = url.split('http://')
  if len(protocol) != 2 or protocol[0] != '':
    return None
  url = protocol[1]
  hp = url.split('/')
  if len(hp) == 1:
    host = hp[0]
    if len(host) > 0:
      return (host, '/')
    return None
  host = hp[0]
  path = "/" + "/".join(hp[1:])
  return(host, path)