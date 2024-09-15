import cv2
import numpy as np
import mediapipe as mp
import bmf 
from pose_analyzer import PoseAnalyzer
from move_coach import MoveCoach

class FightingMoveDetector(bmf.Module):
    def __init__(self, node, option=None):
        self.node = node
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='data/training/pose_landmarker_lite.task'),
            running_mode=VisionRunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.landmarker = PoseLandmarker.create_from_options(options)
        
        self.pose_analyzer = PoseAnalyzer()
        self.move_coach = MoveCoach()
        self.frame_timestamp = 0
    
    def process(self, task):
        for packet in task.get_inputs()[0]:
            if packet.timestamp == bmf.Timestamp.EOF:
                task.timestamp = bmf.Timestamp.EOF
                return bmf.ProcessResult.OK
            
            frame = packet.get(bmf.VideoFrame).numpy()
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            
            pose_landmarker_result = self.landmarker.detect_for_video(mp_image, self.frame_timestamp)
            self.frame_timestamp += 33  # Assuming 30 fps, adjust as needed
            
            if pose_landmarker_result.pose_landmarks:
                landmarks = pose_landmarker_result.pose_landmarks[0]
                moves = self.pose_analyzer.analyze_pose(landmarks)
                
                advice = self.move_coach.generate_advice(moves)
                
                self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_pose.POSE_CONNECTIONS)
                cv2.putText(frame, f"Detected: {', '.join(moves)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                y_offset = 60
                for line in advice.split(" | "):
                    cv2.putText(frame, f"Advice: {line}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    y_offset += 30
            
            output_frame = bmf.VideoFrame(frame)
            task.get_outputs()[0].put(output_frame)
        
        return bmf.ProcessResult.OK