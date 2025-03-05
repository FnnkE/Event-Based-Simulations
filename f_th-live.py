import cv2 as cv
import numpy as np
import time


f = open("th-timings.txt", "w")

# Open the default camera
cam = cv.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

output = np.zeros((frame_height,frame_width,3), np.uint8)

ret, frame = cam.read()

frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
# frameB = cv.blur(frameG,(5,5))
frameB = cv.medianBlur(frameG,5)
ret,frameTH = cv.threshold(frameB,127,255,cv.THRESH_BINARY)

initial = frameTH

while True:
    start_time = time.perf_counter()

    ret, frame = cam.read()

    frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameB = cv.medianBlur(frameG,5)
    # frameB = cv.GaussianBlur(frameG, (5, 5), 0)
    ret,frameTH = cv.threshold(frameB,127,255,cv.THRESH_BINARY)

    new = frameTH-initial 
    old = initial-frameTH

    for y in range(frame_height):
        for x in range(frame_width):
            output[y,x] = (old[y,x], 0, new[y,x])
    
    initial = frameTH
    # Display the captured frame
    cv.imshow('Camera', output)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    f.write(str(elapsed_time)+"\n")

    # Press 'q' to exit the loop
    if cv.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv.destroyAllWindows()