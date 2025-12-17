#!/usr/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import logging

SAFE_DISTANCE = 0.30
DANGER_DISTANCE = 0.15

# Motor pins
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

# Sensor pins
IR_M = 22
IR_L = 27
IR_R = 18
TRIG = 17
ECHO = 4

# LED pins
LED0 = 10
LED1 = 9
LED2 = 25

logging.basicConfig(
    filename='rover_patrol.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_gpio():
    # Motor setup
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    # Sensor setup
    GPIO.setup(IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # LED setup
    GPIO.setup(LED0, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.HIGH)

def motor_forward():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def motor_backward():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def motor_turn_left():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def motor_turn_right():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def motor_stop():
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def piroettonj():
    motor_turn_left()
    motor_turn_left()
    motor_turn_left()
    motor_turn_left()

    time.sleep(5)

def led_sirena(led_pin1, led_pin2):
    GPIO.output(led_pin2, GPIO.HIGH)
    GPIO.output(led_pin1, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(led_pin1, GPIO.HIGH)
    GPIO.output(led_pin2, GPIO.LOW)
    time.sleep(0.5)

def collision_avoidance():
    if GPIO.input(IR_M) == False:
        motor_stop()
    else:
        motor_forward()

def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TRIG, GPIO.LOW)
    
    while not GPIO.input(ECHO):
        pass
    t1 = time.time()
    
    while GPIO.input(ECHO):
        pass
    t2 = time.time()
    
    distance = (t2 - t1) * 340 / 2
    return distance

def loop_rover():
    while True:
        motor_turn_left()
        distance_left = get_distance()
        logging.info(f"Distanza sinistra: {distance_left:.2f}m")
        motor_turn_right()
        distance_center = get_distance()
        logging.info(f"Distanza centro: {distance_center:.2f}m")
        motor_turn_right()
        distance_right = get_distance()
        logging.info(f"Distanza destra: {distance_right:.2f}m")
        motor_turn_left()

        #TODO: Fix if
        if (distance_center > distance_left):
            if (distance_center > distance_right):
                motor_forward()
                time.sleep(1)
            else:
                motor_turn_right()
                motor_forward()
                time.sleep(1)
        else:
            motor_turn_left()
            motor_forward()
            time.sleep(1)

if __name__ == '__main__':
    try:
        setup_gpio()
        loop_rover()
        
    except KeyboardInterrupt:
        motor_stop()
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.cleanup()