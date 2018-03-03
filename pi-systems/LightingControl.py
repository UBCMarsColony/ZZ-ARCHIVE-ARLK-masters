import RPi.GPIO as GPIO
import time

lights = 0  # Lighting control on Pin D0
inner_door = 1  # Inner door open/closed sensor on Pin D1
outer_door = 2  # Inner door open/closed sensor on Pin D1
pir = 3  # Person in Room (PIR) sensor on Pin
gas = 4  # Gas pumps on/off sensor on Pin D3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(lights, GPIO.OUT)
GPIO.setup(inner_door, GPIO.IN)
GPIO.setup(outer_door, GPIO.IN)
GPIO.setup(pir, GPIO.IN)
GPIO.setup(gas, GPIO.OUT)

while 1:
    if GPIO.input(pir) or GPIO.input(gas):
        GPIO.output(lights, 1)

    elif GPIO.input(inner_door) and (GPIO.input(outer_door) == 0):
        GPIO.output(lights, 1)

    elif GPIO.input(outer_door) and (GPIO.input(inner_door) == 0):
        GPIO.output(lights, 1)

    elif GPIO.input(lights):
        lights_on = GPIO.wait_for_edge(pir, GPIO_RISING, timeout=30000)
        if lights_on is None:
            GPIO.output(lights, 0)


