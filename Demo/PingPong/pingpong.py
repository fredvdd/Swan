from Actors.keywords import LocalActor, ready, sync, callback, initialise

class Ponger(LocalActor):
  
    def pong(self, pinger):
        print "pong"
        pinger.ping(self)

class Pinger(LocalActor):
  
    def birth(self):
        m1 = Ponger()
        m1.pong(self)
        

    def ping(self, ponger):
        print 'ping'
        ponger.pong(self)
    
    
def start():
    Pinger()
  
if __name__ == '__main__':
    initialise(start)