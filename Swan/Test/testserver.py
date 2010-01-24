import time
import BaseHTTPServer
from Actors.keywords import *
from Swan.server import Server 


HOST_NAME = 'localhost' #
PORT_NUMBER = 8080 #


class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        print "Hello Handler"

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

class TestActor(LocalActor):
    
    def birth(self):
        print "Test Actor Born"
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), Server)
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
        

    def userwrote(self, line):
        print line
        if line == "die":
	        self.die()
        #else:
        #    Keyboard().readline(Reference(self.actor_id))

def start():
    Server("localhost", 8080)
    #TestActor()
    #server_class = BaseHTTPServer.HTTPServer
    #httpd = server_class((HOST_NAME, PORT_NUMBER), Server)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    #try:
    #    httpd.serve_forever()
    #except KeyboardInterrupt:
    #    pass
    #httpd.server_close()
    #print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)


if __name__ == '__main__':
    initialise(start)