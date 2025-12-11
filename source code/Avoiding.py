#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

def	Avoiding():# Infrared obstacle avoidance function
	if GPIO.input(IR_M) == False:
		Motor_Stop()
	else:
		Motor_Forward()
	
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
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

#Pin type setting
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
######## Definition of Motor Drive Interface#################
ENA = 13	#//L298 Enable A
ENB = 20	#//L298 Enable B
IN1 = 19	#//Motor interface1
IN2 = 16	#//Motor interface2
IN3 = 21	#//Motor interface3
IN4 = 26	#//Motor interface4
########Definition of Infrared Sensor Interface #################

IR_M = 22	#The middle avoid obstacles infrared of the car


#########The motor is initialized to LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
#########Infrared is initialized as input and internally pulled high#########

GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)


time.sleep(2)
try:
		while True:
			Avoiding()
			time.sleep(0.1)
except KeyboardInterrupt:
         GPIO.cleanup()
