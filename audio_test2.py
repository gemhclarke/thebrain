# ===================================================================
# Setup
# ===================================================================
from time import sleep
import sys, termios, tty, os, pygame, threading

# ===================================================================
# Functions
# ===================================================================

def play_emergency_sound():
    print("Playing emergency sound. There are " + str( threading.active_count() ) + " threads active")
    while getattr(emergency_sound_thread, "do_run", True):
        pygame.mixer.init()
        pygame.mixer.Channel(0).play( pygame.mixer.Sound('audio/alien_danger.wav') )
        while pygame.mixer.Channel(0).get_busy() == True:
            sleep(.25)
    print( "Stopping emergency sound" )


def play_background_sound():
    print("Playing background sound. There are " + str( threading.active_count() ) + " threads active")
    while getattr(background_sound_thread, "do_run", True):
        pygame.mixer.init()
        pygame.mixer.Channel(1).play( pygame.mixer.Sound('audio/buzzer.wav') )
        while pygame.mixer.Channel(1).get_busy() == True:
            sleep(.25)
    print( "Stopping background sound" )


def get_keypress():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


# ===================================================================
# Main program 
# ===================================================================


while True:
    key = get_keypress()

    if (key == "0"):
        print("Exiting!")
        exit(0)
 
    if (key == "1"):
        print("1 pressed")
        global background_sound_thread
        background_sound_thread = threading.Thread( target=play_background_sound, args=() )
        background_sound_thread.start()

    if (key == "2"):
        print("1 pressed")
        global emergency_sound_thread
        emergency_sound_thread = threading.Thread( target=play_emergency_sound, args=() )
        emergency_sound_thread.start()

    if (key == "z"):
        print("z pressed")
        background_sound_thread.do_run = False

    if (key == "x"):
        print("x pressed")
        emergency_sound_thread.do_run = False
