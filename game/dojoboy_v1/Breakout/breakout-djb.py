# ----------------------------------------------------------
#  Breakout.py  Game
# by Billy Cheung  2019 10 26
# Modified By Yoyo Zorglup for the DojoBoy 2023 12 25
# ----------------------------------------------------------

from time import sleep_ms,ticks_ms, ticks_diff
from math import sqrt
from random import randint
from dojoboy_v1.dojoboy import DojoBoy

djb = DojoBoy(show_intro=True,width=160,height=128,framerate=30)

PADDLE_W = 22
PADDLE_H = 10

BALL_W = BALL_H = 6

BRICK_W = (djb.display.width//8)-2
BRICK_H = 10

class Ball(object):
    """Ball."""

    def __init__(self, x, y, x_speed, y_speed, display, width=2, height=2,
                 frozen=False):
        self.x = x
        self.y = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.prev_x = x
        self.prev_y = y
        self.width = width
        self.height = height
        self.center = width // 2
        self.max_x_speed = 3
        self.max_y_speed = 3
        self.frozen = frozen
        self.display = display
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_speed2 = 0.0
        self.y_speed2 = 0.0
        self.created = ticks_ms()

    def clear(self):
        """Clear ball."""
        self.display.rect(self.x, self.y, self.width, self.height, djb.display.BLACK, True)

    def clear_previous(self):
        """Clear prevous ball position."""
        self.display.rect(self.prev_x, self.prev_y, self.width, self.height, djb.display.BLACK, True)

    def draw(self):
        """Draw ball."""
        self.clear_previous()
        self.display.rect( self.x, self.y, self.width, self.height, djb.display.RED_H, True)

    def set_position(self, paddle_x, paddle_y, paddle_x2, paddle_center):
        bounced = False
        """Set ball position."""
        self.prev_x = self.x
        self.prev_y = self.y
        # Check if frozen to paddle
        if self.frozen:
            # Freeze ball to top center of paddle
            self.x = paddle_x + (paddle_center - self.center)
            self.y = paddle_y - self.height
            if ticks_diff(ticks_ms(), self.created) >= 2000:
                # Release frozen ball after 2 seconds
                self.frozen = False
            else:
                return
        self.x += int(self.x_speed) + int(self.x_speed2)
        self.x_speed2 -= int(self.x_speed2)
        self.x_speed2 += self.x_speed - int(self.x_speed)

        self.y += int(self.y_speed) + int(self.y_speed2)
        self.y_speed2 -= int(self.y_speed2)
        self.y_speed2 += self.y_speed - int(self.y_speed)

        # Bounces off walls
        if self.y < 10:
            self.y = 10
            self.y_speed = -self.y_speed
            bounced = True
        if self.x + self.width >= djb.display.width - 3:
            self.x = djb.display.width - 3 - self.width
            self.x_speed = -self.x_speed
            bounced = True
        elif self.x < 3:
            self.x = 3
            self.x_speed = -self.x_speed
            bounced = True

        # Check for collision with Paddle
        if (self.y2 >= paddle_y and
           self.x <= paddle_x2 and
           self.x2 >= paddle_x):
            # Ball bounces off paddle
            self.y = paddle_y - (self.height + 1)
            ratio = ((self.x + self.center) -
                     (paddle_x + paddle_center)) / paddle_center
            self.x_speed = ratio * self.max_x_speed
            self.y_speed = -sqrt(max(1, self.max_y_speed ** 2 - self.x_speed ** 2))
            bounced = True

        self.x2 = self.x + self.width - 1
        self.y2 = self.y + self.height - 1
        return bounced


class Brick(object):
    """Brick."""

    def __init__(self, x, y, color, display, width=12, height=3):
        """Initialize brick.

        Args:
            x, y (int):  X,Y coordinates.
            color (string):  Blue, Green, Pink, Red or Yellow.
            display (SSD1351): OLED djb.
            width (Optional int): Blick width
            height (Optional int): Blick height
        """
        self.x = x
        self.y = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.center_x = x + (width // 2)
        self.center_y = y + (height // 2)
        self.color = color
        self.width = width
        self.height = height
        self.display = display
        self.draw()

    def bounce(self, ball_x, ball_y, ball_x2, ball_y2,
               x_speed, y_speed,
               ball_center_x, ball_center_y):
        """Determine bounce for ball collision with brick."""
        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2
        center_x = self.center_x
        center_y = self.center_y
        if ((ball_center_x > center_x) and
           (ball_center_y > center_y)):
            if (ball_center_x - x2) < (ball_center_y - y2):
                y_speed = -y_speed
            elif (ball_center_x - x2) > (ball_center_y - y2):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x > center_x) and
              (ball_center_y < center_y)):
            if (ball_center_x - x2) < -(ball_center_y - y):
                y_speed = -y_speed
            elif (ball_center_x - x2) > -(ball_center_y - y):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x < center_x) and
              (ball_center_y < center_y)):
            if -(ball_center_x - x) < -(ball_center_y - y):
                y_speed = -y_speed
            elif -(ball_center_x - x) > -(ball_center_y - y):
                y_speed = -y_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x < center_x) and
              (ball_center_y > center_y)):
            if -(ball_center_x - x) < (ball_center_y - y2):
                y_speed = -y_speed
            elif -(ball_center_x - x) > (ball_center_y - y2):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed

        return [x_speed, y_speed]

    def clear(self):
        """Clear brick."""
        self.display.rect(self.x, self.y, self.width, self.height, djb.display.BLACK, True)

    def draw(self):
        """Draw brick."""
        self.display.rect(self.x, self.y, self.width, self.height, self.color, True)
        self.display.rect(self.x, self.y, self.width, self.height, djb.display.WHITE_H) 

