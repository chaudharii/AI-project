import cv2
import numpy as np

class PoseDetector:
    def __init__(self):
        print("✅ Pose Detection Initialized (Simulated Mode)")

    def get_pose(self, frame):
        """Generate simulated pose landmarks from frame (lightweight)"""
        landmarks = self._get_simulated_pose(frame)
        return landmarks, frame
    
    def _get_simulated_pose(self, frame):
        """Generate simulated landmarks (lightweight, no heavy processing)"""
        landmarks = []
        
        # Fast, lightweight pose simulation without heavy image processing
        
        # Generate standard landmarks
        for i in range(33):
            if i == 0:  # head/nose - top center
                landmarks.append((0.5, 0.2, 0.5))
            elif i == 11:  # left shoulder
                landmarks.append((0.35, 0.35, 0.5))
            elif i == 12:  # right shoulder  
                landmarks.append((0.65, 0.35, 0.5))
            elif i == 13:  # left elbow
                landmarks.append((0.25, 0.45, 0.5))
            elif i == 14:  # right elbow
                landmarks.append((0.75, 0.45, 0.5))
            elif i == 15:  # left wrist
                landmarks.append((0.15, 0.55, 0.5))
            elif i == 16:  # right wrist
                landmarks.append((0.85, 0.55, 0.5))
            elif i == 23:  # left hip
                landmarks.append((0.40, 0.65, 0.5))
            elif i == 24:  # right hip
                landmarks.append((0.60, 0.65, 0.5))
            elif i == 25:  # left knee
                landmarks.append((0.40, 0.80, 0.5))
            elif i == 26:  # right knee
                landmarks.append((0.60, 0.80, 0.5))
            else:
                landmarks.append((0.5, 0.5, 0.5))
        
        return landmarks
