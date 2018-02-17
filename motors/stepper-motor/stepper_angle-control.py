#Stepper motor rotation angle function. Re
#Will use RPI.GPIO library for gpio control. 
#pin assignments using "broadcom numbers"

import RPI.GPIO as gpio
include time
def main():
    rotationAngle=90 #angle in degrees
    motorMode='1000'
    gpio.setmode(gpio.BOARD)
    stepperAngularRotation(rotationAngle,motorMode)

def stepperAngularRotation(angle,motorMode):
    driverMode={'0111':400,'1011':800,'0011':1600,'1101':3200,'0101':6400,'1001':12800,'0001':25600,'1110':1000,'0110':2000,'1010':4000,'0010':5000,'1100':8000,'0100':10000,'1000':20000,'0000':25000}
    stepsToRev=(angle/360)*driverMode[motorMode]
    
    
    
