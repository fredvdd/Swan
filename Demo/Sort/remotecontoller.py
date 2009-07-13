from Actors.keywords import *
from Demo.Sort.sorter import Sorter
import random
import time


class Controller(MobileActor):

  def birth(self):
    self.done = False
    self.array = [random.randint(0, 100) for i in range(0, 10)]
    print('Sorting locally:', self.array)
    self.begin = time.time()
    self.sorters = list()

    self.a_sorter = Sorter()
    self.a_sorter.sort(self.array, Reference(self.actor_id))
    
    self.begin = time.time()
    self.done = False
        
    for i in range(0, 4):
      self.sorters.append(Sorter())
    
    for i in range(0, 2):
      self.sorters[i].migrate_to('192.168.1.78:8000')
    
    for i in range(2, 4):
      self.sorters[i].migrate_to('192.168.1.78:8001')

    for sorter in self.sorters:
      sorter.sort(self.array, Reference(self.actor_id))
      
      
  def answer(self, array):
    if not self.done:
      fin = time.time()
      print ('Array has been sorted:', array )
      print ('This took:', fin - self.begin)
      self.done1 = True
    
    
def start():
    Controller()        

if __name__ == '__main__':
  initialise(start)
