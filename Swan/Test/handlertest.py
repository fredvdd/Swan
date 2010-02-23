import socket
import unittest

class RequestTest(unittest.TestCase):

	def setUp(self):
		self.socket = socket.create_connection(('localhost', 8080))
		
	def tearDown(self):
		self.socket.close()
	
	def testRequest(self):
		wfile = self.socket.makefile('w')
		wfile.write("%s %s HTTP/1.1\r\nConnection:keep-alive\r\n\r\n" %
			("GET", "/files/test.html")
		)
		for line in self.socket.makefile('r').readlines():
			print line
			
	def testOptions(self):
		wfile = self.socket.makefile('w')
		wfile.write("%s %s HTTP/1.1\r\nConnection:keep-alive\r\n\r\n" %
			("OPTIONS", "/files/test.html")
		)
		for line in self.socket.makefile('r').readlines():
			print line

if __name__ == '__main__':
    unittest.main()