class Life(object):
    """Life."""

    def __init__(self, index, display, width=4, height=6):
        """Initialize life.

        Args:
            index (int): Life number (1-based).
            display (SSD1351): OLED djb.
            width (Optional int): Life width
            height (Optional int): Life height
        """
        margin = 5
        self.display = display
        self.x = djb.display.width - (index * (width + margin))
        self.y = 0
        self.width = width
        self.height = height
        self.draw()

    def clear(self):
        """Clear life."""
        self.display.rect(self.x, self.y, self.width, self.height, djb.display.BLACK, True)

    def draw(self):
        """Draw life."""
        self.display.rect(self.x, self.y, self.width, self.height,djb.display.WHITE_H, True)


class Paddle(object):
    """Paddle."""

    def __init__(self, display, width, height):
        """Initialize paddle.

        Args:
            display (SSD1306): OLED djb.
            width (Optional int): Paddle width
            height (Optional int): Paddle height
        """
        self.x = djb.display.width//2
        self.y = djb.display.height - 5
        self.x2 = self.x + width - 1
        self.y2 = self.y + height - 1
        self.width = width
        self.height = height
        self.center = width // 2
        self.display = display

    def clear(self):
        """Clear paddle."""
        self.display.rect(self.x, self.y, self.width, self.height, djb.display.BLACK, True)


    def draw(self):
        """Draw paddle."""
        self.display.rect(self.x, self.y,self.width, self.height, djb.display.BLUE_H, True)

    def h_position(self, x):
        """Set paddle position.

        Args:
            x (int):  X coordinate.
        """
        new_x = max(3,min (x, djb.display.width-self.width))
        if new_x != self.x :  # Check if paddle moved
            prev_x = self.x  # Store previous x position
            self.x = new_x
            self.x2 = self.x + self.width - 1
            self.y2 = self.y + self.height - 1
            self.draw()
            # Clear previous paddle
            if x > prev_x:
                self.display.rect(prev_x, self.y, x - prev_x, self.height, djb.display.BLACK, True)
            else:
                self.display.rect(x + self.width, self.y, (prev_x + self.width)-(x + self.width), self.height, djb.display.BLACK, True)
        else:
            self.draw()

