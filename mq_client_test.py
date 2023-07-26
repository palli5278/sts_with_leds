#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mq_client_test.py
#  
#  Copyright 2023  <rp@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import paho.mqtt.client as mqtt #import the client1
import time
import board
import neopixel_spi as neopixel
import signal
import sys

colour_pattern = 5
LED_COUNT = 12  # Number of LEDs in your external WS2812 LED ring
BRIGHTNESS = 1.0
PIXEL_ORDER = neopixel.GRB
DELAY = 0.1
NUM_PIXELS = 12
spi = board.SPI()
# Change D18 to the appropriate GPIO pin where your WS2812 LED ring is connected
pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False
)

color_green = [0x00,0xFF,0x00]
color_red = [255, 0x00, 0x00]
increment = 12

def green():
    global increment
    global color_green
    global LED_COUNT
    global BRIGHTNESS
    color_green[1] += increment

    if color_green[1] >= 255:
        color_green[1] = 255
        increment = -12

    if color_green[1] <= 0:
        color_green[1] = 0
        increment = 12

    # Fill the entire WS2812 LED ring with the same color
    for i in range(LED_COUNT):
        pixels[i] = tuple(color_green)

    pixels.show()
    time.sleep(0.01)         


def red():
    global increment
    global color_red
    global LED_COUNT
    global BRIGHTNESS
    color_red[0] += increment

    if color_red[0] >= 255:
        color_red[0] = 255
        increment = -12

    if color_red[0] <= 0:
        color_red[0] = 0
        increment = 12

    # Fill the entire WS2812 LED ring with the same color
    for i in range(LED_COUNT):
        pixels[i] = tuple(color_red)

    pixels.show()
    time.sleep(0.01)         
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(256):  # One full cycle of the color wheel
        for i in range(LED_COUNT):
            pixel_index = (i * 256 // LED_COUNT) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def leds_status(payload):
    global colour_pattern
    if payload == "rainbow":
        colour_pattern = 0
    elif payload == "red":
        colour_pattern = 1
    elif payload == "green":
        colour_pattern = 2
    else:
        colour_pattern = 3
        print("something else ",payload)
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    pay = str(message.payload.decode("utf-8"))
    leds_status(pay)
########################################


def main(args):
    global colour_pattern
    broker_address="127.0.0.1"
    #broker_address="iot.eclipse.org"
    print("creating new instance")
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic","metamorph/test/leds")
    client.subscribe("metamorph/test/leds")
    while True:
        if (colour_pattern == 1):
            red()
        elif(colour_pattern == 2):
            green()
        elif(colour_pattern == 0):
            rainbow_cycle(0)    
        else:
            print("colour:",colour_pattern)
            time.sleep(1)
            
        """
        match colour_pattern:
            case 1:
                red()
            case _:
                print("colour:",colour_pattern)
                time.sleep(1)
                """
    """
    print("Subscribing to topic","house/bulbs/bulb1")
    client.subscribe("house/bulbs/bulb1")
    print("Publishing message to topic","house/bulbs/bulb1")
    client.publish("house/bulbs/bulb1","OFF")
    time.sleep(4) # wait
    #client.loop_stop() #stop the loop
    """
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
