import cv2
import numpy as np
from datetime import datetime
from gpiozero import Button
from time import sleep
from ControllerButtons import ControllerButtons

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

while(True):
    
    
    
    ret, frame = Buttonz.cap.read()

    if ret == True: 

        # Write the frame into the file 'output.avi'
        if (Buttonz.out != None):
            Buttonz.out.write(frame)

        # Display the resulting frame    
        cv2.imshow('frame',frame)
        
        #Get key press
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

        
    # Break the loop
    else:
        break  

# When everything done, release the video capture and video write objects
Buttonz.cap.release()

# Closes all the frames
cv2.destroyAllWindows()




# LORA CONTROLLER MAIN


# def main():
#     logging.basicConfig(filename='output.log', filemode='w', level=logging.DEBUG)
#     payload = ""

#     print("Connecting to REYAX RYLR896 transceiver module…")
#     serial_conn = serial.Serial(
#         port="/dev/serial0",
#         baudrate=115200,
#         timeout=5,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS
#     )

#     if serial_conn.isOpen():
        
#         prmainnt("Serial Port is Open")
        
#         set_lora_config(serial_conn)
#         check_lora_config(serial_conn)
        
        
#         connect_to_camera(serial_conn)
        
        
#         wait_read(serial_conn)
        
#         #CONNECTION SET UP, ENTER STANBY MODE
        
#         standby_mode(serial_conn)