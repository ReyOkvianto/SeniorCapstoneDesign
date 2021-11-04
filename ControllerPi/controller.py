# import cv2
# import numpy as np
  
  
# cap = cv2.VideoCapture(0)
  
# #1: make a nice large empty image:
# draw = np.zeros((480,800,3), dtype=np.uint8)

# #2: resize the cam frame to 640x480 (keeping a decent aspect ratio)
# frame = cv2.resize(frame, (640,480))

# #3: blit it into the large img
# draw[0:480, 0:640, :] = frame

# while(True):
      
#     # Capture frames in the video
#     ret, frame = cap.read()
  
#     # describe the type of font
#     # to be used.
#     font = cv2.FONT_HERSHEY_SIMPLEX
  
#     # Use putText() method for
#     # inserting text on video
#     cv2.putText(frame, 
#                 'TEXT ON VIDEO', 
#                 (50, 50), 
#                 font, 1, 
#                 (0, 255, 255), 
#                 2, 
#                 cv2.LINE_4)
  
#     # Display the resulting frame
#     cv2.imshow('video', frame)
  
#     # creating 'q' as the quit 
#     # button for the video
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# # release the cap object
# cap.release()
# # close all windows
# cv2.destroyAllWindows()


import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="DEEEEEZ NUTSSSS", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        label = tkinter.Label(window, text="DEEEEEZ NUTSSSS")
        label.pack(pady=20)


        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # self.vid.set(cv2.CAP_PROP_FPS, 30)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")