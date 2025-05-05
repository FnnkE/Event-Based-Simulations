import cv2 as cv
import numpy as np
import os
import time

# COLOR CONSTANTS
CBOLD     = '\33[1m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CEND    = '\33[0m'
CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

def convert_to_spikes(src, smoothing=True,
             new_color=[255,0,0], old_color=[0,0,255],
             directory = "output",
             timing_output=False, timing_title="EventTimings.txt",
             text_output=False, text_title="EventOutput.txt",
             vid_output=False, vid_title="EventOutput.avi"):
    
    # Create color factors
    n_R = new_color[0]/255; n_G = new_color[1]/255; n_B = new_color[2]/255
    o_R = old_color[0]/255; o_G = old_color[1]/255; o_B = old_color[2]/255
    
    # Get information about camera or videos
    frame_width = int(src.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(src.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Read a frame from source 
    ret, frame = src.read()
    if not ret: 
            print('Image not captured') 
            return 1

    # Produce intial threshold frame
    frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameTH = cv.adaptiveThreshold(frameG, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 10)
    initial = frameTH
    
    # Initialize arrays (convert to np??)
    timeList = []
    newFrames = []
    oldFrames = []
    allFrames = []
    output = np.zeros((frame_height,frame_width,3), np.uint8)

    # General hit or miss kernel mask
    if (smoothing):
        kernel = np.array([ [-1, -1, -1],
                            [-1,  1, -1],
                            [-1, -1, -1] ], dtype="int")


    ##### Loop through video or feed
    while src.isOpened():
        # Start performance timer
        startTime = cv.getTickCount()

        # Read a frame from the webcam 
        ret, frame = src.read()
        if not ret: 
            print('Video Ended') 
            break
        
        # Produce new threshold frame
        frameG = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ___,frameTH = cv.threshold(frameG,125,255,cv.THRESH_BINARY)
        # frameTH = cv.adaptiveThreshold(frameG, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 10)

        # Calculate event simulation
        new = cv.subtract(frameTH, initial)
        old = cv.subtract(initial, frameTH)
        initial = frameTH.copy()

        # Smooth image with Hit or Miss
        if (smoothing):
            single_pixels = cv.morphologyEx(new, cv.MORPH_HITMISS, kernel)
            single_pixels_inv = cv.bitwise_not(single_pixels)
            new = cv.bitwise_and(new, new, mask=single_pixels_inv)

            single_pixels = cv.morphologyEx(old, cv.MORPH_HITMISS, kernel)
            single_pixels_inv = cv.bitwise_not(single_pixels)
            old = cv.bitwise_and(old, old, mask=single_pixels_inv)
        
        # Refine events through erosion
        # new = cv.erode(new, kernel, iterations=1)
        # old = cv.erode(old, kernel, iterations=1)

        # Refine events through opening
        # new = cv.morphologyEx(new, cv.MORPH_OPEN, kernel)
        # old = cv.morphologyEx(old, cv.MORPH_OPEN, kernel)

        # Update New Frame
        output[:, :, 2] = old*o_R  + new*n_R # RED
        output[:, :, 1] = old*o_G + new*n_G  # GREEN
        output[:, :, 0] = old*o_B + new*n_B  # BLUE
        
        # Backup current frames
        allFrames.append(output.copy())
        newFrames.append(new.copy())
        oldFrames.append(old.copy())

        # Display Event-Like frame
        cv.imshow('Event Output', output)

        # Calculate total elapsed time for frame
        endTime = cv.getTickCount()
        timeList.append((endTime-startTime)/cv.getTickFrequency())
        
        # Press 'q' to exit the loop
        if cv.waitKey(1) == ord('q'):
            break
    cv.destroyAllWindows()

    ##### Generate directory if needed
    if (timing_output or vid_output or text_output):
        os.makedirs(directory, exist_ok=True)

    ##### Save timings between frames to file
    if (timing_output):
        # Start performance timer
        startTime = time.time()
        # Open/create file
        f = open(f"{directory}/{timing_title}", "w")
        # Iterate through each time entry
        totalSize = len(timeList)
        for index, timeEntry in enumerate(timeList):
            # Calculate current progress
            progress = int((index/totalSize)*10)
            remaining = (10-progress)
            print(f"Saving Timings             | 0% [{CYELLOW}{'▨'*progress}{CEND}{(' '*remaining)}] 100% | {CYELLOW2}Loading{CEND}", end='\r', flush=True)
            # Write time to file
            f.write(str(timeEntry)+"\n")
        # Close file
        f.close()
        # End timer and calculate elapsed time
        endTime = time.time()
        print(f"Saving Timings             | 0% [{CYELLOW}{'■'*10}{CEND}] 100% | {CGREEN}Complete{CEND} ({(endTime-startTime):.3f}s)", end='\n', flush=True)
    
    ##### Save event output as video
    if (vid_output):
        # Start performance timer
        startTime = time.time()
        # Create video with similar specs to source
        frame_rate = int(src.get(cv.CAP_PROP_FPS))
        video = cv.VideoWriter(f"{directory}/{vid_title}", cv.VideoWriter_fourcc(*'MJPG'), frame_rate, (frame_width, frame_height))
        # Iterate through each frame
        totalSize = len(allFrames)
        for index, frame in enumerate(allFrames):
            # Calculate current progress
            progress = int((index/totalSize)*10)
            remaining = (10-progress)
            print(f"Saving Video               | 0% [{CYELLOW}{'▨'*progress}{CEND}{(' '*remaining)}] 100% | {CYELLOW2}Loading{CEND}", end='\r', flush=True)
            # Write frame to video
            video.write(frame)
        # Close video
        video.release()
        # End timer and calculate elapsed time
        endTime = time.time()
        print(f"Saving Video               | 0% [{CYELLOW}{'■'*10}{CEND}] 100% | {CGREEN}Complete{CEND} ({(endTime-startTime):.3f}s)", end='\n', flush=True)

    ##### Convert events into arrays  
    # Create numpy arrays
    totalEvents = np.empty([1,4])
    oldFramesNP = np.array(oldFrames)
    newFramesNP = np.array(newFrames)
    # Start performance timer
    startTime = time.time()
    # Iterate across each event and store into a singular array
    timeElapsed = 0
    totalSize = len(timeList)
    for index, timeEntry in enumerate(timeList):
        # Calculate current progress
        progress = int((index/totalSize)*10)
        remaining = (10-progress)
        print(f"Converting Events to Array | 0% [{CYELLOW}{'▨'*progress}{CEND}{(' '*remaining)}] 100% | {CYELLOW2}Loading{CEND}", end='\r', flush=True)
        # Update current time
        timeElapsed += timeEntry
        timeElapsed = round(timeElapsed, 5)
        # Find coordinates of events
        new_x_coords, new_y_coords = np.nonzero(newFramesNP[index, :, :])
        old_x_coords, old_y_coords = np.nonzero(oldFramesNP[index, :, :])
        # Format event arrays
        newEvents = np.stack([ [timeElapsed]*len(new_x_coords), new_x_coords, new_y_coords, [1]*len(new_y_coords) ], axis=1, dtype=object)
        oldEvents = np.stack([ [timeElapsed]*len(old_x_coords), old_x_coords, old_y_coords, [-1]*len(old_y_coords) ], axis=1, dtype=object)
        # Combine event arrays
        frameEvents = np.concatenate( (newEvents, oldEvents), axis=0)
        totalEvents = np.concatenate( (totalEvents, frameEvents), axis=0)
    # End timer and calculate elapsed time
    endTime = time.time()
    print(f"Converting Events to Array | 0% [{CYELLOW}{'■'*10}{CEND}] 100% | {CGREEN}Complete{CEND} ({(endTime-startTime):.3f}s)", end='\n', flush=True)

    ##### Save events to a specified file and .npy file 
    if (text_output):
        # Start performance timer
        startTime = time.time()
        print(f"Exporting Events           | 0% [{CYELLOW}{'▨'*0}{CEND}{(' '*10)}] 100% | {CYELLOW2}Loading{CEND}", end='\r', flush=True)
        # Save events to .npy file
        np.save(f"{directory}/{text_title}", totalEvents)
        print(f"Exporting Events           | 0% [{CYELLOW}{'▨'*5}{CEND}{(' '*5)}] 100% | {CYELLOW2}Loading{CEND}", end='\r', flush=True)
        # Save events to file
        with open(f"{directory}/{text_title}", "w+") as f:
            content = str(totalEvents)
            f.write(content)
        np.savetxt(f"{directory}/numpy_{text_title}", totalEvents, fmt='%0.2f')
        # End timer and calculate elapsed time
        endTime = time.time()
        print(f"Exporting Events           | 0% [{CYELLOW}{'■'*10}{CEND}] 100% | {CGREEN}Complete{CEND} ({(endTime-startTime):.3f}s)", end='\n', flush=True)
    
    ##### Return numpy array of all events
    return totalEvents


import sys
cap = cv.VideoCapture("Perfect-loop-cube.gif")
if (cap.isOpened() == False):
    print("Error Occured: File Not Opened.")
    sys.exit()
cv.destroyAllWindows()

# Best Colors
# [255, 255, 255], [138, 170, 229] : White, Light Blue
# [234, 115, 141], [137, 171, 227] : Pink, Light Blue
# [151, 188, 98], [44, 95, 45]     : Green, Dark Green
# [251, 165, 24], [16, 55, 92]     : Orange, Dark Blue

# [184, 80, 66] Muted Red

convert_to_spikes(cap, [255, 255, 255], [251, 165, 24], vid_output=True, vid_title="Output.avi", text_output=True, timing_output=True)

cap.release()