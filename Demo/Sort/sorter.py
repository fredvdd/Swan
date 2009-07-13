from Actors.keywords import *
import random

class Sorter(MobileActor):

  def birth(self):
    pass

  def sort(self, array, reply):
      while not all([a <= b for a,b in zip(array, array[1:])]):
          random.shuffle(array)
      reply.answer(array)
