from Actors.keywords import *
from Demo.TrapAprox.coord import TrapCoordinator
from Actors.Common.theatre import TheatreList
import sys

def start():
 # TheatreList().addchild(here())
  TrapCoordinator(int(sys.argv[2]), int(sys.argv[1]), 0 , 20)

if __name__ == '__main__':
  initialise(start)