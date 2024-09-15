import numpy as np
import mediapipe as mp

class PoseAnalyzer:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        
    def analyze_pose(self, pose_landmarks):
        moves = []
        if self.detect_jab(pose_landmarks):
            moves.append("Jab")
        if self.detect_cross(pose_landmarks):
            moves.append("Cross")
        # Add more move detections here
        return moves
    
    def detect_jab(self, pose_landmarks):
        left_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
        
        arm_angle = self.calculate_angle(
            [left_shoulder.x, left_shoulder.y],
            [left_elbow.x, left_elbow.y],
            [left_wrist.x, left_wrist.y]
        )
        return arm_angle > 160 and left_wrist.x > left_shoulder.x and left_shoulder.visibility > 0.8 and left_wrist.visibility > 0.8
    
    def detect_cross(self, pose_landmarks):
        right_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        
        arm_angle = self.calculate_angle(
            [right_shoulder.x, right_shoulder.y],
            [right_elbow.x, right_elbow.y],
            [right_wrist.x, right_wrist.y]
        )
        return arm_angle > 160 and right_wrist.x < right_shoulder.x and right_shoulder.visibility > 0.8 and right_wrist.visibility > 0.8
    
    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180.0:
            angle = 360-angle
        return angle