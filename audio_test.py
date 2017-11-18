import time
import pygame
pygame.mixer.init()
pygame.mixer.music.load("audio/buzzer.wav")

for count in range (5):
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
    time.sleep(.25)
