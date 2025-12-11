#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

def checkdist():
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(17,GPIO.LOW)
    while not GPIO.input(4):
               pass
    t1 = time.time()
    while GPIO.input(4):
               pass
    t2 = time.time()
    return (t2-t1)*340/2
	
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)

#GPIO.setmode(GPIO.BCM)
########Definition of Motor Drive Interface #################
ENA = 13	#//L298 Enable A
ENB = 20	#//L298 Enable B
IN1 = 19	#//Motor interface1
IN2 = 16	#//Motor interface2
IN3 = 21	#//Motor interface3
IN4 = 26	#//Motor interface4

GPIO.setup(17,GPIO.OUT,initial=GPIO.LOW)#Ultrasound module transmitter pin settings
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)#Ultrasound module receiver pin settings
#########The motor is initialized to LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

time.sleep(2)
try:
         while True:
		ds = checkdist()
		if ds > 0.15:
			print 'Distance: %0.3f m' %ds
			Motor_Forward()
		else:
			Motor_Stop()
		time.sleep(0.1)
except KeyboardInterrupt:
         GPIO.cleanup()
