#!/usr/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import logging

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor pins
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

# Sensor pins
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
    time.sleep(2)

def led_sirena(led_pin1, led_pin2):
    GPIO.output(led_pin2, GPIO.HIGH)
    GPIO.output(led_pin1, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(led_pin1, GPIO.HIGH)
    GPIO.output(led_pin2, GPIO.LOW)
    time.sleep(0.5)

# Stare sempre a 20 cm di distanza, il sensore IR vede ostacoli a pochi centimetri (~2cm)
def collision_avoidance():
    if GPIO.input(IR_M) == False:
        motor_stop()
        motor_backward()
        time.sleep(0.5)
        piroettonj()

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

def where_to_go(d_l, d_c, d_r):
    max_distance = max(d_l, d_c, d_r)
    logging.info("Valutazione - L:{:.2f}m C:{:.2f}m R:{:.2f}m".format(d_l, d_c, d_r))

    if (max_distance == d_l):
        logging.info("Direzione presa: SINISTRA")
        motor_turn_left()
        time.sleep(0.7) 
        motor_forward()
    elif (max_distance == d_r):
        logging.info("Direzione presa: DESTRA")
        motor_turn_right()
        time.sleep(0.7) 
        motor_forward()
    else:
        logging.info("Direzione presa: AVANTI")
        motor_forward()

    start_time = time.time()
    duration = 1
    
    while (time.time() - start_time) < duration:
        collision_avoidance()
        time.sleep(0.1)

def loop_rover():
    while True:
        motor_turn_left()
        time.sleep(0.7)
        distance_left = get_distance()
        motor_turn_right()
        time.sleep(0.7)
        distance_center = get_distance()
        motor_turn_right()
        time.sleep(0.7)
        distance_right = get_distance()
        motor_turn_left()
        time.sleep(0.7)

        where_to_go(distance_left, distance_center, distance_right)


if __name__ == '__main__':
    try:
        setup_gpio()
        time.sleep(2)
        loop_rover()
        
    except KeyboardInterrupt:
        print('\nRover interrotto forzatamente.\n')
    finally:
        motor_stop()
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.cleanup()
        logging.info("Rover arrestato")