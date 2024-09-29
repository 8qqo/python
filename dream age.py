import cv2
import time
from datetime import datetime

url = 'https://cctv4.kctmc.nat.gov.tw/fcd4f79a/'
cap = cv2.VideoCapture(url)

# Set properties for smoother streaming
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Buffering frames for smoother playback

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        time.sleep(2)
        cap = cv2.VideoCapture(url)
        continue

    # Resize the frame to a reasonable size for processing
    resized_frame = cv2.resize(frame, (640, 360))  # Adjust as needed

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
    
    cv2.imshow('oxxostudio', resized_frame)

    # Calculate delay to achieve 60 FPS (adjust as needed)
    elapsed_time = time.time() - start_time
    delay = max(1, int((1 /60 - elapsed_time) * 1000))  # Targeting 60 FPS
    if cv2.waitKey(delay) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
