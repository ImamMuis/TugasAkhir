import numpy as np
import cv2
import time
import os
import random
import sys


fps = 30
width = 640
height = 480
video_codec = cv2.VideoWriter_fourcc(*'mp4v')
name = random.randint(0, 1000)
print(name)
if os.path.isdir(str(name)) is False:
    name = random.randint(0, 1000)
    name = str(name)

name = os.path.join(os.getcwd(), str(name))
print("ALl logs saved in dir:", name)
os.mkdir(name)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret = cap.set(3, 640)
ret = cap.set(4, 480)
cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


start = time.time()
video_file_count = 1
video_file = os.path.join(name, str(video_file_count) + ".mp4")
print("Capture video saved location : {}".format(video_file))

# Create a video write before entering the loop
video_writer = cv2.VideoWriter(
    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
)

while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 1)
        cv2.imshow("frame", frame)
        if time.time() - start > 10:
            start = time.time()
            video_file_count += 1
            video_file = os.path.join(name, str(video_file_count) + ".mp4")
            video_writer = cv2.VideoWriter(
                video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
            )
            # No sleeping! We don't want to sleep, we want to write
            # time.sleep(10)

        # Write the frame to the current video writer
        video_writer.write(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()