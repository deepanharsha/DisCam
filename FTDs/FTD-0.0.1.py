import cv2

# Function to take a picture when the mouse is clicked
def take_picture(event, x, y, flags, param):
    global captures
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, capture in enumerate(captures):
            ret, frame = capture.read()
            if ret:
                file_path = f"captured_image_{i}.jpg"
                cv2.imwrite(file_path, frame)
                print(f"Image captured from camera {i+1} successfully!")

# Initialize a list to hold captures for all available cameras
captures = []

# Get the number of available cameras
num_cameras = 0
for i in range(10):
    capture = cv2.VideoCapture(i)
    if capture.isOpened():
        num_cameras += 1
        captures.append(capture)
    else:
        break

# Check if at least one camera is available
if num_cameras == 0:
    print("Error: No cameras detected.")
    exit()

# Print the message for developers
print("Dear Developers,\nTo Develop And License This Software,\nPlease Visit: https://github.com/deepanharsha/DisCam/blob/main/LICENSE.md\n")

# Calculate number of rows and columns for window arrangement
num_rows = num_cameras // 2 + num_cameras % 2
num_cols = 2 if num_cameras >= 2 else 1

# Create windows for each camera feed
window_names = []
for i, capture in enumerate(captures):
    window_name = f"Camera {i+1} Feed"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, take_picture)
    window_names.append(window_name)

while True:
    # Read frame from each camera and display in corresponding window
    for i, capture in enumerate(captures):
        ret, frame = capture.read()
        if ret:
            window_name = window_names[i]
            frame = cv2.flip(frame, 1)  # Flip horizontally for mirrored view
            cv2.imshow(window_name, frame)

    # Check for key press or window closure
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break

    # Check if any window is closed
    for i, window_name in enumerate(window_names):
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            captures[i].release()
            captures.pop(i)
            window_names.pop(i)

    # Break the loop if all windows are closed
    if not captures:
        break

# Close all windows
cv2.destroyAllWindows()
