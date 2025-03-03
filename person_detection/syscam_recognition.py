import cv2
from face_recognition_system import FaceRecognitionSystem

def start_realtime_detection(camera_source=0):
    # Initialize the system
    face_system = FaceRecognitionSystem('known_faces')
    
    # Initialize video capture
    cap = cv2.VideoCapture(camera_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
    
    window_name = 'Face Recognition'
    cv2.namedWindow(window_name)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        results = face_system.process_frame(frame)
        
        # Draw results
        for result in results:
            x, y, w, h = result['box']
            name = result['name'] or 'Unknown'
            confidence = result['confidence']
            
            # Draw box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw label with confidence
            label = f"{name} ({confidence:.2%})"
            cv2.putText(frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                       (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow(window_name, frame)
        
        # Break loop on 'q' press or if window is closed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Exit the program
    import sys
    sys.exit(0)

if __name__ == "__main__":
    start_realtime_detection() 