from Actors.keywords import *
from Actors.Common.server import BServer

class ChatServer(BServer):

  def say(self, message):
    for child in self.children:
      child(message)
