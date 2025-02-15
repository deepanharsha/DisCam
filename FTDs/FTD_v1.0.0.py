import cv2

def take_picture(event, x, y, flags, param):
    captures = param  # Get the camera list from the callback parameter
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, capture in enumerate(captures):
            if capture.isOpened():  # Ensure the camera is still available
                ret, frame = capture.read()
                if ret:
                    file_path = f"captured_image_{i}.jpg"
                    cv2.imwrite(file_path, frame)
                    print(f"Image captured from Camera {i+1} successfully!")

captures = []
index = 0
resolutions = []
while True:
    capture = cv2.VideoCapture(index)
    if not capture.isOpened():
        capture.release()
        break
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resolutions.append((width, height))
    captures.append(capture)
    index += 1

if not captures:
    print("Error: No cameras detected.")
    exit()

print("Dear Developers,\nTo Develop And License This Software,\nPlease Visit: https://github.com/deepanharsha/DisCam/blob/main/LICENSE.md\n")

window_names = [f"Camera {i+1} Feed" for i in range(len(captures))]
for i, window_name in enumerate(window_names):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Allow rescaling
    cv2.resizeWindow(window_name, resolutions[i][0], resolutions[i][1])  # Set to camera's default resolution
    cv2.setMouseCallback(window_name, take_picture, captures)

while True:
    for i, capture in enumerate(captures):
        if capture.isOpened():  # Ensure camera is still available
            ret, frame = capture.read()
            if ret:
                cv2.imshow(window_names[i], cv2.flip(frame, 1))

    if cv2.waitKey(1) == 27:
        break

    closed_indices = [i for i, window_name in enumerate(window_names)
                      if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1]
    for i in reversed(closed_indices):
        if i < len(captures):  # Prevent index errors
            captures[i].release()
            captures.pop(i)
            window_names.pop(i)
            resolutions.pop(i)

    if not captures:
        break

for capture in captures:
    capture.release()
cv2.destroyAllWindows()
