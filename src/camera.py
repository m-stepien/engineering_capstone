import cv2
from flask import Flask, Response
import os
import glob

app = Flask(__name__)


def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


def generate_mock_frames():
    mock_images_path = "frames/*.jpg"  # Path to your mock images
    mock_images = [cv2.imread(img_path) for img_path in sorted(glob.glob(mock_images_path))]
    if not mock_images:
        print("Error: No mock images found.")
        exit()
    while True:
        for frame in mock_images:
            if frame is None:
                print("Failed to load mock frame.")
                continue

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')



@app.route('/video')
def video():
    return Response(generate_mock_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12346)