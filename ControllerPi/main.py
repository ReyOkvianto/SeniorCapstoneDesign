import cv2
import numpy as np
from datetime import datetime
from gpiozero import Button
from time import sleep
from ControllerButtons import ControllerButtons
from LoRaController import LoRaController
from threading import *

# setting up
# ScreenshotIn = 18
# RecordIn = 23
# UpIn = 24
# DownIn = 25
# LightsIn = 21
# Active_State = False
# Previous_State = Button(1)

# Create Controller Button
Buttonz = ControllerButtons(18, 23, 24, 25, 21)
ScreenshotButton = Buttonz.ScreenshotButton
RecordButton = Buttonz.RecordButton
UpButton = Buttonz.UpButton
DownButton = Buttonz.DownButton
LightsButton = Buttonz.LightsButton

loraController = LoRaController()

thread = Thread(target=loraController.standby_mode, args=(Buttonz.GetCommand,))
thread.start()


while(True):
    ret, frame = Buttonz.cap.read()

    if ret == True: 

        # Write the frame into the file 'output.avi'
        if (Buttonz.out != None):
            Buttonz.out.write(frame)

        # Display the resulting frame    
        cv2.imshow('frame',frame)
        
        pressedKey = cv2.waitKey(1) & 0xFF
        
        Buttonz.Pressed(ScreenshotButton, frame=frame)
        Buttonz.Released(ScreenshotButton)
        
        Buttonz.Pressed(RecordButton)
        Buttonz.Released(RecordButton)
        
        Buttonz.Pressed(UpButton)
        Buttonz.Released(UpButton)
        
        Buttonz.Pressed(DownButton)
        Buttonz.Released(DownButton)
        
        Buttonz.Pressed(LightsButton)
        Buttonz.Released(LightsButton)

        # Press Q on keyboard to stop recording
        if pressedKey == ord('q'):
            print("Terminating")
            break


        if pressedKey == ord('s'):
            loraController.send("HELLO")

        
    # Break the loop
    else:
        break  

# When everything done, release the video capture and video write objects
Buttonz.cap.release()

# Closes all the frames
cv2.destroyAllWindows()