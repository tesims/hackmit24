import cv2
import numpy as np
import mediapipe as mp
import bmf
from fight_move_detector import FightingMoveDetector
from pose_analyzer import PoseAnalyzer
from move_coach import MoveCoach

def process_video(video_path):
    graph = bmf.graph()
    
    # Decode the video
    video = graph.decode({'input_path': video_path})
    
    # Apply the FightingMoveDetector
    detector = FightingMoveDetector(None)
    detected_video = video['video'].module(detector)
    
    # Encode the output
    output_path = 'output.mp4'
    bmf.encode(detected_video, None, {'output_path': output_path}).run()
    
    # Process the output video to count moves
    move_counts = {}
    total_frames = 0
    
    cap = cv2.VideoCapture(output_path)
    pose_analyzer = PoseAnalyzer()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        total_frames += 1
        
        # Convert the frame to RGB (MediaPipe uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform pose estimation
        with mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            # Analyze pose and detect moves
            moves = pose_analyzer.analyze_pose(results.pose_landmarks)
            
            # Count moves
            for move in moves:
                move_counts[move] = move_counts.get(move, 0) + 1
    
    cap.release()
    
    return move_counts, total_frames

def main():
    video_paths = [
        "data/test/action.mp4",
        "data/test/action2.mp4",
        "data/test/action3.mp4"
    ]
    
    for i, video_path in enumerate(video_paths):
        print(f"Processing video {i+1}: {video_path}")
        try:
            move_counts, total_frames = process_video(video_path)
            print(f"Total frames processed: {total_frames}")
            if total_frames > 0:
                for move, count in move_counts.items():
                    print(f"{move}: {count} times ({count/total_frames*100:.2f}%)")
            else:
                print("No frames were processed.")
        except Exception as e:
            print(f"An error occurred: {e}")
        print()

if __name__ == "__main__":
    main()