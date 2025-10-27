# traffic signal Detection
import cv2
import numpy as np

# Initialize webcam
cam = cv2.VideoCapture(0)

print("Press 'q' to stop the program.")

while True:
    # Capture a frame from the camera
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break
    
    # Resize the image for faster processing
    img = cv2.resize(img, (640, 480))
    
    # Convert to HSV color space
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Extract Hue, Saturation, and Value channels
    H, S, V = cv2.split(hsvImg)
    
    # Define more accurate thresholds for red, yellow, and green
    redMask1 = (H < 10) & (S > 128) & (V > 153)
    redMask2 = (H > 160) & (S > 128) & (V > 153)
    redMask = cv2.bitwise_or(redMask1.astype(np.uint8), redMask2.astype(np.uint8))
    yellowMask = (H > 20) & (H < 30) & (S > 128) & (V > 153)
    greenMask = (H > 40) & (H < 75) & (S > 128) & (V > 153)
    
    # Clean up the masks using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    redMask = cv2.morphologyEx(redMask, cv2.MORPH_CLOSE, kernel)
    yellowMask = cv2.morphologyEx(yellowMask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    greenMask = cv2.morphologyEx(greenMask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    
    # Detect contours for each mask
    contours_red, _ = cv2.findContours(redMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(yellowMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize action variable
    action = "No signal detected"
    
    # Process red signal regions
    if len(contours_red) > 0:
        for contour in contours_red:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red Signal", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        action = "STOP"  # Red signal means stop
    
    # Process yellow signal regions
    if len(contours_yellow) > 0:
        for contour in contours_yellow:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(img, "Yellow Signal", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        action = "WAIT"  # Yellow signal means wait
    
    # Process green signal regions
    if len(contours_green) > 0:
        for contour in contours_green:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Green Signal", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        action = "GO"  # Green signal means go
    
    # Display the action on the image
    cv2.putText(img, action, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
    
    # Display the result
    cv2.imshow("Traffic Signal Detection and Action Suggestion", img)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cam.release()

cv2.destroyAllWindows()
