#! /usr/bin/python
# -*- coding:utf-8 -*-

# Combina ultrasuoni e infrarossi per una navigazione autonoma più sofisticata,
# con movimento casuale quando trova ostacoli.

# Caratteristiche della nuova funzionalità:
# Multi-sensore: Combina ultrasuoni (distanza precisa) e infrarossi (rilevamento rapido)
# 3 Zone di sicurezza:
# - Zona sicura (>30cm): avanti normale
# - Zona warning (15-30cm): rallentamento e manovre caute
# - Zona pericolo (<15cm): stop immediato e retromarcia

# Strategie di evitamento intelligenti:
# Retromarcia quando troppo vicino
# Curve casuali per varietà di movimento
# Preferenza di svolta basata sui sensori laterali

# Feedback visivo LED:
# LED spenti = tutto OK
# LED1 acceso = warning
# LED1+2 = pericolo
# Tutte accese = ostacolo IR rilevato

# Gestione errori: KeyboardInterrupt per stop sicuro

import RPi.GPIO as GPIO
import time
import random

# Pin Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

######## Motor Drive Interface #################
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26

######## Sensors Interface #################
IR_M = 22    # Middle infrared sensor
IR_L = 27    # Left infrared sensor
IR_R = 18    # Right infrared sensor
TRIG = 17    # Ultrasonic trigger
ECHO = 4     # Ultrasonic echo

######## LED Interface #################
LED0 = 10    # Headlight
LED1 = 9     # Status LED 1
LED2 = 25    # Status LED 2

######## Motor Setup #################
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

######## Sensor Setup #################
GPIO.setup(IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

######## LED Setup #################
GPIO.setup(LED0, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LED1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LED2, GPIO.OUT, initial=GPIO.HIGH)

# Constants
SAFE_DISTANCE = 0.30  # 30cm safe distance
DANGER_DISTANCE = 0.15  # 15cm danger zone

def Motor_Forward():
    """Move robot forward"""
    print('Moving Forward')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def Motor_Backward():
    """Move robot backward"""
    print('Moving Backward')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def Motor_TurnLeft():
    """Turn robot left"""
    print('Turning Left')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def Motor_TurnRight():
    """Turn robot right"""
    print('Turning Right')
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def Motor_Stop():
    """Stop all motors"""
    print('Stopping')
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def Get_Distance():
    """Measure distance using ultrasonic sensor"""
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

def LED_Status(status):
    """Control LED indicators based on robot status
    0 = All clear (all OFF)
    1 = Warning (LED1 ON)
    2 = Danger (LED1 + LED2 ON)
    3 = Obstacle detected (All ON)
    """
    if status == 0:  # All clear
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
    elif status == 1:  # Warning
        GPIO.output(LED0, GPIO.LOW)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.HIGH)
    elif status == 2:  # Danger
        GPIO.output(LED0, GPIO.LOW)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
    elif status == 3:  # Obstacle IR detected
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.HIGH)

def Smart_Patrol():
    """
    Smart patrol mode with multi-sensor obstacle avoidance
    - Uses ultrasonic for distance measurement
    - Uses infrared sensors for close obstacle detection
    - Implements random turn strategy when obstacle detected
    - LED indicators show robot status
    """
    print('\n=== Smart Patrol Mode Started ===')
    
    while True:
        # Get ultrasonic distance
        distance = Get_Distance()
        
        # Check infrared sensors
        ir_middle = GPIO.input(IR_M)
        ir_left = GPIO.input(IR_L)
        ir_right = GPIO.input(IR_R)
        
        # Decision logic
        if ir_middle == False:
            # Immediate obstacle detected by IR
            print('!!! IR Obstacle Detected - Emergency Stop')
            LED_Status(3)
            Motor_Stop()
            time.sleep(0.5)
            
            # Back up
            Motor_Backward()
            time.sleep(0.8)
            Motor_Stop()
            
            # Random turn to avoid obstacle
            turn_direction = random.choice(['left', 'right'])
            turn_duration = random.uniform(0.5, 1.5)
            
            if turn_direction == 'left':
                Motor_TurnLeft()
            else:
                Motor_TurnRight()
            time.sleep(turn_duration)
            Motor_Stop()
            
        elif distance < DANGER_DISTANCE:
            # Very close obstacle by ultrasonic
            print('!!! Danger Zone: %0.2f m' % distance)
            LED_Status(2)
            Motor_Stop()
            time.sleep(0.3)
            
            # Back up
            Motor_Backward()
            time.sleep(0.5)
            Motor_Stop()
            
            # Smart turn based on side sensors
            if ir_left == False and ir_right == True:
                print('Obstacle on left, turning right')
                Motor_TurnRight()
                time.sleep(1.0)
            elif ir_right == False and ir_left == True:
                print('Obstacle on right, turning left')
                Motor_TurnLeft()
                time.sleep(1.0)
            else:
                # Random turn
                if random.random() > 0.5:
                    Motor_TurnLeft()
                else:
                    Motor_TurnRight()
                time.sleep(random.uniform(0.7, 1.2))
            Motor_Stop()
            
        elif distance < SAFE_DISTANCE:
            # Warning distance
            print('Warning: %0.2f m - Slowing down' % distance)
            LED_Status(1)
            
            # Slow approach or slight turn
            if ir_left == False:
                Motor_TurnRight()
                time.sleep(0.3)
            elif ir_right == False:
                Motor_TurnLeft()
                time.sleep(0.3)
            else:
                Motor_Forward()
                time.sleep(0.2)
            Motor_Stop()
            
        else:
            # All clear - move forward
            print('All clear: %0.2f m' % distance)
            LED_Status(0)
            Motor_Forward()
        
        time.sleep(0.1)

# Main execution
if __name__ == '__main__':
    try:
        # Turn on headlight
        GPIO.output(LED0, GPIO.LOW)
        print('Initializing Smart Patrol System...')
        time.sleep(2)
        
        Smart_Patrol()
        
    except KeyboardInterrupt:
        print('\n\nProgram stopped by user')
        Motor_Stop()
        GPIO.output(LED0, GPIO.HIGH)
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.cleanup()
        print('GPIO cleaned up. Goodbye!')