from Actors.keywords import *
from Demo.HTTP.Browser.browser import Browser
from Actors.Common.theatre import RegisteredTheatre

def start():
  RegisteredTheatre()
  Browser()
  
if __name__ == '__main__':
  initialise(start)