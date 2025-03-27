import cv2


def canny_edge_detection(frame): 
    """
    Perform Canny edge detection on a given frame.
    This function converts the input frame to grayscale, applies a median blur 
    to reduce noise, and then performs Canny edge detection to extract edges.
    Args:
        frame (numpy.ndarray): The input image frame in BGR format.
    Returns:
        numpy.ndarray: A binary image where edges are marked in white (255) 
        and non-edges are black (0).
    """
    # Convert the frame to grayscale for edge detection 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
      
    # Apply gaussian blur to reduce noise and smoothen edges 
    blurred = cv2.medianBlur(gray,5)
      
    # Perform canny edge detection 
    edges = cv2.Canny(blurred, 10, 500) 
      
    return edges