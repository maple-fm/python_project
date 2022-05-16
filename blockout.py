# -*- coding:utf-8 -*-

import tkinter as tk
import random

FNT = ('Times new Roman', 20, 'bold')

block = []
for i in range(5):
  block.append([1]*10)

for i in range(10):
  block.append([0]*10)

  key = ''
  keyoff = False

def key_down(e):
  global key
  key = e.keysym

def key_up(e):
  global keyoff
  keyoff = True

class Block():
  def __init__(self):
    self.is_clr = True

  def draw_block(self, cvs, stage, score):
    self.is_clr = True
    cvs.delete('BG')
    for y in range(15):
      for x in range(10):
        gx = x*80
        gy = y*40
        if block[y][x] == 1:
          cvs.create_rectangle(gx+1, gy+4, gx+79, gy+32, fill=self.block_color(x,y), width=0, tag='BG')
          self.is_clr = False
    cvs.create_text(200, 20, text='STAGE'+str(stage), fill='white', font=FNT, tag='BG')
    cvs.create_text(600, 20, text='SCORE'+str(score), fill='white', font=FNT, tag='BG')

  def block_color(self, x, y):
    col = '#{0:x}{1:x}{2:x}'.format(15-x-int(y/3), x+1, y*3+3)
    return col

class Bar:
  def __init__(self):
    self.bar_x = 0
    self.bar_y = 540
    self.bar_range = 0

  def draw_bar(self, cvs):
    cvs.delete('BAR')
    cvs.create_rectangle(self.bar_x-80-self.bar_range, self.bar_y-12, self.bar_x+80+self.bar_range, self.bar_y+12, fill='silver', width=0, tag='BAR')
    cvs.create_rectangle(self.bar_x-78-self.bar_range, self.bar_y-14, self.bar_x+78+self.bar_range, self.bar_y+14, fill='silver', width=0, tag='BAR')
    cvs.create_rectangle(self.bar_x-78-self.bar_range, self.bar_y-12, self.bar_x+78+self.bar_range, self.bar_y+12, fill='white', width=0, tag='BAR')


  def move_bar(self,key):
    if key == 'Left' and self.bar_x > 80:
      self.bar_x = self.bar_x - 40
    if key == 'Right' and self.bar_x < 720:
      self.bar_x = self.bar_x + 40


class Ball:
  def __init__(self,bar):
    self.idx = 0
    self.tmr = 0
    self.score = 0
    self.ball_x = 0
    self.ball_y = 0
    self.ball_xp = 0
    self.ball_yp = 0
    self.bar = bar
    self.ball_count = 2

  def set_ball(self, x, y, xp, yp):
    self.ball_x = x
    self.ball_y = y
    self.ball_xp = xp
    self.ball_yp = yp

  def draw_ball(self, cvs,tag_name):
    cvs.delete(tag_name)
    cvs.create_oval(self.ball_x-20, self.ball_y-20, self.ball_x+20, self.ball_y+20, fill='gold', outline='orange', width=2, tag=tag_name)
    cvs.create_oval(self.ball_x-16, self.ball_y-16, self.ball_x+12, self.ball_y+12, fill='yellow', width=0, tag=tag_name)

  def move_ball(self, bar_x, bar_y):

    self.ball_x += self.ball_xp
    if self.ball_x < 20:
      self.ball_x = 20
      self.ball_xp = -self.ball_xp
    if self.ball_x > 780:
      self.ball_x = 780
      self.ball_xp = -self.ball_xp
    x = int(self.ball_x/80)
    y = int(self.ball_y/40)
    if block[y][x] == 1:
      block[y][x] = 0
      self.ball_xp = -self.ball_xp
      self.score += 10
      bar_long = random.randint(1,99)
      if bar_long < 30:
        self.bar.bar_range += 5
      if 31<bar_long<70:
        self.bar.bar_range -=5

    self.ball_y += self.ball_yp
    if self.ball_y >= 600:
      self.idx = 2
      self.tmr = 0
      return
    if self.ball_y < 20:
      self.ball_y = 20
      self.ball_yp = -self.ball_yp
    x = int(self.ball_x/80)
    y = int(self.ball_y/40)
    if block[y][x] == 1:
      block[y][x] = 0
      self.ball_yp = -self.ball_yp
      self.score += 10
      bar_long = random.randint(1,99)
      if bar_long < 30:
        self.bar.bar_range += 5
      if 31<bar_long<70:
        self.bar.bar_range -=5

    if bar_y-40 <= self.ball_y and self.ball_y <= bar_y:
      if bar_x-80-self.bar.bar_range <= self.ball_x and self.ball_x <= bar_x+80+self.bar.bar_range:
        self.ball_yp -= 10
        self.score += 1
      elif bar_x-100-self.bar.bar_range <= self.ball_x and self.ball_x <= bar_x-80-self.bar.bar_range:
        self.ball_yp -= 10
        self.ball_xp = random.randint(-20, -10)
        self.score += 2
      elif bar_x+80+self.bar.bar_range <= self.ball_x and self.ball_x <= bar_x+100+self.bar.bar_range:
        self.ball_yp -= 10
        self.ball_xp = random.randint(10, 20)
        self.score += 2


