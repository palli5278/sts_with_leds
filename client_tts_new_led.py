#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client_tts_new_led.py
#  
#  Copyright 2023 root <root@raja-Inspiron-N5110>
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

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import re
import requests
import os
import json
from gtts import gTTS
import subprocess
import time, threading

#from TTS.api import TTS

topics = ["metamorph/test/tts"]
topics_freeze = ["metamorph/test/freeze"]
#url = "https://534a-122-171-21-59.ngrok-free.app/talktofriend"
url = "http://20.74.172.80:5000/api/talktofriend"
cmd = "gtts-cli \"That sounds like a wonderful experience! It's always special to reconnect with someone who had a significant impact on your life, especially a teacher who inspired a love for a subject.\" | mpg123 -"

com_start = "gtts-cli \""
com_str = "That sounds like a wonderful experience! It's always special to reconnect with someone who had a significant impact on your life, especially a teacher who inspired a love for a subject."
com_end = "\" | mpg123 -"

u_flag_freeze = False

# The following is a multilingual model
#model_name = "tts_models/multilingual/multi-dataset/your_tts"
# Init TTS
#tts = TTS(model_name)
broker_address = "127.0.0.1"
broker_port = 1883

def foo():
    #print(time.ctime())
    global u_flag_freeze
    if(u_flag_freeze == False):
        publish.single("metamorph/test/freeze", "unfreeze", hostname="127.0.0.1")
    else:
        print(time.ctime())
    threading.Timer(3, foo).start()



def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    for line in proc_stdout.decode().split('\n'):
        print (line)
        #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))
    json_text=json.loads(message.payload)
    global u_flag_freeze
    """if (u_flag_freeze == False):
        u_flag_freeze = True
        metamorph_cloud(json_text)
    else:
        print("skip")"""
    if message.topic == "metamorph/test/freeze":
        if message.payload == b"freeze":
            u_flag_freeze = True
        elif message.payload == b"unfreeze":
            u_flag_freeze = False
        return 
    if not u_flag_freeze:
        u_flag_freeze = True
        metamorph_cloud(json_text)
    else:
        print("skip")    

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("my-topic")
def on_message(client, userdata, msg):
    print(f"Message received [{msg.topic}]: {msg.payload}")


def metamorph_cloud(json_text):
    global broker_address
    global broker_port
    global u_flag_freeze
    if json_text:
        #publish.single("metamorph/test/leds","red", hostname="127.0.0.1")
        publish.single("metamorph/test/leds", "red", hostname=broker_address, port=broker_port)
    response = requests.post(url, json=json_text)
    # Check the response status code
    if response.status_code == 200:
        json_response = response.json()
        if 'error' in json_response:
            print('Error posting data: {}'.format(json_response['error']))
            #text_speech=pyttsx3.init()
            answer = "something wrong! could you please try again?"
            #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")
            #text_speech.say(answer)
            #text_speech.runAndWait()
            #tts.tts_to_file(text=answer, speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")
            #os.system(" aplay output.wav")
        else:
            print(response.text)
            #print(type(response.text))
            json_res=json.loads(response.text)
            json_val=json_response["responsetext"]
            if json_val:
                #publish.single("metamorph/test/leds", "rainbow", hostname="127.0.0.1")
                publish.single("metamorph/test/leds", "rainbow", hostname=broker_address, port=broker_port)
            #text_speech=pyttsx3.init()
            #answer=json_val["text"]
            #text_speech.say(answer)
            #text_speech.runAndWait()
            # Text to speech to a file
            #tts.tts_to_file(text=json_val, speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")
            #os.system("aplay output.wav")
            #ret = subprocess.run(cmd, capture_output=True, shell=True)
            cmd = com_start + json_val +  com_end
            if cmd:
                #publish.single("metamorph/test/leds", "green", hostname="127.0.0.1")
                publish.single("metamorph/test/leds", "green", hostname=broker_address, port=broker_port)
            #subprocess_cmd(cmd)
            ret = subprocess.run(cmd, capture_output=True, shell=True)
            print(ret.stdout.decode())
            #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")
            print('Data posted successfully')
            u_flag_freeze = False
            #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")
    else:
        print('Error posting data: {}'.format(response.content))
        answer = "Oh no! I may be offline."
        #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")
        #text_speech=pyttsx3.init()
        #text_speech.say(answer)
        #text_speech.runAndWait()
        # Text to speech to a file
        #tts.tts_to_file(text=answer, speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")
        #os.system(" aplay output.wav")

def main(args):
    
    #m = subscribe.simple(topics, hostname="192.168.219.107", retained=False, msg_count=1)
    #print(m)
    foo()
    subscribe.callback(print_msg, topics, hostname="127.0.0.1")
    #publish.single("metamorph/test/freeze", "unfreeze", hostname="192.168.219.107")
    """
    for a in m:
        print(a.topic)
        print(a.payload)
    """
    """
    client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
    client.on_connect = on_connect
    client.on_message = on_message
    #client.username_pw_set("myusername", "aeNg8aibai0oiloo7xiad1iaju1uch")
    client.connect('127.0.0.1', 1883)
    client.loop_forever()  # Start networking daemon
    """

    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
