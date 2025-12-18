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

# Collision avoidance
SAFE_DISTANCE = 0.50
DANGER_DISTANCE = 0.20
MAX_SPEED = 100
MEDIUM_SPEED = 60

pwm_ENA = None
pwm_ENB = None

logging.basicConfig(
    filename='rover_patrol.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_gpio():
    global pwm_ENA, pwm_ENB
    # Motor setup
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    pwm_ENA = GPIO.PWM(ENA, 1000)
    pwm_ENB = GPIO.PWM(ENB, 1000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

    # Sensor setup
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # LED setup
    GPIO.setup(LED0, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.HIGH)

def motor_forward(speed=MAX_SPEED):
    pwm_ENA.ChangeDutyCycle(speed)
    pwm_ENB.ChangeDutyCycle(speed)
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
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(0)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def piroettonj():
    print("Cambio direzione per ostacolo")
    motor_turn_left()
    time.sleep(2)
    motor_stop()

def led_sirena():
    print("Sirena LED attiva")
    GPIO.output(LED0, GPIO.HIGH)
    GPIO.output(LED2, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(LED2, GPIO.HIGH)
    GPIO.output(LED0, GPIO.LOW)
    time.sleep(0.5)

def collision_avoidance():
    distance = get_distance()
    
    if distance > SAFE_DISTANCE:
        return MAX_SPEED, False
    elif distance > DANGER_DISTANCE:
        return MEDIUM_SPEED, False
    else:
        return 0, True

def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TRIG, GPIO.LOW)
    
    timeout = time.time() + 0.5
    while not GPIO.input(ECHO):
        if time.time() > timeout:
            print("TIMEOUT: Echo non ricevuto")
            return 999
    t1 = time.time()
    
    timeout = time.time() + 0.5
    while GPIO.input(ECHO):
        if time.time() > timeout:
            print("TIMEOUT: Echo troppo lungo")
            return 999
    t2 = time.time()
    
    distance = (t2 - t1) * 340 / 2
    print("Distanza rilevata: {:.2f}m".format(distance))
    return distance

def where_to_go(d_l, d_c, d_r):
    max_distance = max(d_l, d_c, d_r)
    logging.info("Valutazione - L:{:.2f}m C:{:.2f}m R:{:.2f}m".format(d_l, d_c, d_r))

    if (max_distance == d_c):
        logging.info("Direzione presa: AVANTI")
    elif (max_distance == d_r):
        logging.info("Direzione presa: DESTRA")
        motor_turn_right()
        time.sleep(0.7)
    else:
        logging.info("Direzione presa: SINISTRA")
        motor_turn_left()
        time.sleep(0.7)

    start_time = time.time()
    duration = 1
    current_speed = 0
    
    while (time.time() - start_time) < duration:
        new_speed, need_stop = collision_avoidance()
        
        if need_stop:
            motor_stop()
            time.sleep(0.3)
            piroettonj()
            current_speed = 0
        elif new_speed != current_speed:
            motor_forward(new_speed)
            current_speed = new_speed
        
        time.sleep(0.1)

def loop_rover():
    print("Avvio pattugliamento...")
    while True:
        print("\n--- Scansione SINISTRA ---")
        motor_turn_left()
        time.sleep(0.7)
        distance_left = get_distance()
        print("--- Scansione CENTRO ---")
        motor_turn_right()
        time.sleep(0.7)
        distance_center = get_distance()
        print("--- Scansione DESTRA ---")
        motor_turn_right()
        time.sleep(0.7)
        distance_right = get_distance()
        motor_turn_left()
        time.sleep(0.7)

        where_to_go(distance_left, distance_center, distance_right)


if __name__ == '__main__':
    print("=== AVVIO ROVER ===")
    try:
        setup_gpio()
        time.sleep(2)
        loop_rover()
        
    except KeyboardInterrupt:
        print("\n=== ARRESTO ROVER ===")
    finally:
        motor_stop()
        if pwm_ENA:
            pwm_ENA.stop()
        if pwm_ENB:
            pwm_ENB.stop()
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.cleanup()
        logging.info("Rover arrestato")