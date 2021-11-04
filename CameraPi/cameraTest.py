import cv2
import numpy as np
from datetime import datetime
# import RPi.GPIO as GPIO
from gpiozero import Button
from time import sleep

class ControllerButtons():
    
    ScreenshotButton = None
    RecordButton = None
    UpButton = None
    DownButton = None
    LightsButton = None
    
    Active_State = False
    Previous_State = Button(1)
    
    def __init__(self, ScreenshotIn, RecordIn, UpIn, DownIn, LightsIn):
        
        self.ScreenshotButton = Button(ScreenshotIn)
        self.RecordButton = Button(RecordIn)
        self.UpButton = Button(UpIn)
        self.DownButton = Button(DownIn)
        self.LightsButton = Button(LightsIn)

    def Pressed(self, button):
        if button.is_pressed and self.Active_State == False:
            self.Active_State = True
            
            if self.ScreenshotButton == button:
                print("SCREENSHOT BUTTON HAS BEEN PRESSED")
            if self.RecordButton == button:
                print("Record BUTTON HAS BEEN PRESSED")
            if self.UpButton == button:
                print("Up BUTTON HAS BEEN PRESSED")
            if self.DownButton == button:
                print("Down BUTTON HAS BEEN PRESSED")
            if self.LightsButton == button:
                print("Lights BUTTON HAS BEEN PRESSED")
#             print("Taking Screenshot")
#             filename_images = "images/Screenshot_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".jpeg"
#             cv2.imwrite(filename_images, frame)
            self.Previous_State = button
#             ScreenshotButton.wait_for_release(2)

    def Released(self, button):
            if button.is_active == False and self.Previous_State == button:
                self.Active_State = False
                
                if self.ScreenshotButton == button:
                    print("SCREENSHOT BUTTON HAS BEEN released")
                if self.RecordButton == button:
                    print("Record BUTTON HAS BEEN released")
                if self.UpButton == button:
                    print("Up BUTTON HAS BEEN released")
                if self.DownButton == button:
                    print("Down BUTTON HAS BEEN released")
                if self.LightsButton == button:
                    print("Lights BUTTON HAS BEEN released")
#         print(ScreenshotButton.is_active)

# setting up
# ScreenshotIn = 18
# RecordIn = 23
# UpIn = 24
# DownIn = 25
# LightsIn = 21
# Active_State = False
# Previous_State = Button(1)
# 
# ScreenshotButton = Button(ScreenshotIn)
# RecordButton = Button(RecordIn)
# UpButton = Button(UpIn)
# DownButton = Button(DownIn)
# LightsButton = Button(LightsIn)

# Create Controller Button
Buttonz = ControllerButtons(18, 23, 24, 25, 21)
ScreenshotButton = Buttonz.ScreenshotButton
RecordButton = Buttonz.RecordButton
UpButton = Buttonz.UpButton
DownButton = Buttonz.DownButton
LightsButton = Buttonz.LightsButton
# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
filename_videos = "videos/Recording_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".avi"
out = cv2.VideoWriter(filename_videos,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

i = 0

while(True):
    ret, frame = cap.read()

    if ret == True: 

        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame    
        cv2.imshow('frame',frame)
        
        #Take picture
        pressedKey = cv2.waitKey(1) & 0xFF
        
        Buttonz.Pressed(ScreenshotButton)
        Buttonz.Released(ScreenshotButton)
        
        Buttonz.Pressed(RecordButton)
        Buttonz.Released(RecordButton)
        
        Buttonz.Pressed(UpButton)
        Buttonz.Released(UpButton)
        
        Buttonz.Pressed(DownButton)
        Buttonz.Released(DownButton)
        
        Buttonz.Pressed(LightsButton)
        Buttonz.Released(LightsButton)
        
#         if Buttonz.ScreenshotButton.is_pressed and Buttonz.Active_State == False:
#             Buttonz.Active_State = True
#             i += 1
#             print("SCREENSHOT BUTTON HAS BEEN PRESSED", i)
# #             print("Taking Screenshot")
# #             filename_images = "images/Screenshot_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".jpeg"
# #             cv2.imwrite(filename_images, frame)
#             Buttonz.Previous_State = Buttonz.ScreenshotButton
# #             ScreenshotButton.wait_for_release(2)
#         if Buttonz.ScreenshotButton.is_active == False and Buttonz.Previous_State == Buttonz.ScreenshotButton:
#             Buttonz.Active_State = False
#             i+=1
#             print("Screenshot button not being pressed lol", i)
#         print(ScreenshotButton.is_active)
            
            
            
#         if RecordButton.is_pressed and Active_State == False:
#             Active_State = True
#             i+=1
#             print("RECORD BUTTON HAS BEEN PRESSED", i)
#             Previous_State = RecordButton
# #             RecordButton.wait_for_release(2)
#         if RecordButton.is_active == False and Previous_State == RecordButton:
#             Active_State = False
#             i+=1
#             print("Record button not being pressed lol", i)
#             
#             
#             
#         if UpButton.is_pressed and Active_State == False:
#             Active_State = True
#             i+=1
#             print("UP BUTTON HAS BEEN PRESSED", i)
#             Previous_State = UpButton
#         if UpButton.is_active == False and Previous_State == UpButton:
#             Active_State = False
#             i+=1
#             print("UP button not being pressed lol", i)
#             
#             
#             
#         if DownButton.is_pressed and Active_State == False:
#             Active_State = True
#             i+=1
#             print("DOWN BUTTON HAS BEEN PRESSED", i)
#             Previous_State = DownButton
#         if DownButton.is_active == False and Previous_State == DownButton:
#             Active_State = False
#             i+=1
#             print("Down button not being pressed lol", i)
#             
#             
#             
#         if LightsButton.is_pressed and Active_State == False:
#             Active_State = True
#             i+=1
#             print("LIGHT BUTTON HAS BEEN PRESSED", i)
#             Previous_State = LightsButton
#         if LightsButton.is_active == False and Previous_State == LightsButton:
#             Active_State = False
#             i+=1
#             print("Light button not being pressed lol", i)
#             

        
        if pressedKey == ord('s'):
            print("Taking Screenshot")
            filename_images = "images/Screenshot_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".jpeg"
            cv2.imwrite(filename_images, frame)

        # Press Q on keyboard to stop recording
        if pressedKey == ord('q'):
            print("Terminating")
            break

        
    # Break the loop
    else:
        break  

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()