class Score(object):
    """Score."""

    def __init__(self, display):
        """Initialize score.

        Args:
            display (SSD1306): OLED djb.
        """
        margin = 5
        self.display = display
        self.display.text('S:', margin, 0, djb.display.WHITE_H)
        self.x = 20 + margin
        self.y = 0
        self.value = 0
        self.draw()

    def draw(self):
        """Draw score value."""
        self.display.rect(self.x, self.y, 20, 8, djb.display.BLACK, True)
        self.display.text( str(self.value), self.x, self.y, djb.display.WHITE_H)

    def game_over(self):
        """Display game_over."""
        self.display.text('GAME OVER', (self.display.width // 2) - 30,
                               int(self.display.height // 1.5), djb.display.WHITE_H)

    def increment(self, points):
        """Increase score by specified points."""
        self.value += points
        self.draw()

def load_level(level, display) :
    #global frameRate
    if demo :
      djb.display.frame_rate = 60 + level * 10
    else :
      djb.display.frameRate = djb.display.frame_rate + level * 5
    bricks = []
    for row in range(12, 40 + 6 * level , 12):
        brick_color = djb.display.color_pal[level%16]
        for col in range(1, djb.display.width, BRICK_W + 2 ):
            bricks.append(Brick(col, row, brick_color, display, BRICK_W, BRICK_H))

    return bricks

demoOn = False
exitGame = False

while not exitGame :
    #paddle_width = 22
    #frameRate = 30
    #gc.collect()
    #print (gc.mem_free())


    gameOver = False
    usePaddle = False
    if demoOn :
        demo = True
    else :
        demo = False


    while True:
        djb.display.fill(djb.display.BLACK)
        djb.display.text('BREAKOUT', 0, 0, djb.display.WHITE_H)
        djb.display.rect(90,0, djb.max_vol*4+2,6, djb.display.WHITE_H)
        djb.display.fill_rect(91,1, djb.vol[0] * 4,4, djb.display.RED_H)
        djb.display.text('A Start  L Quit', 0, 10, djb.display.WHITE_H)
        if usePaddle :
            djb.display.text('Up Paddle', 0,20, djb.display.WHITE_H)
        else :
            djb.display.text('Up Button', 0,20, djb.display.WHITE_H)
        if demo :
            djb.display.text('Dw AI-Player', 0,30, djb.display.WHITE_H)
        else :
            djb.display.text('Dw 1-Player', 0,30, djb.display.WHITE_H)
        djb.display.text('M + U/D Frame/s {}'.format(djb.display.frame_rate), 0,40, djb.display.WHITE_H)
        djb.display.text('V + U/D Sound', 0, 50, djb.display.WHITE_H)
        djb.display.show()

        djb.scan_jst_btn()
        if djb.setVolume() :
            pass
        elif djb.setFrameRate():
            pass
        elif djb.just_released(djb.btn_Left) :
            exitGame = True
            gameOver= True
            break
        elif djb.just_pressed(djb.btn_A) or demoOn :
            if demo :
                djb.display.fill(0)
                djb.display.text('DEMO', 5, 0, djb.display.WHITE_H)
                djb.display.text('B to Stop', 5, 30, djb.display.WHITE_H)
                djb.display.show()
                sleep_ms(1000)
                demoOn = True
            break
        elif djb.just_pressed(djb.btn_Up) :
            usePaddle =  not usePaddle
        elif djb.just_pressed(djb.btn_Down) :
            demo = not demo

    if not exitGame :
      djb.display.fill(djb.display.BLACK)

      # Generate bricks
      MAX_LEVEL = const(5)
      level = 1
      bricks = load_level(level, djb.display)

      # Initialize paddle
      paddle = Paddle(djb.display, PADDLE_W, PADDLE_H)

      # Initialize score
      score = Score(djb.display)

      # Initialize balls
      balls = []
      # Add first ball
      balls.append(Ball(djb.display.width//2, djb.display.height - 10, -2, -1, djb.display, BALL_W, BALL_H, frozen=True))

      # Initialize lives
      lives = []
      for i in range(1, 3):
          lives.append(Life(i, djb.display))

      prev_paddle_vect = 0

      djb.display.show()


      try:
          while not gameOver :
              djb.scan_jst_btn()
              if demo :
                if djb.just_released (djb.btn_B) :
                  djb.display.text('Demo stopped', 5, 30, djb.display.WHITE_H)
                  djb.display.show()
                  sleep_ms(1000)
                  gameOver = True
                  demoOn = False
                else :
                  paddle.h_position(balls[0].x - 5 + randint (0,7))
              elif usePaddle :
                paddle.h_position(int(djb.getPaddle() // 9.57))
              else :
                paddle_vect = 0
                if djb.pressed(djb.btn_Left | djb.btn_B) :
                  paddle_vect = -1
                elif djb.pressed(djb.btn_Right | djb.btn_A) :
                  paddle_vect = 1
                if paddle_vect != prev_paddle_vect :
                  paddle_vect *= 3
                else :
                  paddle_vect *= 5
                paddle.h_position(paddle.x + paddle_vect)
                prev_paddle_vect = paddle_vect

               # Handle balls
              score_points = 0
              for ball in balls:
                  # move ball and check if bounced off walls and paddle
                  if ball.set_position(paddle.x, paddle.y,paddle.x2, paddle.center):
                      djb.play_freq(900, 10)
                  # Check for collision with bricks if not frozen
                  if not ball.frozen:
                      prior_collision = False
                      ball_x = ball.x
                      ball_y = ball.y
                      ball_x2 = ball.x2
                      ball_y2 = ball.y2
                      ball_center_x = ball.x + ((ball.x2 + 1 - ball.x) // 2)
                      ball_center_y = ball.y + ((ball.y2 + 1 - ball.y) // 2)

                      # Check for hits
                      for brick in bricks:
                          if(ball_x2 >= brick.x and
                             ball_x <= brick.x2 and
                             ball_y2 >= brick.y and
                             ball_y <= brick.y2):
                              # Hit
                              if not prior_collision:
                                  ball.x_speed, ball.y_speed = brick.bounce(
                                      ball.x,
                                      ball.y,
                                      ball.x2,
                                      ball.y2,
                                      ball.x_speed,
                                      ball.y_speed,
                                      ball_center_x,
                                      ball_center_y)
                                  djb.play_tone('C6', 10)
                                  prior_collision = True
                              score_points += 1
                              brick.clear()
                              bricks.remove(brick)

                  # Check for missed
                  if ball.y2 > djb.display.height - 2:
                      ball.clear_previous()
                      balls.remove(ball)
                      if not balls:
                          # Lose life if last ball on screen
                          if len(lives) == 0:
                              score.game_over()
                              djb.play_tone('G4', 500)
                              djb.play_tone('C5', 200)
                              djb.play_tone('F4', 500)
                              gameOver = True
                          else:
                              # Subtract Life
                              lives.pop().clear()
                              # Add ball
                              balls.append(Ball(djb.display.width//2, djb.display.height - 10, 2, -3, djb.display, BALL_W, BALL_H,
                                           frozen=True))
                  else:
                      # Draw ball
                      ball.draw()
              # Update score if changed
              if score_points:
                  score.increment(score_points)

              # Check for level completion
              if not bricks:
                  for ball in balls:
                      ball.clear()
                  balls.clear()
                  level += 1
                  PADDLE_W -=2
                  if level > MAX_LEVEL:
                      level = 1
                  bricks = load_level(level, djb.display)
                  balls.append(Ball(djb.display.width//2, djb.display.height - 10, -2, -1, djb.display, BALL_W, BALL_H, frozen=True))
                  djb.play_tone('C5', 20)
                  djb.play_tone('D5', 20)
                  djb.play_tone('E5', 20)
                  djb.play_tone('F5', 20)
                  djb.play_tone('G5', 20)
                  djb.play_tone('A5', 20)
                  djb.play_tone('B5', 20)
                  djb.play_tone('C6', 20)
              djb.display.show_and_wait()
      except KeyboardInterrupt:
              djb.cleanup()
      sleep_ms(2000)

