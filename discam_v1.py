import os
import cv2
import time
import tkinter as tk
from tkinter import messagebox

def display_gui_message(message, name):
    root = tk.Tk()
    root.title("DisCam v1")

    label_message = tk.Label(root, text=message, font=("Helvetica", 16))
    label_message.pack(padx=20, pady=10)

    label_name = tk.Label(root, text=f"Made By: {name}", font=("Helvetica", 14))
    label_name.pack(padx=20, pady=10)

    def close_gui():
        root.destroy()

    root.after(5000, close_gui)  # Close the GUI window after 5 seconds
    root.mainloop()

def display_camera_feed(starting_camera_index=0, name="M Harsha Deepan"):
    display_gui_message("DisCam v1", name)

    current_camera_index = starting_camera_index
    working_cameras = []

    # Set the photo directory
    photo_directory = "C:/Discam/Photos/"
    os.makedirs(photo_directory, exist_ok=True)

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

        working_cameras.append(window_name)

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame is read successfully
            if not ret:
                print("Error: Couldn't read frame.")
                break

            # Mirror the frame
            mirrored_frame = cv2.flip(frame, 1)

            # Display the mirrored frame in the corresponding window
            cv2.imshow(window_name, mirrored_frame)

            # Check for key press
            key = cv2.waitKey(1) & 0xFF

            # Take a photo when 'c' key is pressed
            if key == ord('c'):
                photo_filename = os.path.join(photo_directory, f'photo_{time.strftime("%Y%m%d%H%M%S")}.png')
                cv2.imwrite(photo_filename, frame)
                print(f"Photo saved as {photo_filename}")

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

    label_copyright = tk.Label(root, text="Copyright © 2024 M Harsha Deepan.", font=("Helvetica", 12))
    label_copyright.pack(padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    # You can change the starting_camera_index if you have multiple cameras
    # and provide your name as an argument
    display_camera_feed(name="M Harsha Deepan")
