import cv2
import time
import threading
from datetime import datetime

# URLs for video streams
urls = [
    'https://cctv6.kctmc.nat.gov.tw/7f82a59c/',
    'https://cctv1.kctmc.nat.gov.tw/02f22e11/',
    'https://cctv4.kctmc.nat.gov.tw/c9653df7/',
    'https://cctv6.kctmc.nat.gov.tw/abc0307a/',
    'https://cctv6.kctmc.nat.gov.tw/ae6689ba/?t=1695677315361',
    'https://cctv1.kctmc.nat.gov.tw/6e559e58/?t=1695677229521',
    'https://cctv6.kctmc.nat.gov.tw/abc0307b/?t=1695676989659',
    'https://cctv6.kctmc.nat.gov.tw/d5ce1b72/'
]

# Initialize video capture for each URL
caps = [cv2.VideoCapture(url) for url in urls]

# Set properties for smoother streaming
for cap in caps:
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 8)  # Buffering frames for smoother playback

# Check if cameras are opened successfully
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Cannot open camera for URL: {urls[i]}")
        exit()

# Define window size for display
window_width, window_height = 480, 360

# Function to read and display frames from a capture object
def read_and_display(cap, window_name):
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Cannot receive frame from camera: {window_name}")
            time.sleep(2)
            break
        
        # Resize the frame to the specified window size
        resized_frame = cv2.resize(frame, (window_width, window_height))

        # Get current date and time
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Put the current time on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = 0.5
        text_color = (255, 255, 255)  # White color
        text_thickness = 1
        text = current_time

        # Calculate the text position to be at the bottom right corner
        text_size_tuple, _ = cv2.getTextSize(text, font, text_size, text_thickness)
        text_x = resized_frame.shape[1] - text_size_tuple[0] - 10
        text_y = resized_frame.shape[0] - 10

        cv2.putText(resized_frame, text, 
                    (text_x, text_y), 
                    font, 
                    text_size,
                    text_color,
                    text_thickness)
        
        # Display the processed frame in the corresponding window
        cv2.imshow(window_name, resized_frame)

        # Wait for a key press to quit
        if cv2.waitKey(1) == ord('q'):
            break

# Create threads for each video capture
threads = []
for i, cap in enumerate(caps):
    thread = threading.Thread(target=read_and_display, args=(cap, f'oxxostudio_{i}'))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Release video captures and close all windows
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
