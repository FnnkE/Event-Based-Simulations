import cv2 as cv
import numpy as np

def main():
    # Setup default camera
    cam = cv.VideoCapture(0)
    frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Read a frame from the webcam 
    ret, frame = cam.read()
    if not ret: 
            print('Image not captured') 
            return 1

    # Produce intial threshold frame
    frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameB = cv.medianBlur(frameG,5)
    ret,frameTH = cv.threshold(frameB,127,255,cv.THRESH_BINARY)
    initial = frameTH

    # Initialize arrays
    totalList = []
    output = np.zeros((frame_height,frame_width,3), np.uint8)

    while True:
        totalStartTime = cv.getTickCount()

        # Read a frame from the webcam 
        ret, frame = cam.read()
        if not ret: 
            print('Image not captured') 
            break

        # Produce new threshold frame
        frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frameB = cv.medianBlur(frameG,5)
        ret,frameTH = cv.threshold(frameB,127,255,cv.THRESH_BINARY)

        # Calculate Event-Like simulation
        new = cv.subtract(frameTH, initial)
        old = cv.subtract(initial, frameTH)
        output[:, :, 2] = old  
        output[:, :, 0] = new 
        
        initial = frameTH.copy()

        # Display Event-Like frame
        cv.imshow('Camera', output)

        # Calculate total elapsed time for frame
        totalEndTime = cv.getTickCount()
        totalList.append((totalEndTime-totalStartTime)/cv.getTickFrequency())
        
        # Press 'q' to exit the loop
        if cv.waitKey(1) == ord('q'):
            break

    # Save timings per frame to file
    f = open("d_improved-filter-th-timings.txt", "w")
    for i in totalList:
        f.write(str(i)+"\n")
    f.close()

    # Release the webcam and close the windows 
    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__": 
    main()