import os
import cv2
import time
import tkinter as tk
from tkinter import messagebox

def display_gui_message(message, name):
    root = tk.Tk()
    root.title("DisCam v1.1 Release")

    label_message = tk.Label(root, text=message, font=("Helvetica", 16))
    label_message.pack(padx=20, pady=10)

    label_name = tk.Label(root, text=f"Made By: {name}", font=("Helvetica", 14))
    label_name.pack(padx=20, pady=10)

    def close_gui():
        root.destroy()

    root.after(5000, close_gui)  # Close the GUI window after 2 seconds
    root.mainloop()

def detect_face(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return len(faces) > 0

def display_camera_feed(starting_camera_index=0, name="Your Name"):
    display_gui_message("DisCam v1.1 Release", name)

    current_camera_index = starting_camera_index
    working_cameras = []

    # Get the path to the user's Pictures\Discam directory
    photo_directory = os.path.expanduser(os.path.join('~', 'Pictures', 'Discam'))

    # Create the directory if it doesn't exist
    os.makedirs(photo_directory, exist_ok=True)

    # Flag to toggle face detection
    face_detection_enabled = False

    # Timer for face detection pictures
    last_face_detection_time = time.time()

    # Function to handle mouse events
    def on_mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button down
            take_photo()

    # Function to take a photo
    def take_photo():
        nonlocal photo_directory
        photo_filename = os.path.join(photo_directory, f'photo_{time.strftime("%Y%m%d%H%M%S")}.png')
        cv2.imwrite(photo_filename, frame)
        print(f"Photo saved as {photo_filename}")

    while True:
        # Open the camera
        cap = cv2.VideoCapture(current_camera_index)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            print(f"Error: Couldn't open camera with index {current_camera_index}. Trying the next index.")
            current_camera_index += 1
            if current_camera_index > 2:  # Assuming you have 3 cameras, you can adjust this number
                print("Error: All camera indices failed. Exiting.")
                break
            continue

        # Create a window for the current camera
        window_name = f'Camera {current_camera_index}'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        # Set the window size to 800x600
        cv2.resizeWindow(window_name, 800, 600)

        # Set mouse event callback
        cv2.setMouseCallback(window_name, on_mouse_event)

        working_cameras.append(window_name)

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame is read successfully
            if not ret:
                print("Error: Couldn't read frame.")
                break

            # Mirror the frame horizontally
            frame = cv2.flip(frame, 1)

            # Display the frame in the corresponding window
            cv2.imshow(window_name, frame)

            # Check for key press
            key = cv2.waitKey(1) & 0xFF

            # Toggle face detection on/off when 'f' key is pressed
            if key == ord('f'):
                face_detection_enabled = not face_detection_enabled
                print("Face detection enabled" if face_detection_enabled else "Face detection disabled")

            # If face detection is enabled and a face is detected, take a photo
            if face_detection_enabled and time.time() - last_face_detection_time >= 3 and detect_face(frame):
                print("Face detected, taking photo...")
                take_photo()
                last_face_detection_time = time.time()

            # Take a photo when 'c' key is pressed
            elif key == ord('c'):
                take_photo()

            # Break the loop if Esc key is pressed
            elif key == 27:
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyWindow(window_name)

        # Break the outer loop if Esc key is pressed
        if key == 27:
            break

        current_camera_index += 1
        if current_camera_index > 2:  # Assuming you have 3 cameras, you can adjust this number
            print("Error: All camera indices failed. Exiting.")
            break

    # Display copyright message after closing the camera feed
    root = tk.Tk()
    root.title("Copyright")

    label = tk.Label(root, text="Copyright © 2024 M Harsha Deepan.", font=("Helvetica", 12))
    label.pack(padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    # You can change the starting_camera_index if you have multiple cameras
    # and provide your name as an argument
    display_camera_feed(name="M Harsha Deepan at https://github.com/deepanharsha")
