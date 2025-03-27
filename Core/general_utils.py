import cv2

def setup_webcam():
    """
    Initializes and sets up the webcam for video capture.

    This function creates a VideoCapture object to access the default webcam
    (device index 0) and retrieves the frame width and height properties.

    Returns:
        tuple: A tuple containing the frame height and frame width as integers.
    """
    cap = cv2.VideoCapture(0) 
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return (frame_height, frame_width)


def check_webcam_functionality():
    """
    Verifies if the webcam is operational by attempting to capture a frame.

    Returns:
        tuple: A tuple containing a boolean indicating success (True if the webcam 
               captured a frame, False otherwise) and the captured frame (or None if unsuccessful).
    """
    webcam = cv2.VideoCapture(0)
    success, captured_frame = webcam.read()
    if not success:
        print('Failed to capture an image from the webcam.')
        return False, None
    return success, captured_frame

