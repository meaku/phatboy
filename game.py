#!/usr/bin/env python

import time
import os
import pygame
import glob

DRUM_FOLDER = "drums2"

BANK = os.path.join(os.path.dirname(__file__), DRUM_FOLDER)

pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)

files = glob.glob(os.path.join(BANK, "*.wav"))
files.sort()
samples = [pygame.mixer.Sound(f) for f in files]


import unicornhat as unicorn

import drumhat

def hit_handler(event):
  jump()
  global hearts
  if hearts < 0:
    hearts=3

def reset():
  print("reset")
  global hearts
  hearts=3
  global speed
  speed=0.5
  global counter
  counter=0
  global score
  score=1

drumhat.on_hit(1, reset)

drumhat.on_hit(8, hit_handler)

score=1
counter=0
up=1
lastjump=counter
speed=0.5
hearts=3
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.2)
width,height=unicorn.get_shape()

def tempo():
  global speed
  if counter == 7:
    speed=0.925*speed

def sky():
  for y in range(height):
    for x in range(width):
      unicorn.set_pixel(x,y,50,100,255)

def ground():
  for x in range(width):
    unicorn.set_pixel(x,0,0,255,0)

def enemy(x):
  unicorn.set_pixel(x,1,255,255,255)

def player(y):
  unicorn.set_pixel(6,y,255,0,0)

def jump():
  global up
  print("jump")
  samples[2].play(loops=0)

  up=2
  global lastjump
  if lastjump == counter-1:
    up=1
  else:
    lastjump=counter

def life():
  global hearts
  if counter == 7 and up == 1:
    hearts=hearts-1

def dead():
  if hearts < 1:
    print("death")
    for x in range(width):
      for y in range(height):
        unicorn.set_pixel(x,y,255,0,0)
    unicorn.show()
    while hearts == 0:
      time.sleep(1)

def hp():
  if hearts == 3:
    unicorn.set_pixel(0,3,255,0,0)
    unicorn.set_pixel(1,3,255,0,0)
    unicorn.set_pixel(2,3,255,0,0)
  if hearts == 2:
    unicorn.set_pixel(0,3,255,0,0)
    unicorn.set_pixel(1,3,255,0,0)
  if hearts == 1:
    unicorn.set_pixel(0,3,255,0,0)

while True:
  tempo()
  sky()
  ground()
  player(up)
  enemy(counter)
  counter=counter+1
  if counter > 7:
    counter=0
    print(score, hearts)
    if(hearts > 0):
      score=score+1
  life()
  dead()
  hp()
  unicorn.show()
  up=1
  time.sleep(speed)


