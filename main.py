import cv2
import sys
from core.detector import EnvironmentDetector
from core.audio import SpatialSonar

def main():
    print("Initializing EnvironmentDetector...")
    try:
        detector = EnvironmentDetector()
    except Exception as e:
        print(f"Failed to load detector: {e}")
        sys.exit(1)
        
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit(1)
        
    # Get frame dimensions to initialize SpatialSonar
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab initial frame. Exiting...")
        sys.exit(1)
        
    height, width, _ = frame.shape
    total_area = width * height
    
    print("Initializing SpatialSonar...")
    sonar = SpatialSonar()
    sonar.start()
        
    print("Webcam opened successfully. Press 'q' in the video window to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
            
        # Get current frame dimensions
        frame_height, frame_width = frame.shape[:2]
        
        # Analyze the frame
        detections = detector.analyze_frame(frame)
        
        # Audio feedback for the closest object
        if detections:
            # Find the single detection with the largest area (closest object)
            closest_obj = max(detections, key=lambda d: d['area'])
            
            # Strict Pan Normalization (-1.0 to 1.0)
            normalized_pan = (closest_obj['x_center'] / (frame_width / 2.0)) - 1.0
            normalized_pan = max(-1.0, min(1.0, normalized_pan))
            
            # Area Normalization (0.0 to 1.0)
            normalized_area = closest_obj['area'] / (frame_width * frame_height)
            normalized_area = max(0.0, min(1.0, normalized_area))
            
            # Update target for continuous spatial audio feedback
            sonar.update_target(target_pan=normalized_pan, target_area=normalized_area)
            
            # Print the closest object for terminal feedback
            print(f"Closest: {closest_obj['class_name']} (pan: {normalized_pan:.2f}, prox: {normalized_area:.2f})")
        else:
            print("No objects detected. Idling...")
            # Send 'idle' values: center pan, and a value that evaluates to 100Hz (area=0.0 means 200Hz, we drop to 0.0 per prompt)
            sonar.update_target(target_pan=0.0, target_area=0.0)
            
        # We need a small window to capture the 'q' key press using OpenCV
        cv2.imshow('Webcam Feed - Press q to quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break
            
    sonar.stop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
