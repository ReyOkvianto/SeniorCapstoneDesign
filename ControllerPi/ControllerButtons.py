import cv2
import numpy as np
from datetime import datetime
from gpiozero import Button
from time import sleep
from PIL import Image, ImageDraw, ImageFont

class ControllerButtons():
    
    ScreenshotButton = None
    RecordButton = None
    UpButton = None
    DownButton = None
    LightsButton = None
    
    cap = None
    frame_width = None
    frame_height = None
    out = None
    
    Active_State = False
    Previous_State = Button(1)

    Command = None

    status_img = None
    recording_img = None
    
    def __init__(self, ScreenshotIn, RecordIn, UpIn, DownIn, LightsIn):
        
        self.ScreenshotButton = Button(ScreenshotIn)
        self.RecordButton = Button(RecordIn)
        self.UpButton = Button(UpIn)
        self.DownButton = Button(DownIn)
        self.LightsButton = Button(LightsIn)
        
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)

        # Check if camera opened successfully
        if (self.cap.isOpened() == False): 
          print("Unable to read camera feed")
          
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))

        image_width = self.frame_width
        image_height = int(self.frame_height/10)
        img = Image.new('RGB', (image_width, image_height), color=(~255, ~255, ~255))

        # create the canvas
        canvas = ImageDraw.Draw(img)

        status_text = cv2.getTextSize("Connecting...", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        recording_text = cv2.getTextSize("Not Recording", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

        x_pos_status_text = (self.frame_width - status_text[0]) / 2
        y_pos_status_text = (image_height + status_text[1]) / 2 

        x_pos_recording_text = (self.frame_width - recording_text[0]) / 2
        y_pos_recording_text = (image_height + recording_text[1]) / 2

        img.save('hello_world.png')

        self.status_img = cv2.imread('hello_world.png')
        cv2.putText(self.status_img, "Connecting...", (int(x_pos_status_text),int(y_pos_status_text)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        self.recording_img = cv2.imread('hello_world.png')
        cv2.putText(self.recording_img, "Not Recording", (int(x_pos_recording_text),int(y_pos_recording_text)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        

    def Pressed(self, button, frame=None):
        if button.is_pressed and self.Active_State == False:
            self.Active_State = True
            if self.ScreenshotButton == button:
                print("SCREENSHOT BUTTON HAS BEEN PRESSED")
                self.TakeScreenshot(frame)
            if self.RecordButton == button:
                print("Record BUTTON HAS BEEN PRESSED")

                if self.out == None: 
                    self.RecordStart()
                else:
                    self.RecordStop()
            if self.UpButton == button:
                self.Command = "MOVE CAMERA UP"
                print("Up BUTTON HAS BEEN PRESSED")
                
            if self.DownButton == button:
                self.Command = "MOVE CAMERA DOWN"
                print("Down BUTTON HAS BEEN PRESSED")

            if self.LightsButton == button:
                self.Command = "TOGGLE LIGHT"
                print("Lights BUTTON HAS BEEN PRESSED")
#             print("Taking Screenshot")
#             filename_images = "images/Screenshot_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".jpeg"
#             cv2.imwrite(filename_images, frame)
            self.Previous_State = button
#             ScreenshotButton.wait_for_release(2)

    def Released(self, button):
            if button.is_active == False and self.Previous_State == button:
                self.Active_State = False
                #if self.ScreenshotButton == button:
                #    print("SCREENSHOT BUTTON HAS BEEN released")
                #if self.RecordButton == button:
                #    print("Record BUTTON HAS BEEN released")
                #if self.UpButton == button:
                #    print("Up BUTTON HAS BEEN released")
                #if self.DownButton == button:
                #    print("Down BUTTON HAS BEEN released")
                #if self.LightsButton == button:
                    #print("Lights BUTTON HAS BEEN released")

                self.Command = None
#         print(ScreenshotButton.is_active)

    def RecordStart(self):
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        self.SetRecordingText("Recording")
        filename_videos = "/home/pi/Desktop/VIDEOS/Recording_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".avi"
        self.out = cv2.VideoWriter(filename_videos,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (self.frame_width, self.frame_height))
        
    def RecordStop(self):
        self.SetRecordingText("Not Recording")
        self.out.release()
        self.out = None


    def TakeScreenshot(self, frame):
        filename_images = "/home/pi/Desktop/IMAGES/Screenshot_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".jpeg"
        cv2.imwrite(filename_images, frame)
        self.SetText("Took Screenshot")

    def GetCommand(self):
        return self.Command

    def SetText(self, message):
        status_text = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

        self.status_img = cv2.imread('hello_world.png')

        x_pos_status_text = (self.frame_width - status_text[0]) / 2
        y_pos_status_text = (int(self.frame_height/10)+ status_text[1]) / 2
        cv2.putText(self.status_img, message, (int(x_pos_status_text),int(y_pos_status_text)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)



    def SetRecordingText(self, message):
        self.recording_img = cv2.imread('hello_world.png')

        recording_text = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

        x_pos_recording_text = (self.frame_width - recording_text[0]) / 2
        y_pos_recording_text = (int(self.frame_height/10) + recording_text[1]) / 2 
        cv2.putText(self.recording_img, message, (int(x_pos_recording_text),int(y_pos_recording_text)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)


