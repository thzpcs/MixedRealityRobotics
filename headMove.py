# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:03:32 2018

@author: Skyler
"""

import urllib2 as ur

import argparse
import motion
from naoqi import ALProxy
from time import sleep
import sys

def main():
    
	# Initializes the robot
    robotIP = '169.254.129.162'
    PORT = 9559
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    
    
	# Constants for using motionProxy
    frame        = motion.FRAME_ROBOT
    isAbsolute   = True
    useSensorValues = True
    isEnabled = True
    
    # Wake up robot
    motionProxy.wakeUp()
    postureProxy.goToPosture("Crouch", 0.4)
    motionProxy.wbEnableEffectorControl("Head", isEnabled)

# Main loop
    while True:
        
		# Pulls information from the Unity server and converts it
        content = (ur.urlopen("http://127.0.0.1:5000").read())
        
        x,y,z = content.split(' ')
        
        headCoords = [float(z)*(3.14159/180),
					  float(x)*(3.14159/180),
                      float(y)*(3.14159/180)]

        for x in range(3):
            if headCoords[x] > 3.14159:
                headCoords[x] = headCoords[x] - (2*3.14159)

		headCoords[2] = -headCoords[2]
		headCoords[0] = -headCoords[0]
		
        # Rotates the head
        motionProxy.wbSetEffectorControl("Head", headCoords)
        sleep(0.2)

if __name__ == "__main__":

	main()
	