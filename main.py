import cv2
import sys
from core.detector import EnvironmentDetector

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
        
    print("Webcam opened successfully. Press 'q' in the video window to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
            
        # Analyze the frame
        detections = detector.analyze_frame(frame)
        
        # Print the detections
        if detections:
            # Format output for readability
            detected_items = [f"{d['class_name']} (x-center: {d['x_center']:.1f}, area: {d['area']:.1f})" for d in detections]
            print(" | ".join(detected_items))
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
