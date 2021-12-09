from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from datetime import datetime
from datetime import timedelta


# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

image_width = frame_width
image_height = int(frame_height/4)
img = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))

# create the canvas
canvas = ImageDraw.Draw(img)

x_pos = int((image_width) / 2)
y_pos = int((image_height) / 2)

img.save('hello_world.png')

last_time = datetime.now()

img2 = cv2.imread('hello_world.png')
cv2.putText(img2, "AYOOOO", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

while(True):
    ret, frame = cap.read()

    if ret == True: 
        # Use opencv to read in two images on top of each other

        images = np.vstack((frame, img2))

        cv2.imshow('images', images)

        pressedKey = cv2.waitKey(1) & 0xFF
        # Press Q on keyboard to stop recording
        if pressedKey == ord('q'):
            img2 = cv2.imread('hello_world.png')
            cv2.putText(img2, "test1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            
        if pressedKey == ord('s'):
            img2 = cv2.imread('hello_world.png')
            cv2.putText(img2, "test2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            

# When everything done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
