#coding:utf-8
import pyaudio
import wave
from baidu_speech_api import BaiduVoiceApi
import json
import signal
import sys
import serial
import threading
import base64
import RPi.GPIO as GPIO
import os
import re
import thread
import socket
import requests
from aip.speech import AipSpeech

from urllib2 import Request, urlopen, URLError, HTTPError
import time
from pixels import Pixels, pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

from pwm1 import duoji,setup
from sort import sort

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 512
RECORD_SECONDS = 2
#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
#WAVE_OUTPUT_FILENAME = "output.wav"

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
p = None
stream = None
try:
    p = pyaudio.PyAudio()
    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                start=False)
except:
    pass

APP_ID = '11674925'
API_KEY = 'XATnBiP0mO9SYUSAPyrryPHP'
SECRET_KEY = '3Xk0pPNgsRkkRfRLOL2K5PGpFZ2jEMvr'
boolWaterlight = 0

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)

def generator_list(list):
    for l in list:
        yield l

def record():
    try:
        stream.start_stream()
        print("* recording")
        frames = []
        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except:
                pass
        print("* done recording")
        stream.stop_stream()
        print("start to send to baidu")
        # audio_data should be raw_data
        text = baidu.server_api(generator_list(frames))
        if text:
            try:
                text = json.loads(text)
                for t in text['result']:
                    print(t)
                    return(t)
            except KeyError: 
                return("get nothing")
        else:
            print("get nothing")
            return("get nothing")
    except:
        pass

def sigint_handler(signum, frame):
    stream.stop_stream()
    stream.close()
    p.terminate()
    print ('catched interrupt signal!')
    sys.exit(0)

def takePhoto():
    os.system('raspistill -t 500 -o imgs/test.jpg')
    
def getAPI():
    url = 'http://api.tianapi.com/txapi/imglajifenlei/'

    f = open(r'imgs/test.jpg', 'rb')
    encode = base64.b64encode(f.read())
    f.close()

    body = {
        "key": "ce06af298c5c6bcaecf0f05fc1253629",
        "img": str(encode)
    }
    headers = {'content-type': "application/x-www-form-urlencoded"}

    response = requests.post(url, data=body, headers=headers)
    '''
    if response.status_code == 200:
        print(response.text)
    else:
        raise Exception
    '''
    jsonStr = response.text
    print(jsonStr)
    jsonRes = json.loads(jsonStr)
    lajitip = ''
    try:
        lajitip = jsonRes['newslist'][0]['lajitip']
        lajitip = lajitip.encode('utf8')
    except:
        print('lajitip Error')
    'print(lajitip)'
    '''
    利用正则匹配垃圾类型
    '''
    reStr = '(?<=是).*垃圾'
    print(type(lajitip))
    result = re.findall(reStr,lajitip)
    print(result)
    if not len(result) == 0 :
        print(result[0])
        result[0] = result[0].decode('utf8')
        if result[0] == u'可回收垃圾':
            #ser.write('1'.encode())
            print('ser write 1')
        elif esult[0] == u'干垃圾':
            #ser.write('2'.encode())
            print('ser write 2')
        elif esult[0] == u'厨余垃圾':
            #ser.write('3'.encode())
            print('ser write 3')
        elif esult[0] == u'有毒有害垃圾':
            #ser.write('4'.encode())
            print('ser write 4')
    else:
        print('dao qi')
        #raise Exception

#########################################


def send2Server():
    IP = '47.98.42.12'
    port = 10002
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((IP,port))
        print('connect')
        client.send(b'111111')
    except:
        pass

def cameraSendServer():
    takePhoto()
    getAPI()
    send2Server()

def main():
    # 注册ctrl-c中断
    signal.signal(signal.SIGINT, sigint_handler)
    pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
    #ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    #thread.start_new_thread(thread_water, ())

    #trash_recycle = [u'塑料瓶',u'玻璃杯',u'纸箱']
    #trash_wet = [u'树叶', u'果皮', u'剩饭']
    #trash_dry = [u'骨头', u'陶瓷', u'餐具']
    #trash_harmful = [u'电池', u'灯泡', u'化妆品']
    signal_start = 0

    setup()
    # start serial thread
    
    while True:
        try:
            #if  str(ser.read(5))== '1':
             #   thr = threading.Thread(target=cameraSendServer)
              #  thr.start()
               # thr.join()

            time.sleep(1)
            outputtext = record()
            outputtext = outputtext.replace(u'。',u'')
            
            if signal_start == 1 and sort(outputtext) == u'可回收垃圾':
    #        if outputtext in trash_recycle and signal_start == 1:
               # boolWaterlight = 0
             #   ser.write('1'.encode())
                os.system("sudo mpg123 recycle.mp3")
               # data =[255,255,255] * 3
                #pixels.show(data)
                signal_start = 0
                #duoji()

            elif signal_start == 1 and sort(outputtext) == u'干垃圾':
              #   ser.write(b'2')
                 #boolWaterlight = 0
                 os.system("sudo mpg123 dry.mp3")
                 #data =[255,0,0] * 3
                 #pixels.show(data)
                 signal_start = 0
                 #duoji()
                        
            #elif outputtext in trash_wet and signal_start == 1:
            elif signal_start == 1 and sort(outputtext) == u'厨余垃圾':
               #  ser.write(b'3')
                 #boolWaterlight = 0       
                 os.system("sudo mpg123 wet.mp3")
                 #data =[0,255,0] * 3
                 #pixels.show(data)
                 signal_start = 0
                 #duoji()

            #elif outputtext in trash_harmful and signal_start == 1:
            elif signal_start == 1 and sort(outputtext) == u'有毒有害垃圾':
                # ser.write(b'4')
                 signal_start = 0
                 os.system("sudo mpg123 harmful.mp3")
                 #boolWaterlight = 1
                 #data =[0,0,255] * 3
                 #duoji()
                
            elif (u'垃圾') in outputtext:
                 signal_start = 1
                # boolWaterlight = 0
                 os.system("sudo mpg123 start.mp3")
                 #pixels.off()
                 
            elif signal_start == 1: 
                os.system("sudo mpg123 repeat.mp3")
                
            elif (u'闭嘴') in outputtext:
                exit(1)
                    
                
        except KeyError: 
            stream.close()
            p.terminate()
            GPIO.cleanup()


if __name__ == '__main__':
    main()


