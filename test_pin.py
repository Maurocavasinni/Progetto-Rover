#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Test porte - testa LED, motori, sensori IR e ultrasuoni

import RPi.GPIO as GPIO
import time

# Pin Configuration
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
IR_M = 22
IR_L = 27
IR_R = 18
TRIG = 17
ECHO = 4

# LED pins
LED0 = 10
LED1 = 9
LED2 = 25

# Setup porte
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

def test_led(led_pin, led_name):
    print('Testing %s (pin %d)...' % (led_name, led_pin))
    GPIO.output(led_pin, GPIO.LOW)  # Turn ON
    time.sleep(1.0)
    GPIO.output(led_pin, GPIO.HIGH)  # Turn OFF
    time.sleep(0.5)
    print('%s OK' % led_name)

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

def test_motor(motor_func, motor_name):
    print('Testing %s...' % motor_name)
    motor_func()
    time.sleep(0.5)
    motor_stop()
    time.sleep(0.5)
    print('%s OK' % motor_name)

def test_ir_sensor(ir_pin, ir_name):
    print('Testing %s (pin %d)...' % (ir_name, ir_pin))
    state = GPIO.input(ir_pin)
    if state:
        print('%s: Nessun ostacolo trovato (HIGH)' % ir_name)
    else:
        print('%s: Ostacolo trovato (LOW)' % ir_name)
    print('%s OK' % ir_name)

def test_ultrasonic():
    print('Testing Sensore Ultrasonico...')
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TRIG, GPIO.LOW)
    
    timeout_start = time.time()
    while not GPIO.input(ECHO):
        if time.time() - timeout_start > 0.1:
            print('Ultrasonic: Timeout - attesa avvio echo')
            return
    t1 = time.time()
    
    timeout_start = time.time()
    while GPIO.input(ECHO):
        if time.time() - timeout_start > 0.1:
            print('Ultrasonic: Timeout - echo non terminato')
            return
    t2 = time.time()
    
    distance = (t2 - t1) * 340 / 2
    print('Distanza percepita: %.3f m (%.1f cm)' % (distance, distance * 100))

def main():    
    setup_gpio()
    print('Setup GPIO completato\n')
    
    # Test LEDs
    print('--- Testing LED ---')
    test_led(LED0, 'LED0')
    test_led(LED1, 'LED1')
    test_led(LED2, 'LED2')
    print('')
    
    # Test Motors
    print('--- Testing Motori ---')
    time.sleep(2)
    test_motor(motor_forward, 'Avanti')
    test_motor(motor_backward, 'Indietro')
    test_motor(motor_turn_left, 'Sinistra')
    test_motor(motor_turn_right, 'Destra')
    print('')
    
    # Test IR Sensors
    print('--- Testing Sensori Infrarossi ---')
    test_ir_sensor(IR_M, 'Centrale')
    test_ir_sensor(IR_L, 'Sinistro')
    test_ir_sensor(IR_R, 'Destro')
    print('')
    
    # Test Ultrasonic
    print('--- Testing Sensore Ultrasonico ---')
    test_ultrasonic()
    print('')
    
    print('========================================')
    print('Fine Test')
    print('========================================')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nTest interrotto forzatamente')
    finally:
        motor_stop()
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.cleanup()
