import cv2 
import numpy as np
import time
  
def canny_edge_detection(frame): 
    # Convert the frame to grayscale for edge detection 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
      
    # Apply Gaussian blur to reduce noise and smoothen edges 
    blurred = cv2.medianBlur(gray,5) # cv2.GaussianBlur(src=gray, ksize=(3, 5), sigmaX=0.5) 
      
    # Perform Canny edge detection 
    edges = cv2.Canny(blurred, 70, 135) 
      
    return edges

def main(): 

    # f = open("filter-edge-timings.txt", "w")

    # Open the default webcam  
    cap = cv2.VideoCapture(0) 

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output = np.zeros((frame_height,frame_width,3), np.uint8)

    ret, frame = cap.read() 
    if not ret: 
        print('Image not captured') 
        return 1
    
    edges = canny_edge_detection(frame) 

    initial = edges
      
    while True: 
        # start_time = time.perf_counter()

        # Read a frame from the webcam 
        ret, frame = cap.read() 
        if not ret: 
            print('Image not captured') 
            break
        
        # Perform Canny edge detection on the frame 
        edges = canny_edge_detection(frame) 
          
        new = edges-initial 
        old = initial-edges

        for y in range(frame_height):
            for x in range(frame_width):
                output[y,x] = (old[y,x], 0, new[y,x])

        # Display the original frame and the edge-detected frame 
        #cv2.imshow("Original", frame) 
        cv2.imshow("Edges", output) 

        initial = edges

        # end_time = time.perf_counter()
        # elapsed_time = end_time - start_time
        # f.write(str(elapsed_time)+"\n")
          
        # Exit the loop when 'q' key is pressed 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
      
    # Release the webcam and close the windows 
    cap.release() 
    cv2.destroyAllWindows()

    # f.close()

if __name__ == "__main__": 
    main()