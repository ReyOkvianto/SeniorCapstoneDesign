import cv2
import numpy as np
from datetime import datetime
# import RPi.GPIO as GPIO
from gpiozero import Button
from time import sleep

def button_callback(channel):
    print(channel)
    print("Button Pressed")

# setting up
in1 = 23

button = Button(in1)

# GPIO.setmode( GPIO.BCM)
# #GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(in1, GPIO.IN)

# GPIO.setup(out1, GPIO.OUT)

# GPIO.output(out1, GPIO.LOW)

# GPIO.setwarnings(False)

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

while(True):
    ret, frame = cap.read()

    if ret == True: 

        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame    
        cv2.imshow('frame',frame)
        
        #Take picture
        pressedKey = cv2.waitKey(1) & 0xFF
        
        
        if button.is_pressed:
            print("BUTTON HAS BEEN PRESSED")
            button.wait_for_release(2)
#         if GPIO.input(in1):
#             print("Button Pressed")
#         if GPIO.input(in1):
#             button_callback(in1)
            #GPIO.add_event_detect(in1,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
        
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