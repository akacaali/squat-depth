import cv2
import numpy as np

# Path to your video file
video_path = r"C:\Users\david\Downloads\squat.mp4"
output_path = r"C:\Users\david\Downloads\output_squat_tracking.mp4"

# Capture video from the file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
else:
    print("Video file opened successfully.")

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Define the range for the green color #76FF03 in HSV
lower_green = np.array([40, 240, 240])
upper_green = np.array([50, 255, 255])

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    if not ret:
        print("End of video file reached or cannot read the frame.")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    # Draw circles around detected green areas and store their centers
    for contour in contours:
        # Get the minimum enclosing circle around the contour
        ((x, y), radius) = cv2.minEnclosingCircle(contour)

        # Only consider significant contours
        if radius > 5:
            # Draw the circle in the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            centers.append((int(x), int(y)))

    # If two centers are detected, draw a line between them
    if len(centers) == 2:
        cv2.line(frame, centers[0], centers[1], (0, 255, 0), 2)

        # Calculate the angle of the line
        (x1, y1), (x2, y2) = centers
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

        # Check if the line is approximately vertical
        if -10 <= angle <= 10 or 170 <= angle <= 190:
            cv2.putText(frame, "Good", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            print("Good")
        else:
            cv2.putText(frame, "Fail", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            print("Fail")

    # Show the frame with tracking and line
    cv2.imshow('Tracked Video', frame)

    # Write the frame to the output video
    out.write(frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()
