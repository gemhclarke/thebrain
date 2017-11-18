# ===================================================================
# Setup
# ===================================================================
from blinkstick import blinkstick
from time import sleep
bstick1 = blinkstick.find_first()
from mpu6050 import mpu6050
#from threading import Thread
import threading
import pygame
import os


# ===================================================================
# Functions
# ===================================================================

def leds_reset():

    print("Resetting LEDs")
    for led_number in range(8):
        bstick1.set_color( index=led_number, red=0, green=0, blue=0)


def leds_morph( colour, brightness ):

    # This function loops through all 8 LEDs checking the value of gyro_x on each loop. If gyro_x is 
    # outside of pre-defined range, the defense systems are called.

    for led_number in range(8):
        r,g,b = adjust_brightness( colour, brightness )

        if( (gyro_x > 30 or gyro_x < -30) or (gyro_y > 30 or gyro_y < -30) or (gyro_z > 30 or gyro_x < -30) ):
            print ("Emergency - gyroscope movement detected")
            emergencySoundThread = threading.Thread(target=play_emergency_sound)
            emergencySoundThread.start()
            leds_gyro_emergency()

        bstick1.morph( index=led_number, red=r, green=g, blue=b, duration=400, steps=30)


def leds_gyro_emergency():

    # Start the emergency LED pattern. We'll repeat 5 cycles but each time check the value of gyro_x and gyro_y
    # If these value are back in range we declare the emergency is over and reload the background sound and break the loop

    for count in range(5):
        for led_number in range(8):
            bstick1.morph( index=led_number, red=255, green=0, blue=0, duration=200, steps=30)

	sleep(0.0)

        for led_number in range(8):
            bstick1.morph( index=led_number, red=100, green=0, blue=0, duration=200, steps=30)

        if( (gyro_x < 30 and gyro_x > -30) and (gyro_y < 30 and gyro_y > -30) and (gyro_z < 30 and gyro_x > -30) ):
            print ("Emergency over, reverting back to normal mode")
	    backgroundSoundThread = threading.Thread( target=play_background_sound, args=() )
            backgroundSoundThread.start()
            break  


def adjust_brightness( colour, brightness ):
     
    # This function converts HEX to RGB and reduces each RGB value by the
    # same amount to act as a brightness control
    # The brightness argument can be anything from 0.1 to 255.0
     
    r,g,b = bstick1._hex_to_rgb( colour ) 
    r = r * (brightness/100)
    g = g * (brightness/100)
    b = b * (brightness/100)
    return(r,g,b)


def play_emergency_sound():
    print("Playing emergency sound")
    pygame.mixer.init()
    pygame.mixer.music.load("audio/alien_danger.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        sleep(.25)


def play_background_sound():
    print("Starting background sound thread" )
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print("Playing background sound")
        pygame.mixer.init()
        pygame.mixer.music.load("audio/buzzer.wav")

        while True:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                sleep(.25)
    print( "Stopping background sound thread" )


def monitor():
    print("Starting gyroscope monitor")
    global gyro_x
    global gyro_y
    global gyro_z
    sensor = mpu6050(0x68)
    while True:
        gyro_data = sensor.get_gyro_data()
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']
        gyro_z = gyro_data['z']
        #print ("Gyro data is: " + str(gyro_x) + " " + str(gyro_y) + " " + str(gyro_z) )
        sleep(0.6)

      

# ===================================================================
# Main program 
# ===================================================================

# Start the giroscope and accelerometer monitoring
giroThread = threading.Thread( target=monitor, args=() )
giroThread.start()

# Start the background sound
bst = threading.Thread( target=play_background_sound, args=() )
bst.start()

# Reset all the LED's
leds_reset()

# Start "rest" mode by looping though some LED patterns continually 
while True:
    leds_morph("#00ff84", 100.0)
    leds_morph("#ffffff", 100.0)
    leds_morph("#00ff84", 100.0)
