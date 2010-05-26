import socket
from time import time

for i in range(0,5):
	start = time()
	s = socket.create_connection(('localhost',8080))
	wfile = s.makefile('w')
	wfile.write("GET /test.html HTTP/1.1\n")
	wfile.write(
		"Accept:application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\n"
		"Referer:http://localhost:8080/test.html\n"
		"User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.38 Safari/533.4\n\n"
	)
	wfile.flush()
	rfile = s.makefile('r')
	response = rfile.readline()
	print response
	print "Test %s : %s" % (i,time()-start)

	
	