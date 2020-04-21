import vlc
import os
import time
import datetime
import random
import pytube

def regsetup():
    print("ran setup")
    global alarmTimeHour
    global alarmTimeMin
    global wakeSounds
    global stopMusic
    alarmTimeHour = int(input("enter hour "))
    alarmTimeMin = int(input("enter minute "))
    

def alarmnoise():
    player = vlc.MediaPlayer("/home/gcullen/Downloads/BigYoshisLounge.mp4")
    def play():
        player.play()
    while(True):
        play()


def comparetime(alarmHour, alarmMinute):
    #datetime.time(now.hour, now.minute, now.second):
    while(True):
        now = datetime.datetime.now()
        x = now.strftime("%H:%M")
        y = '{}:{}'.format(alarmHour, alarmMinute)
        if alarmHour < 10:
            y = '0{}:{}'.format(alarmHour, alarmMinute)
        if alarmMinute < 10:
            y = '{}:0{}'.format(alarmHour, alarmMinute)
        if alarmMinute < 10 and alarmHour < 10:
            y = '0{}:0{}'.format(alarmHour, alarmMinute)
        if y == x:
            alarmnoise()
        else:
            time.sleep(60)

if __name__ == "__main__":
    try:
        regsetup()
        comparetime(alarmTimeHour, alarmTimeMin)
    except:
        print("Did you type in the time correctly?")
