import tkinter as tk
from tkinter import filedialog
import shutil
import cv2
import recognition
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.cap = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(window, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        self.label = tk.Label(window, text="No file selected", padx=10, pady=10)
        self.label.pack()

        self.button_frame = tk.Frame(window)
        self.button_frame.pack(pady=10)

        self.button_upload = tk.Button(self.button_frame, text="Upload ID", command=self.open_file_dialog)
        self.button_upload.pack(side=tk.LEFT, padx=10)

        self.button_snapshot = tk.Button(self.button_frame, text="Take Snapshot", command=self.take_snapshot)
        self.button_snapshot.pack(side=tk.LEFT, padx=10)

        self.update()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            destination_path = "./id.jpg"
            shutil.copy(file_path, destination_path)

            self.label.config(text="ID loaded")
        else:
            self.label.config(text="No file selected")

    def take_snapshot(self):
        ret, frame = self.cap.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame_rgb)
        self.photo = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        snapshot_path = "./snapshot.png"
        image.save(snapshot_path)

        result = self.check_id_match()

        if result:
            self.label.config(text="ID matches!")
        else:
            self.label.config(text="ID does not match!")

    def check_id_match(self):
        self.label.config(text="Processing...")
        
        return recognition.match_id_face("./id.jpg", "./snapshot.jpg")

    def update(self):
        ret, frame = self.cap.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.photo = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.window.after(10, self.update)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

app_window = tk.Tk()
app = App(app_window, "Identity Verification")

app_window.mainloop()
