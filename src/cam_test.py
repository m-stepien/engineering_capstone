import cv2
import os

cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_filename, frame)
    print(f"Saved {frame_filename}")

    frame_count += 1

    if frame_count >= 100:  # Stop after 100 frames
        break

cap.release()
print("Done capturing frames.")

