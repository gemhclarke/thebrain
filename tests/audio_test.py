import time
import pygame
pygame.mixer.init()
pygame.mixer.music.load("../audio/alien_danger.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    time.sleep(.25)
