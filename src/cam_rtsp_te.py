import cv2
import subprocess
import time

def stream_camera():
    # Open the video capture using V4L2 (Linux video capture API)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Using V4L2
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # FFmpeg command to stream via RTSP
    ffmpeg_cmd = [
        'ffmpeg',
        '-re',  # Read input at native frame rate
        '-i', 'pipe:0',  # Input from stdin (pipe)
        '-c:v', 'libx264',  # Video codec
        '-f', 'rtsp',  # Output format
        'rtsp://inz.local:8554/test'  # RTSP server URL
    ]
    
    # Start the FFmpeg process
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Ensure the process is still running
        if process.poll() is not None:
            print("FFmpeg process terminated unexpectedly.")
            break

        # Write the frame to FFmpeg's stdin
        try:
            print("good")
            process.stdin.write(frame.tobytes())
        except BrokenPipeError as e:
            print("Error: Broken pipe while sending data to FFmpeg.")
            print(e)
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        print("good")

    # Cleanup
    cap.release()
    process.stdin.close()
    process.wait()

if __name__ == "__main__":
    stream_camera()


# import cv2
# import subprocess
# import time
# import sys

# def stream_camera():
#     # Open the video capture using V4L2 (Linux video capture API)
#     cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Using V4L2
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return

#     # FFmpeg command to stream via RTSP
#     ffmpeg_cmd = [
#         'ffmpeg',
#         '-re',  # Read input at native frame rate
#         '-i', 'pipe:0',  # Input from stdin (pipe)
#         '-c:v', 'libx264',  # Video codec
#         '-f', 'rtsp',  # Output format
#         'rtsp://localhost:8554/test'  # RTSP server URL
#     ]
    
#     # Start the FFmpeg process
#     process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Failed to grab frame.")
#             break

#         # Ensure the process is still running
#         if process.poll() is not None:
#             print("FFmpeg process terminated unexpectedly.")
#             break

#         # Write the frame to FFmpeg's stdin
#         try:
#             process.stdin.write(frame.tobytes())
#         except BrokenPipeError:
#             print("Error: Broken pipe while sending data to FFmpeg.")
#             break
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             break

#         # Optionally, capture FFmpeg output (for debugging purposes)
#         output = process.stdout.readline()
#         if output:
#             print(f"FFmpeg Output: {output.decode('utf-8')}", end="")

#         # Optionally, capture any errors from FFmpeg
#         err_output = process.stderr.readline()
#         if err_output:
#             print(f"FFmpeg Error: {err_output.decode('utf-8')}", end="")

#     # Cleanup
#     cap.release()
#     process.stdin.close()
#     process.stderr.close()
#     process.wait()

# if __name__ == "__main__":
#     try:
#         stream_camera()
#     except Exception as e:
#         print(f"An error occurred: {e}", file=sys.stderr)
