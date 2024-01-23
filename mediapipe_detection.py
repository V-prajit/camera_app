#Importing The Required Libraries
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk

# Function to calculate angle with 90 degrees as 0
def calculate_angle(a, b, c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.degrees(radians)

    if angle < 0:
        angle += 360

    # Adjusting the angle so that 90 degrees becomes 0
    adjusted_angle = angle - 90

    # Handling angles greater than 180 degrees (making sure they fall within the -90 to +90 range)
    if adjusted_angle > 90:
        adjusted_angle -= 180
    elif adjusted_angle < -90:
        adjusted_angle += 180

    return adjusted_angle


# Function to process pose
def process_pose(frame):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    l_angle = 0
    r_angle = 0

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark
        
        l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        
        r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        
        l_angle = calculate_angle(l_elbow, l_shoulder, l_hip)
        r_angle = -(calculate_angle(r_elbow, r_shoulder, r_hip))

        cv2.putText(image, f"L Angle: {int(l_angle)}", 
                    tuple(np.multiply(l_elbow, [frame.shape[1], frame.shape[0]]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
        cv2.putText(image, f"R Angle: {int(r_angle)}", 
                    tuple(np.multiply(r_elbow, [frame.shape[1], frame.shape[0]]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    except:
        pass

    pose.close()
    return image, l_angle, r_angle

# Main Application
class ArmDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize min and max angles for both arms
        self.l_min_angle, self.l_max_angle = float('inf'), float('-inf')
        self.r_min_angle, self.r_max_angle = float('inf'), float('-inf')

        # Button to choose video file
        self.btn_choose_video = tk.Button(window, text="Choose Video", width=15, command=self.open_video_file)
        self.btn_choose_video.pack(pady=5)

        # Label for video
        self.video_label = tk.Label(window)
        self.video_label.pack()

        self.cap = None

        self.window.mainloop()

    def open_video_file(self):
        self.video_path = filedialog.askopenfilename(title="Select Video File", 
                                                     filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")])
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.update_video_frame()

    def update_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            processed_frame, l_angle, r_angle = process_pose(frame)
            self.update_angle_records(l_angle, r_angle)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)))
            self.video_label.config(image=self.photo)
            self.window.after(33, self.update_video_frame)
        else:
            self.cap.release()
            self.display_angle_summary()

    def update_angle_records(self, l_angle, r_angle):
        # Update left arm angles
        if l_angle < self.l_min_angle:
            self.l_min_angle = l_angle
        if l_angle > self.l_max_angle:
            self.l_max_angle = l_angle

        # Update right arm angles
        if r_angle < self.r_min_angle:
            self.r_min_angle = r_angle
        if r_angle > self.r_max_angle:
            self.r_max_angle = r_angle

    def display_angle_summary(self):
        summary = f"Left Arm - Min Angle: {int(self.l_min_angle)}, Max Angle: {int(self.l_max_angle)}\n"
        summary += f"Right Arm - Min Angle: {int(self.r_min_angle)}, Max Angle: {int(self.r_max_angle)}"
        messagebox.showinfo("Angle Summary", summary)

# Create a window and pass it to the Application object
ArmDetectionApp(tk.Tk(), "Arm Detection with MediaPipe")
