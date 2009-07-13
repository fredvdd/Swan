from Actors.keywords import *
from Demo.OTP.visual import VisualRootSupervisor, VisualSupervisor, VisualFixedWorker, VisualMobileWorker

def start():
    r = VisualRootSupervisor()
    s = VisualSupervisor(r)
    VisualFixedWorker(s)
    VisualMobileWorker(s)
  
if __name__ == '__main__':
  initialise(start)