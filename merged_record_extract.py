import cv2
import numpy as np
import pyautogui
import math
import os
import time

"""
Records screen input, creates video file named output.avi
Iterates over screen recording video and creates an image per frame of the screen recording.

"""

RESOLUTION = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"XVID")


def record_screen():
    output = cv2.VideoWriter("output.avi", codec, 20.0, (RESOLUTION))
    while True:
        img = pyautogui.screenshot()
        # convert pixels to numpy array to work with OpenCV
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output.write(frame)
        # if the user clicks esc, it exits
        if cv2.waitKey(1) == 27:
            break

    # Close everything upon completion
    cv2.destroyAllWindows()
    output.release()


def extract_frames(inputvid):
    # Creates frames folder to store images
    framePath = os.path.join(os.getcwd(), "frames");
    if not os.path.exists(framePath):
        os.mkdir(framePath)

    count = 0
    capture = cv2.VideoCapture(inputvid)  # capture the video from the given path
    frameRate = capture.get(5)  # Get framerate of video
    while (capture.isOpened()):
        frameNum = capture.get(1)  # Get current frame number
        ret, frame = capture.read()
        if (ret != True):  # If there are no frames left to read
            break
        if (frameNum % math.floor(frameRate) == 0):
            filename = "frame%d.jpg" % count;
            count += 1
            cv2.imwrite(os.path.join(framePath, filename), frame)  # Writes image of frame.

    capture.release()  # Close video reader


if __name__ == "__main__":
    record_screen()
    extract_frames(inputvid="output.avi")
