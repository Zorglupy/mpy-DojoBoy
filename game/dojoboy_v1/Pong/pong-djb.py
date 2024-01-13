# pongs.py
#
# by Billy Cheung  2019 10 26
# Modified By Yoyo Zorglup for the DojoBoy
#

from time import sleep_ms
from random import randint

from dojoboy_v1.dojoboy import DojoBoy

djb = DojoBoy(show_intro=True,width=160,height=128,framerate=30)

scores = [0,0]

maxScore = 15
gameOver = False
exitGame = False

class Rect (object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move (self, vx, vy) :
        self.x = self.x + vx
        self.y = self.y + vy

    def colliderect (self, rect1) :
      if (self.x + self.w   > rect1.x and
        self.x < rect1.x + rect1.w  and
        self.y + self.h > rect1.y and
        self.y < rect1.y + rect1.h) :
        return True
      else:
        return False

class bat(Rect):
  def __init__(self, velocity, up_key, down_key, *args, **kwargs):
    self.velocity = velocity
    self.up_key = up_key
    self.down_key = down_key
    super().__init__(*args, **kwargs)

  def move_bat(self, board_height, bat_HEIGHT, balls):
    djb.scan_jst_btn()

    if self.up_key == 0  : # use AI
      ballXdiff = 40
      ballY = -1
      for ball in balls :
          if abs(ball.x - self.x) < ballXdiff :
              ballXdiff = abs(ball.x - self.x)
              ballY = ball.y
      if ballY >= 0 :
          self.y = max(min(ballY - pong.bat_HEIGHT//2 +  randint(0,pong.bat_HEIGHT//2+1), board_height-pong.bat_HEIGHT),0)

    elif self.up_key == -1 : # use Paddle
      self.y = int (djb.getPaddle() / (1024 / (board_height-pong.bat_HEIGHT)))
      self.y = int (djb.getPaddle() / (1024 / (board_height-pong.bat_HEIGHT)))

    elif self.up_key == -2 : # use Paddle 2
      self.y = int (djb.getPaddle2() / (1024 / (board_height-pong.bat_HEIGHT)))
    else :
      if djb.pressed(self.up_key):
          self.y = max(self.y - self.velocity,0)
      if djb.pressed(self.down_key):
          self.y = min(self.y + self.velocity, board_height-pong.bat_HEIGHT)

class Ball(Rect):
    def __init__(self, velocity, *args, **kwargs):
        self.velocity = velocity
        self.angle = 0
        super().__init__(*args, **kwargs)

    def move_ball(self):
        self.x += self.velocity
        self.y += self.angle


class Pong:
    HEIGHT = djb.display.height
    WIDTH = djb.display.width

    bat_WIDTH = 5
    bat_HEIGHT = 20
    bat_VELOCITY = 3

    BALL_WIDTH = 4
    BALL_VELOCITY = 2
    BALL_ANGLE = 0

    COLOUR = djb.display.WHITE_H
    scores = [0,0]
    maxScore = 15
    maxballs = 2
    ballschance = 50

    def init (self, onePlayer, demo, usePaddle):
        # Setup the screen
        global scores
        scores = [0,0]
        # Create the player objects.
        self.bats = []
        self.balls = []

        if demo :
          self.bats.append(bat(  # The left bat, AI
              self.bat_VELOCITY,
              0,
              0,
              0,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT))
        elif usePaddle :
          self.bats.append(bat(  # The left bat, use Paddle
              self.bat_VELOCITY,
              -1,
              -1,
              0,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT))
        else :
          self.bats.append(bat(  # The left bat, button controlled
              self.bat_VELOCITY,
              djb.btn_Up,
              djb.btn_Down,
              0,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT))

        # set up control method for left Bat
        if demo or onePlayer:
          self.bats.append(bat(  # The right bat, AI
              self.bat_VELOCITY,
              0,
              0,
              self.WIDTH - self.bat_WIDTH-1,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT
              ))
        elif usePaddle and djb.paddle2 :  # only use paddle2 if its present on the boards
          self.bats.append(bat(      # The right bat, use Paddle
              self.bat_VELOCITY,
              -2,
              -2,
              self.WIDTH - self.bat_WIDTH-1,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT))
        else :  # use buttons for the right bat
          self.bats.append(bat(  # The right bat, button controlled
              self.bat_VELOCITY,
              djb.btnB,
              djb.btnA,
              self.WIDTH - self.bat_WIDTH-1,
              int(self.HEIGHT / 2 - self.bat_HEIGHT / 2),
              self.bat_WIDTH,
              self.bat_HEIGHT
              ))

        self.balls.append(Ball(
            self.BALL_VELOCITY,
            int(self.WIDTH / 2 - self.BALL_WIDTH / 2),
            int(self.HEIGHT / 2 - self.BALL_WIDTH / 2),
            self.BALL_WIDTH,
            self.BALL_WIDTH))

    def score(self, player, ball):
      global gameOver
      global scores
      scores[player] += 1
      djb.play_tone ('G4', 100)

      if len (self.balls) > 1 :
          self.balls.remove(ball)
      else :
          ball.velocity = - ball.velocity
          ball.angle = randint(0,3) - 2
          ball.x = int(self.WIDTH / 2 - self.BALL_WIDTH / 2)
          ball.y = int(self.HEIGHT / 2 - self.BALL_WIDTH / 2)
      if scores[player] >= maxScore :
        gameOver = True

    def check_ball_hits_wall(self):
      for ball in self.balls:

        if ball.x < 0:
          self.score(1, ball)

        if ball.x > self.WIDTH :
          self.score(0, ball)

        if ball.y > self.HEIGHT - self.BALL_WIDTH or ball.y < 0:
          ball.angle = -ball.angle

    def check_ball_hits_bat(self):
      for ball in self.balls:
          for bat in self.bats:
            if ball.colliderect(bat):
                  ball.velocity = -ball.velocity
                  ball.angle = randint (0,3) - 2
                  djb.play_tone ('C6', 10)
                  break

    def game_loop(self):
      global gameOver, exitGame, scores
      demoOn = False
      exitGame = False
      while not exitGame:
        if demoOn :
            playsers = 0
            demo = True
        else :
            players = 1
            demo = False

        onePlayer = True
        usePaddle = False
        gameOver = False

        #menu screen
        while True:
            djb.display.fill(0)
            djb.display.text('Pong', 0, 0, djb.display.WHITE_H)
            djb.display.rect(90,0, djb.max_vol*4+2,6, djb.display.WHITE_H)
            djb.display.rect(91,1, djb.vol[0] * 4,4, djb.display.RED_H, True)
            djb.display.text('A Start  B+L Quit', 0, 10, djb.display.WHITE_H)
            if usePaddle :
                djb.display.text('U Paddle', 0,20, djb.display.WHITE_H)
            else :
                djb.display.text('U Button', 0,20, djb.display.WHITE_H)
            if players == 0 :
                djb.display.text('D AI-Player', 0,30, djb.display.WHITE_H)
            elif players == 1 :
                djb.display.text('D 1-Player', 0,30, djb.display.WHITE_H)
            else :
                djb.display.text('D 2-Player', 0,30, djb.display.WHITE_H)
            djb.display.text('M + U/D Frame/s {}'.format(djb.display.frame_rate), 0,40, djb.display.WHITE_H)
            djb.display.text('V + U/D Sound', 0, 50, djb.display.WHITE_H)
            djb.display.show()
            sleep_ms(10)
            djb.scan_jst_btn()
            if djb.setVolume() :
                pass
            elif djb.setFrameRate():
                pass
            elif djb.pressed (djb.btn_B) and djb.just_pressed(djb.btn_Left) :
                exitGame = True
                gameOver= True
                break
            elif djb.just_pressed(djb.btn_A) or demoOn :
                if players == 0 : # demo
                    onePlayer = False
                    demo = True
                    demoOn = True
                    djb.display.fill(0)
                    djb.display.text('DEMO', 5, 0, djb.display.WHITE_H)
                    djb.display.text('B+L to Stop', 5, 30, djb.display.WHITE_H)
                    djb.display.show()
                    sleep_ms(1000)

                elif players == 1 :
                    onePlayer = True
                    demo = False
                else :
                    onePlayer = False
                    demo = False
                break
            elif djb.just_pressed(djb.btn_Up) :
                usePaddle = not usePaddle
            elif djb.just_pressed(djb.btn_Down) :
                players = (players + 1) % 3

        self.init(onePlayer, demo, usePaddle)

        #game loop

        while not gameOver:
          djb.scan_jst_btn()
          if djb.pressed (djb.btn_B) and djb.justReleased(djb.btn_Left) :
              gameOver = True
              demoOn = False


          self.check_ball_hits_bat()
          self.check_ball_hits_wall()

          # Redraw the screen.
          djb.display.fill(0)

          for bat in self.bats:
            bat.move_bat(self.HEIGHT, self.bat_HEIGHT,self.balls)
            djb.display.rect(bat.x,bat.y,self.bat_WIDTH, self.bat_HEIGHT, self.COLOUR, True)

          for ball in self.balls:
            ball.move_ball()
            djb.display.rect(ball.x,ball.y,self.BALL_WIDTH ,self.BALL_WIDTH, self.COLOUR, True)


          djb.display.center_text_XY ('{} : {}'.format (scores[0], scores[1]), -1, 0, djb.display.WHITE_H)

          if gameOver :
            djb.display.rect(25,25,100, 30,0, True)
            djb.display.text ("Game Over", 30, 30, djb.display.RED_H)
            djb.display.show()
            djb.play_tone ('C5', 200)
            djb.play_tone ('G4', 200)
            djb.play_tone ('G4', 200)
            djb.play_tone ('A4', 200)
            djb.play_tone ('G4', 400)
            djb.play_tone ('B4', 200)
            djb.play_tone ('C5', 400)
          elif len(self.balls) < self.maxballs and randint(0,10000) < self.ballschance :
                  self.balls.append(Ball(
                      self.BALL_VELOCITY,
                      int(self.WIDTH / 2 - self.BALL_WIDTH / 2),
                      int(self.HEIGHT / 2 - self.BALL_WIDTH / 2),
                      self.BALL_WIDTH,
                      self.BALL_WIDTH))

          djb.display.show_and_wait()


#if __name__ == '__main__':
pong = Pong()
pong.game_loop()

#if djb.ESP32 :
#    djb.deinit()
#    del sys.modules["gameESP"]
#gc.collect()

#print ("game exit")