class Application(tk.Canvas):
  def __init__(self,root):
    super().__init__(root)
    self.root = root
    self.stage = 0
    self.cvs = tk.Canvas(root, width=800, height=640, bg='black')
    self.cvs.pack()
    self.bar = Bar()
    self.ball = Ball(self.bar)
    self.ball2 = Ball(self.bar)
    self.block = Block()

  def main_proc(self):
    global key, keyoff

    if self.ball.idx == 0:
      # タイトル画面
      self.ball.tmr += 1
      if self.ball.tmr == 1:
        self.stage = 1
        self.ball.score = 0
      if self.ball.tmr == 2:
        self.ball.ball_x = 160
        self.ball.ball_y = 240
        self.ball.ball_xp = 10
        self.ball.ball_yp = 10
        self.ball.set_ball(160,240,10,10)
        self.ball2.set_ball(400,240,-10,-10)

        # self.ball2.ball_x = 300
        # self.ball2.ball_y = 240
        # self.ball2.ball_xp = -10
        # self.ball2.ball_yp = -10

        self.bar.bar_x = 400

        self.block.draw_block(self.cvs, self.stage, self.ball.score)
        self.ball.draw_ball(self.cvs,'BALL')
        self.bar.draw_bar(self.cvs)
        self.cvs.create_text(400, 150, text='Block Out', fill='white', font=('Times new Roman', 50, 'bold'), tag='TXT')
        self.cvs.create_text(400, 300, text='START', fill='cyan', font=FNT, tag='TXT')
      if self.ball.tmr == 40:
        self.cvs.delete('TXT')
        self.ball.idx = 1
    elif self.ball.idx == 1:
      self.bar.move_bar(key)
      self.ball.move_ball(self.bar.bar_x, self.bar.bar_y)
      # self.ball2.move_ball(self.bar.bar_x, self.bar.bar_y)
      self.block.draw_block(self.cvs, self.stage, self.ball.score)
      self.ball.draw_ball(self.cvs,'BALL')
      # self.ball2.draw_ball(self.cvs,'BALL2')

      self.bar.draw_bar(self.cvs)
      if self.block.is_clr == True:
        self.ball.idx = 3
        self.ball.tmr = 0
    elif self.ball.idx == 2:
      # ゲームオーバー
      self.ball.tmr += 1
      if self.ball.tmr == 1:
        self.cvs.create_text(400, 260, text='GAME OVER', fill='red', font=FNT, tag='TXT')
      if self.ball.tmr == 15:
        self.cvs.create_text(300, 340, text='[R]eplay', fill='cyan', font=FNT, tag='TXT')
        self.cvs.create_text(500, 340, text='[N]ew game', fill='yellow', font=FNT, tag='TXT')
      if key == 'r':
        self.cvs.delete('TXT')
        self.ball.idx = 0
        self.ball.tmr = 0
      if key == 'n':
        self.cvs.delete('TXT')
        for y in range(5):
          for x in range(10):
            block[y][x] = 1
        self.ball.idx = 0
        self.ball.tmr = 0
        self.bar.bar_range = 0
    elif self.ball.idx == 3:
      # ゲームクリア
      self.ball.tmr += 1
      if self.ball.tmr == 1:
        self.cvs.create_text(400, 260, text='GAME CLEAR!', fill='lime', font=FNT, tag='TXT')
      if self.ball.tmr == 15:
        self.cvs.create_text(400, 340, text='Next [SPACE]', fill='cyan', font=FNT, tag='TXT')
      if key == 'space':
        self.cvs.delete('TXT')
        for y in range(5):
          for x in range(10):
            block[y][x] = 1
        self.ball.idx = 0
        self.ball.tmr = 1
        self.bar.bar_range = 0
        self.stage += 1



    if keyoff == True:
      keyoff = False
      if key != '':
        key = ''


    self.root.after(50, self.main_proc)

def main():

  root = tk.Tk()
  root.title('ブロック崩しゲーム')
  root.resizable(False,False)
  root.bind('<Key>', key_down)
  root.bind('<KeyRelease>', key_up)

  app = Application(root=root)
  app.main_proc()
  app.mainloop()

if __name__ == '__main__':
  main()
