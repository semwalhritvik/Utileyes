import cv2
import numpy as np
from ultralytics import YOLO

class EnvironmentDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
    
    def analyze_frame(self, frame: np.ndarray):
        # Run inference directly on frame in memory
        results = self.model(frame)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Calculate X-center
                x_center = (x1 + x2) / 2
                
                # Calculate area to represent proximity
                width = x2 - x1
                height = y2 - y1
                area = width * height
                
                # Get class name
                cls_id = int(box.cls[0].item())
                class_name = result.names[cls_id]
                
                detections.append({
                    'class_name': class_name,
                    'bbox': [x1, y1, x2, y2],
                    'x_center': x_center,
                    'area': area
                })
                
        # Sort based on X-center from left to right
        detections.sort(key=lambda d: d['x_center'])
        
        return detections
