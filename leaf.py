import cv2
import numpy as np

def find_scale_and_area(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    scale_length = None
    object_area = None

    for contour in contours:
        # Approximate the contour to reduce the number of points
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Get bounding box dimensions
        x, y, w, h = cv2.boundingRect(contour)

        # Assuming the scale is the smallest rectangle
        if w > 0 and h > 0 and (w < 100 and h < 100):  # Adjust thresholds as needed
            scale_length = max(w, h)  # Length of the scale in pixels

        else:
            # Calculate object area
            object_area = cv2.contourArea(contour)

    return scale_length, object_area

# Access the laptop camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

print("Press 's' to capture the image and calculate the area.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Show the live video feed
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):  # Press 's' to capture
        scale_length, object_area = find_scale_and_area(frame)
        if scale_length and object_area:
            # Assuming the scale represents 1 cm in real life
            scale_in_cm = 1  # Change this based on your scale
            pixel_to_cm_ratio = scale_in_cm / scale_length

            real_area = object_area * (pixel_to_cm_ratio ** 2)
            print(f"Calculated Area: {real_area:.2f} cm²")
        else:
            print("Could not detect scale or object.")
        break
    elif key == ord('q'):  # Press 'q' to quit
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

