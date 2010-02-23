from Actors.keywords import *
from time import sleep

class EchoActor(MobileActor):
	
	def birth(self):
		print "Echo Actor"
	
	def echo(self, msg):
		print "Received message: %s" % msg
		return "Echo %s" % msg

class TestActor(MobileActor):
	
	def birth(self, echo):
		print "Test Actor"
		self.echo = echo
		self.send("and Bounce")
	
	def send(self, msg):
		reply = self.echo.echo(msg)
		print "Sleeping"
		sleep(5)
		print "Awake"
		print "Received reply: %s" % reply


def start():
	a = EchoActor()
	b = TestActor(a)

if __name__ == '__main__':
    initialise(start)