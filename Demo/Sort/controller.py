from Actors.keywords import *
from Demo.Sort.sorter import Sorter
import random
import time


class Controller(MobileActor):

  def birth(self):
    self.done = False
    self.array = [random.randint(0, 100) for i in range(0, 8)]
    print('Trying to sort:', self.array)
    self.begin = time.time()
    self.sorters = list()
    for i in range(0, 4):
      self.sorters.append(Sorter())
      
    for sorter in self.sorters:
      sorter.sort(self.array, Reference(self.actor_id))

  def answer(self, array):
    if not self.done:
      fin = time.time()
      print ('Array has been sorted:', array )
      print ('This took:', fin - self.begin)
      self.done = True
    
    
def start():
    Controller()        

if __name__ == '__main__':
  initialise(start)
