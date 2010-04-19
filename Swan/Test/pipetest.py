from multiprocessing import Process, Pipe
import socket

def f(conn):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',8080))
	sock.listen(5)
	conn, address = sock.accept()
	print "accepted %s : %s" % (conn, address) 
	conn.send(conn)
	#conn.close()

if __name__ == '__main__':
	parent_conn, child_conn = Pipe()
	p = Process(target=f, args=(child_conn,))
	p.start()
	clisock = parent_conn.recv()   # prints "[42, None, 'hello']"
	print "received %s" % clisock
	p.join()