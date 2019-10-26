# -*- coding: utf-8 -*
# Software PWM Servo.py

import RPi.GPIO as GPIO
import time

P_SERVO = 25 # GPIO端口号，根据实际修改
fPWM = 50  # Hz (软件PWM方式，频率不能设置过高)
a = 12.5
b = 2.5

def setup():
    global pwm
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_SERVO, GPIO.OUT)
    pwm = GPIO.PWM(P_SERVO, fPWM)
    pwm.start(0)

def setDirection(direction):
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print "direction =", direction, "-> duty =", duty
    time.sleep(1) 
   
def duoji():
    print "starting"
    #setup()
    for direction in range(0, 61, 20):
        setDirection(direction)
    direction = 0
    setDirection(0)
    #GPIO.cleanup()
    print "done"

