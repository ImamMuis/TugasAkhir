import cv2
import time

capture_duration = 10
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = cv2.VideoWriter('output.mp4',fourcc, 25.0, (640,480))

start_time = time.time()
while( int(time.time() - start_time) < capture_duration ):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame, 1)
        out.write(frame)
        cv2.imshow('frame',frame)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()