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
    sonar = SpatialSonar(frame_width=width)
        
    print("Webcam opened successfully. Press 'q' in the video window to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
            
        # Analyze the frame
        detections = detector.analyze_frame(frame)
        
        # Audio feedback for the closest object
        if detections:
            # Find the detection with the largest area (closest object)
            closest_obj = max(detections, key=lambda d: d['area'])
            
            # Calculate normalized area (0.0 to 1.0)
            normalized_area = closest_obj['area'] / total_area
            
            # Play spatial audio feedback
            sonar.play_feedback(closest_obj['x_center'], normalized_area)
            
            # Print the closest object for terminal feedback
            print(f"Closest: {closest_obj['class_name']} (pan: {closest_obj['x_center']:.1f}, prox: {normalized_area:.2f})")
        else:
            print("No objects detected.")
            
        # We need a small window to capture the 'q' key press using OpenCV
        cv2.imshow('Webcam Feed - Press q to quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
