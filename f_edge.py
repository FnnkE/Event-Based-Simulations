import cv2 
import numpy as np
  
def canny_edge_detection(frame): 
    # Convert the frame to grayscale for edge detection 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
      
    # Apply gaussian blur to reduce noise and smoothen edges 
    blurred = cv2.medianBlur(gray,5)
      
    # Perform canny edge detection 
    edges = cv2.Canny(blurred, 10, 500) 
      
    return edges

def main():
    # Setup default webcam  
    cap = cv2.VideoCapture(0) 
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read a frame from the webcam 
    ret, frame = cap.read() 
    if not ret: 
        print('Image not captured') 
        return 1
    
    # Produce initial edge frame
    edges = canny_edge_detection(frame) 
    initial = edges

    # Initialize arrays
    CPUTickList = []
    totalList = []
    edgeConversionList = []
    fastEdgeConversionList = []
    output = np.zeros((frame_height,frame_width,3), np.uint8)
  
    while True: 
        totalStartTime = cv2.getTickCount()
        
        # Read a frame from the webcam 
        ret, frame = cap.read() 
        if not ret: 
            print('Image not captured') 
            break
        
        # Perform canny edge detection on the frame with timings
        startTime = cv2.getTickCount()
        edges = canny_edge_detection(frame) 
        endTime = cv2.getTickCount()
        CPUTickList.append((endTime-startTime)/cv2.getTickFrequency())

        # Calculate Event-Like simulations with timings
        startTime = cv2.getTickCount()
        new = cv2.subtract(edges, initial)
        old = cv2.subtract(initial, edges)        
        _, new_thresh = cv2.threshold(new, 200, 255, cv2.THRESH_BINARY)
        _, old_thresh = cv2.threshold(old, 200, 255, cv2.THRESH_BINARY)
        output[:, :, 2] = old_thresh  
        output[:, :, 0] = new_thresh 
        endTime = cv2.getTickCount()
        fastEdgeConversionList.append((endTime-startTime)/cv2.getTickFrequency())

        # Display Event-Like frame
        cv2.imshow("Edges", output) 

        initial = edges.copy()

        # Calculate total elapsed time for frame
        totalEndTime = cv2.getTickCount()
        totalList.append((totalEndTime-totalStartTime)/cv2.getTickFrequency())
        
        # Exit the loop when 'q' key is pressed 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
    # Computing average runtime of canny method
    timingArrayCPU = np.array(CPUTickList)
    print("Average performance time of canny edge method: ", np.mean(timingArrayCPU))
    # timingArrayEdgeConversion = np.array(edgeConversionList)
    # print("Average performance time of edge conversion: ", np.mean(timingArrayEdgeConversion))
    timingArrayFastEdgeConversion = np.array(fastEdgeConversionList)
    print("Average performance time of fast edge conversion: ", np.mean(timingArrayFastEdgeConversion))
      
    # Release the webcam and close the windows 
    cap.release() 
    cv2.destroyAllWindows()

    # Save timing per frame to file
    f = open("d_improved-filter-edge-timings.txt", "w")
    for i in totalList:
        f.write(str(i)+"\n")
    f.close()

if __name__ == "__main__": 
    main()