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
    totalFrames = []
    totalNew = []
    totalOld = []
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
        totalNew.append(new)
        totalOld.append(old)

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

    # Convert frames to Event-Based stream
    totalTime = 0
    f = open("e_th.txt", "w")
    for index, time in enumerate(totalList):
        totalTime += time
        for y_coord, y_val in enumerate(totalNew[index]):
            for x_coord, x_val in enumerate(y_val):
                    if (x_val == 255):
                        f.write("{" + str(totalTime) +",[" + str(x_coord) + "," + str(y_coord)  + "]" + ",1}"+"\n")
        for y_coord, y_val in enumerate(totalOld[index]):
            for x_coord, x_val in enumerate(y_val):
                    if (x_val == 255):
                        f.write("{" + str(totalTime) +",[" + str(x_coord) + "," + str(y_coord)  + "]" + ",-1}"+"\n")
    f.close()

    # print(f"all:    {totalNew}\n {len(totalNew)}")
    # print(f"1:      {totalNew[0]} \n {len(totalNew[0])}")
    # print(f"2:      {totalNew[0][0]} \n {len(totalNew[0][0])}")
    # print(f"3:      {totalNew[0][0][0]}")
    # print(f"{frame_width} x {frame_height} : w x h")
    # format : [time] [y] [x]

    # Release the webcam and close the windows 
    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__": 
    main()