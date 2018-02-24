#Stepper motor rotation angle function. Re
#Will use RPI.GPIO library for gpio control. 
#pin assignments using "broadcom numbers"

import RPI.GPIO as gpio
import time

#DECLARING CONSTANTS
pulPin_LOW=
dirPin_LOW=
enaPin_LOW=
sleepTime=0.04 #seconds
#motor properties
gearRatio=47 #gear ratio, we multiply angle gearRatio times to get wanted rotation

def main():
    
    #gpio pin setup routines
    gpio.setmode(gpio.BOARD)
    gpio.setup()

    motorMode='1000'
    rotateDirection='R'
    rotateAngle=90 #angle in degrees

while true:
    stepperAngularRotation(rotateAngle,motorMode,rotateDirection)
    time.sleep(5)
    stepperAngularRotation(-rotateAngle,motorMode,rotateDirection)

def stepperAngularRotation(angle,motorMode,direction):

    #library of possible motor drive rotation modes. Why anyone would use the bigger microsteps is beyond me, unless you really love slow rotation.
    #each DIP switch configuration(e.g. 0111), gives the # of rotation pulses needed to rotate the **motor** 360 degrees
    driverMode={'0111':400,'1011':800,'0011':1600,'1101':3200,'0101':6400,'1001':12800,'0001':25600,'1110':1000,'0110':2000,'1010':4000,'0010':5000,'1100':8000,'0100':10000,'1000':20000,'0000':25000}
    stepsToRev=int((angle/360)*driverMode[motorMode]*gearRatio) #cast float->int to nearest angle, error is negligible due to reduction gear

    #remember, we use low side switching; do not manipulate pinHIGH assignments
    for rotationIndex <= stepsToRev
        gpio.output(pulPin_LOW,gpio.LOW)
        time.sleep(sleepTime)
        gpio.output(pulPin_LOW,gpio.HIGH)
        time.sleep(sleepTime)

#motor on off power, takes string signal and disables if signal=='DISABLE', fails 'ENABLE'd
def motorOperation(signal)
    if signal=='DISABLE':
        gpio.output(enaPin_LOW,HIGH)
    else:
        gpio_output(enaPin_LOW,LOW)