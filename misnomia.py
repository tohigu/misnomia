#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
import math
from neopixel import *
import argparse
from OSC import OSCServer
import numpy as np

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
pathra_state   = 1       # 0 => Standby 1 => speak TODO: 2 => listen 3 => unknown_fallback

#OSC handlers
def handle_speak(path, tags, args, source):
    #do cesar talking animation
    print('got pathra speak')
    global pathra_state
    pathra_state = 2

def handle_unknown(path, tags, args, source):
    #do cesar talking animation
    print('got pathra unknown')
    global pathra_state
    pathra_state = 3

def handle_listening_start(path, tags, args, source):
    #do cesar talking animation
    print('got pathra awoken')
    global pathra_state
    pathra_state = 1

def handle_listenin_end(path, tags, args, source):
    #do cesar talking animation
    print('got pathra speak')
    global pathra_state
    pathra_state = 1

def run_lights():
    global pathra_state
    fs = 1000
    #get millisecond part of cur. time in millis
    x = round(time.time() * fs) % fs
    f = pathra_state # Should come out as pulses per second
    # compute the value (amplitude) of the sin wave at the for each sample
    # given sample rate and frequency and current time (x)
    y = np.sin(2*np.pi*f * (x/fs))
    y = (y + 1) / 2
    #got amplitude, do lights
    light_amp = int(y * 255)
    print(light_amp)
    color = Color(0,light_amp,0) if pathra_state == 1 else Color(light_amp,light_amp,light_amp)
    color = Color(0,light_amp,light_amp) if pathra_state == 2 else Color(light_amp,light_amp,light_amp)
    color = Color(light_amp,light_amp,0) if pathra_state == 3 else Color(light_amp,light_amp,light_amp)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        # time.sleep(wait_ms/1000.0)
        # call user script
        each_frame()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# # Define functions which animate LEDs in various ways.
# def fadeInOutRed(strip, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     print('in red')
#     global pathra_state
#     pathra_state = 0
#     for i in range(3):
#         for z in range(255,10):
#             color = Color(0,z,0)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#         for y in range(255,0,-10):
#             color = Color(0,y,0)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#
#
# # Define functions which animate LEDs in various ways.
# def fadeInOutPurple(strip, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     print('in red')
#     global pathra_state
#     pathra_state = 0
#     for i in range(3):
#         for z in range(255,10):
#             color = Color(0,z,z)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#         for y in range(255,0,-10):
#             color = Color(0,y,y)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#
# # Define functions which animate LEDs in various ways.
# def fadeInOutYellow(strip, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     print('in red')
#     global pathra_state
#     pathra_state = 0
#     for i in range(3):
#         for z in range(255,10):
#             color = Color(z,z,0)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#         for y in range(255,0,-10):
#             color = Color(y,y,0)
#             for i in range(strip.numPixels()):
#                 strip.setPixelColor(i, color)
#                 strip.show()
#                 # time.sleep(wait_ms/1000.0)
#                 # call user script
#                 each_frame()
#
# def fadeInOutWhite(strip, wait_ms=1):
#     fadeInWhite(strip)
#     fadeOutWhite(strip)
#
# def fadeOutWhite(strip, wait_ms=1):
#     global pathra_state
#     print('out')
#     for y in range(255,0,-1):
#         ncolor = Color(y,y,y)
#         if pathra_state == 1:
#             fadeInOutRed(strip)
#         elif pathra_state == 2:
#             fadeInOutPurple(strip)
#         elif pathra_state == 3:
#             fadeInOutYellow(strip)
#         for j in range(strip.numPixels()):
#             strip.setPixelColor(j, ncolor)
#             strip.show()
#             # time.sleep(wait_ms/1000.0)
#             # call user script
#             each_frame()
#
# def fadeInWhite(strip, wait_ms=1):
#     global pathra_state
#     print('Fading white in')
#     for z in range(255):
#         color = Color(z,z,z)
#         if pathra_state == 1:
#             fadeInOutRed(strip)
#         elif pathra_state == 2:
#             fadeInOutPurple(strip)
#         elif pathra_state == 3:
#             fadeInOutYellow(strip)
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, color)
#             strip.show()
#             # time.sleep(wait_ms/1000.0)
#             # call user script
#             #print('before each frame white')
#             each_frame()
#
# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, color)
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)
#
# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)
#
# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
#
# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
#
# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args[2],args[0],1-args[1])

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True


# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    # while not server.timed_out:
    server.handle_request()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()
    server = OSCServer( ("localhost", 5005) )
    server.addMsgHandler( "/pathraspeak", handle_speak )
    server.addMsgHandler( "/unknown", handle_unknown )
    server.addMsgHandler( "/awoken", handle_listening_start )
    server.timeout = 0
    run = True

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    colorWipe(strip, Color(0,0,0), 10)

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    print('In main')
    try:

        # while True:
            # print ('Color wipe animations.')
            # colorWipe(strip, Color(255, 0, 0))  # Red wipe
            # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            # colorWipe(strip, Color(0, 0, 255))  # Green wipe
            # print ('Theater chase animations.')
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)


        # simulate a "game engine"
        while run:
            # global pathra_status
            # # do the game stuff:
            # if pathra_state == 1 :
            #     fadeInOutRed(strip)
            # if pathra_state == 2 :
            #     fadeInOutPurple(strip)
            # if pathra_state == 3 :
            #     fadeInOutYellow(strip)
            # elif pathra_state == 0:
            #     fadeInOutWhite(strip)
            run_lights()

	server.close()


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
