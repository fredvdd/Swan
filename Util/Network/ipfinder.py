import socketutil
import threading
import socket


def create_ip_server(port):
  threading.Timer(0, ip_server, [port]).start()

def ip_server(port):
  try:
    ip_sock = socketutil.server_socket(port)
    while True:
      conn, (ip, port) = ip_sock.accept()
      print 'pinged by', ip
      data = conn.recv(1024)
      conn.send(ip)
      conn.close()
  except:
    print "Stopping ip_server due to error"
      
def get_ip(ip, port):
  ip_sock = socketutil.client_socket()
  ip_sock.connect((ip, port))
  ip_sock.send('PING')
  my_ip = ip_sock.recv(1024)
  ip_sock.close()
  return str(my_ip)