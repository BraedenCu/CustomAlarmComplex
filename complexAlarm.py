import vlc
from gtts import gTTS
import os
import time
import datetime
import random
import serial
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_vcnl4010
import pafy
import threading

def regsetup():
    print("ran setup")
    global alarmTime
    global wakeSounds
    global sensor
    global i2c
    global dist
    global stopMusic
    alarmTime = int(input("enter wake up time eg. 6, 15 for 6:25 "))
    wakeSounds = input("what do you want me to say? ")
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_vcnl4010.VCNL4010(i2c)
    dist = sensor.proximity
    stopMusic = False
    
def serialSetup():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM1'
    print("connected to: " + ser.portstr)
    count=1
    

def alarmnoise():

    #this is for playing a lofi track on youtube
    url = "https://www.youtube.com/watch?v=5qap5aO4i9A"
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)

    #need it to play asynchronously (probs. spelled that wrong)
    def play():
        while(stopMusic==False):
            player.play()

    thr = threading.Thread(target=play, args=(), kwargs={})
    thr.start()

    #this is for sending user input wakeup messages 
    '''
    #get wait time based on number of chars in string
    length = len(wakeSounds)
    times = length / 5 
    x = random.randint(0, 12)
    accents = {0: 'zh-cn', 1: 'en-uk', 2: 'en', 3: 'en-ph', 4: 'en-ng', 5: 'ru', 6: 'es-us', 7: 'es-es', 8: 'en-gb', 9: 'sw', 10: 'zh-cn', 11: 'nl', 12: 'da'}
    language = accents[x]
    tts = gTTS(wakeSounds, lang=language)
    tts.save('hello.mp3')
    p = vlc.MediaPlayer("file:///home/gcullen/hello.mp3")
    p.play()
    time.sleep(int(times))
    p.stop()
    '''
    waterRelease()

def waterRelease():
    time.sleep(10)
    if sensor.proximity < dist:
        kit = ServoKit(channels=16)
        kit.continuous_servo[0].throttle = 0.5
        print("omg water")
    else:
        stopMusic=True

def comparetime(alarmHour):
    #datetime.time(now.hour, now.minute, now.second):
    while(True):
        now = datetime.datetime.now()
        if alarmHour == datetime.time(now.hour):
            alarmnoise()
        else:
            #time.sleep(60)
            alarmnoise()

if __name__ == "__main__":
    try:
        regsetup()
        #serialSetup()
        comparetime(alarmTime)
    except:
        print("Did you type in the time correctly?")
