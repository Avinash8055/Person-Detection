import cv2
from face_recognition_system import FaceRecognitionSystem
from pathlib import Path
from datetime import datetime, timedelta
def format_video_time(frame_number, fps):
    """Convert frame number to video timestamp"""
    seconds = frame_number / fps
    return f"{int(seconds//60):02d}:{int(seconds%60):02d}"

def process_video(video_path, output_path=None):
    # Check if video file exists
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Create output directory if it doesn't exist
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    
    # If no output path provided, create one with timestamp
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"detected_output_{timestamp}.mp4"
    
    # Initialize the system
    face_system = FaceRecognitionSystem('known_faces')
    
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    frame_count = 0
    detections_log = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        video_time = format_video_time(frame_count, fps)
        
        # Process frame
        results = face_system.process_frame(frame)
        
        # Draw results
        for result in results:
            x, y, w, h = result['box']
            name = result['name'] or 'Unknown'
            confidence = result['confidence']
            
            # Draw box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw label with confidence and video timestamp
            label = f"{name} ({video_time})"
            cv2.putText(frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                       (0, 255, 0), 2)
            
            # Log detection with video timestamp
            if name != 'Unknown':
                detections_log.append(f"[{video_time}] Detected {name}")
        
        # Write frame
        writer.write(frame)
        
        # Show frame while processing
        cv2.imshow('Processing Video', frame)
        
        # Allow early exit with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    
    # Save detection log with video timestamps
    log_path = output_dir / f"detections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_path, 'w') as f:
        f.write("Video Detection Log\n")
        f.write("==================\n")
        f.write(f"Video: {video_path}\n")
        f.write(f"Total Frames: {frame_count}\n")
        f.write(f"Video Duration: {format_video_time(frame_count, fps)}\n\n")
        f.write("Detections:\n")
        f.write("-----------\n")
        for log_entry in detections_log:
            f.write(f"{log_entry}\n")
    
    return str(output_path), str(log_path)

if __name__ == "__main__":
    video_path = "./video/videotrailer.mp4"
    
    try:
        output_video, output_log = process_video(video_path)
        print(f"Processing complete.")
        print(f"Output video saved to: {output_video}")
        print(f"Detection log saved to: {output_log}")
    except Exception as e:
        print(f"Error during processing: {str(e)}") 