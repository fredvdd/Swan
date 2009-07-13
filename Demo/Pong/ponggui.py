from Actors.keywords import *
from Actors.Device.GTK.widgets import *
from Actors.Device.GTK.drawing import *
from Actors.Device.GTK.layout import *
from Demo.Pong.pongmanager import PictureInPictureManager

BAT_SIZE     = (20, 70)
BAT_X_OFFSET = 50 
BOARD_SIZE   = (580,353) 

PIP_BAT_SIZE     = (8, 25)
PIP_BOARD_SIZE   = (130, 90)
PIP_BAT_X_OFFSET = 10
PIP_BALL_SIZE    = (7, 7)
      
class PongWindow(Window):
  
  def birth(self, player):
    self.canvas = PongCanvas(player)
    self.picture = PictureInPictureList()
    self.split = VPair(Frame('Game', self.canvas), HList([]))
    self.player = player
    Window.birth(self, HPair(self.split, self.picture))

  def settheatres(self, theatres, score):
    buttons = []
    buttons.append(Label("Score: %s" % score))
    for theatre in theatres:
      if theatre == here():
        buttons.append(DisabledButton(theatre))
      else:
        buttons.append(Button(theatre).on_click(self.migratepressed))
    self.split.setsecond(HList(buttons))

  def incoming(self, ball):
    self.canvas.ballenters(ball)
     
  def getbatpc(self):
    return self.canvas.getbatpc()
     
  def migratepressed(self, button):
    self.canvas.pause()
    self.player.migraterequested(button.get_title())
    
  def theatreclosing(self):
    self.kill()
    
class BatController(MobileActor):

  def birth(self, bat):
    self.bat = bat

  def mousemove(self, x, y):
    pass
  #  self.bat.moveto(y - BAT_SIZE[1]/2)

  def migrate_to(self, theatre):
    migrate_to(theatre)
    
class PongCanvas(Canvas):  
  
  def birth(self, player):
     Canvas.birth(self, BOARD_SIZE)
     self.player = player
     self.ball = None
     self.bat = Bat(self, self.size[0] - BAT_X_OFFSET)
     self.batcontroller = BatController(self.bat)
     #self.mouselisten(self.batcontroller)
    
  def getbatpc(self):
    ypos = sync(self.bat.getypos())
    return ypos / float(self.size[1])
  
  def intersection(self):
    self.ball.hit()
  
  def ballenters(self, ball):
    self.ball = ball
    ball.attach(self, here(), self.size)
  
  def addball(self, x, y, width, height):
    return Rect(self, x, y, width, height)
  
  def pause(self):
    if self.ball:
      self.ball.pause()
  
  def leaving(self, ball, result):
    self.ball = None
    self.player.leaving(ball, result)

  def arrived(self):
    Canvas.arrived(self)
    self.batcontroller.migrate_to(here())
    if self.ball:
      self.ball.migrate_to(here())
    
class PictureInPictureList(VList):
  
  def birth(self):
    VList.birth(self, [])
    self.screens = dict()
    self.dontequalise()
    PictureInPictureManager().addchild(self)
    self.remoteball = Rect(None, 0, 0, PIP_BALL_SIZE[0], PIP_BALL_SIZE[1])
    
  def ball_at(self, player,  xpc, ypc):
    if player in self.screens:
      screen = self.screens[player]
      screen.ballhere(self.remoteball,PIP_BOARD_SIZE[0] * xpc, PIP_BOARD_SIZE[1] * ypc)
    
  def bats_at(self, batpositions):
    for (player, ypc) in batpositions:
      if player in self.screens:
        screen = self.screens[player]
        screen.setbatpos(ypc)
    
  def setplayers(self, players):
    self.refreshscreens(players)
    
  def arrived(self):
    VList.arrived(self)
    self.remoteball.migrate_to(here())
    
  def refreshscreens(self, players):
    self.clear()
    self.screens = dict()
    i = 1
    for player in players:
      picture = PictureInPicture('Player %s' % i)
      self.screens[player] = picture
      self.add(picture)
      i += 1
    self.update()

class PictureInPicture(Frame):
  
  def birth(self, name):
    self.canvas = Canvas(PIP_BOARD_SIZE)
    self.bat = Rect(self.canvas, PIP_BOARD_SIZE[0] - PIP_BAT_X_OFFSET, 10, PIP_BAT_SIZE[0], PIP_BAT_SIZE[1])
    Frame.birth(self, name, self.canvas)
    
  def ballhere(self, ball, x, y):
    currently = sync(ball.attached_to())
    if self.canvas != currently:
      ball.detach()
      ball.attach(self.canvas)
    ball.setpos(x, y)
    
  def setbatpos(self, ypc):
    y = int(ypc * PIP_BOARD_SIZE[1])
    self.bat.setpos(PIP_BOARD_SIZE[0] - PIP_BAT_X_OFFSET, y)
    
class Bat(Rect):
  
  def getypos(self):
    return self.ypos
  
  def birth(self, canvas, xpos):
    self.ypos = 150
    self.xpos = xpos
    Rect.birth(self, canvas, xpos, self.ypos, BAT_SIZE[0], BAT_SIZE[1])
    
  def moveto(self, ypos):
    self.ypos = ypos
    self.setpos(self.xpos, self.ypos)