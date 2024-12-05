import cv2
import socket
import time

# Set up the UDP socket for streaming
server_ip = 'inz.local'  # Change this to the client's IP address
server_port = 12346
server_address = (server_ip, server_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open the camera capture (use `0` for the default camera)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Set the frame width and height for the camera
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# H.264 encoding setup using FFmpeg (make sure FFmpeg is installed)
fourcc = cv2.VideoWriter_fourcc(*'H264')  # H.264 codec or 'avc1'
fps = 30  # Frames per second

# VideoWriter to write H.264 encoded frames
# This uses FFmpeg's 'h264' codec for real-time encoding
output = cv2.VideoWriter(
    'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay ! udpsink host=192.168.0.154 port=12346',
    cv2.CAP_GSTREAMER, 0, fps, (frame_width, frame_height)
)

# Start streaming the video
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    print(len(frame.tobytes())) 
    # Send the frame over UDP (H.264 encoded)
    cv2.imshow("Live Video Feed", frame) 

    output.write(frame) 


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
sock.close()
cv2.destroyAllWindows()
