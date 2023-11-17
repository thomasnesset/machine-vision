import tkinter as tk
from tkinter import filedialog
import shutil
import cv2
import time
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Open the default camera (index 0)
        self.cap = cv2.VideoCapture(0)

        # Create a canvas to display the webcam feed
        self.canvas = tk.Canvas(window, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # Create a label to display the selected file path
        self.label = tk.Label(window, text="No file selected", padx=10, pady=10)
        self.label.pack()

        # Create a frame to center the buttons
        self.button_frame = tk.Frame(window)
        self.button_frame.pack(pady=10)

        # Create a button to open the file dialog
        self.button_upload = tk.Button(self.button_frame, text="Upload ID", command=self.open_file_dialog)
        self.button_upload.pack(side=tk.LEFT, padx=10)

        # Create a button to take a snapshot
        self.button_snapshot = tk.Button(self.button_frame, text="Take Snapshot", command=self.take_snapshot)
        self.button_snapshot.pack(side=tk.LEFT, padx=10)

        # After initializing the GUI components, start the webcam feed
        self.update()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            # Copy the selected file to the current working directory
            filename = file_path.split("/")[-1]  # Extract the filename
            destination_path = "./" + filename  # Destination path in the current directory
            shutil.copy(file_path, destination_path)

            self.label.config(text="File Path: " + destination_path)
        else:
            self.label.config(text="No file selected")

    def take_snapshot(self):
        # Capture a single frame
        ret, frame = self.cap.read()

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL ImageTk object from the frame
        image = Image.fromarray(frame_rgb)
        self.photo = ImageTk.PhotoImage(image)

        # Display the snapshot on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Save the snapshot to a file in the current working directory (you can customize the filename)
        snapshot_path = "./snapshot.png"
        image.save(snapshot_path)

        # Check if the ID matches the person in the snapshot (replace this with your actual function)
        result = self.check_id_match(snapshot_path)

        # Update the result text
        if result:
            self.label.config(text="ID matches!")
        else:
            self.label.config(text="ID does not match!")

    def check_id_match(self, snapshot_path):
        self.label.config(text="Processing...")
        # Replace this function with your actual implementation to check if the ID matches the person
        # This is just a placeholder
        # You can use face recognition libraries or any other method to perform the actual matching
        time.sleep(2)
        return True

    def update(self):
        # Get a frame from the webcam
        ret, frame = self.cap.read()

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL ImageTk object from the frame
        self.photo = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

        # Update the canvas with the new frame
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Schedule the update method to be called after 10 milliseconds
        self.window.after(10, self.update)

    def __del__(self):
        # Release the camera when the object is deleted
        if self.cap.isOpened():
            self.cap.release()

# Create the main window and the WebcamApp instance
app_window = tk.Tk()
app = WebcamApp(app_window, "Identity Verification")

# Start the main loop
app_window.mainloop()
