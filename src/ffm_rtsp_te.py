import cv2
import subprocess
import numpy as np

def stream_camera():
    # OpenCV VideoCapture to access the webcam or a video device
    # cap = cv2.VideoCapture(0)  # Use the correct camera index or device path
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",  # Real-time streaming
        "-f", "rawvideo",  # Raw input format
        "-pix_fmt", "bgr24",  # Pixel format from OpenCV
        "-s", f"{width}x{height}",  # Frame size
        "-r", str(fps),  # Frame rate
        "-i", "-",  # Input from stdin
        "-c:v", "libx264",  # H.264 codec
        "-preset", "ultrafast",  # Encoding speed preset
        "-tune", "zerolatency",  # Reduce latency
        "-f", "rtsp",  # Output format
        "rtsp://0.0.0.0:8554/test"  # RTSP server URL
    ]

    # Start the FFmpeg process
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    try:
        while True:
            ret, frame = cap.read()  # Capture a frame from the camera
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Write the frame to the FFmpeg process
            process.stdin.write(frame.tobytes())
    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        # Clean up resources
        cap.release()
        process.stdin.close()
        process.wait()

stream_camera()

