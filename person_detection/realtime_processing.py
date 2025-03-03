import cv2
import numpy as np
from PIL import ImageGrab, Image, ImageTk
from face_recognition_system import FaceRecognitionSystem
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import shutil

class ScreenProcessor:
    def __init__(self):
        self.face_system = FaceRecognitionSystem('known_faces')
        self.is_running = False
        self.writer = None
        self.detected_faces = set()
        self.detection_data = []  # Store detection data
        
        # Create output directories
        self.output_dir = Path("./output")
        self.faces_dir = self.output_dir / "detected_faces"
        self.output_dir.mkdir(exist_ok=True)
        self.faces_dir.mkdir(exist_ok=True)
        
        # Initialize GUI
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Screen Face Detection")
        self.root.geometry("400x500")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Start/Stop button
        self.start_button = ttk.Button(
            main_frame, 
            text="Start Detection", 
            command=self.toggle_detection
        )
        self.start_button.grid(row=0, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Stopped")
        self.status_label.grid(row=1, column=0, pady=5)
        
        # Frame for detected faces
        faces_frame = ttk.LabelFrame(main_frame, text="Detected Faces", padding="5")
        faces_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas for detected faces
        self.faces_canvas = tk.Canvas(faces_frame, width=380, height=400)
        self.faces_canvas.grid(row=0, column=0)
        
        # List to store photo references (prevent garbage collection)
        self.photo_references = []
    
    def save_detected_face(self, frame, x, y, w, h, name, timestamp):
        # Create session directory for this detection run
        if not hasattr(self, 'session_dir'):
            session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_dir = self.output_dir / f"detection_session_{session_timestamp}"
            self.session_dir.mkdir(exist_ok=True)
            self.session_faces_dir = self.session_dir / "faces"
            self.session_faces_dir.mkdir(exist_ok=True)
        
        # Extract and save face region
        face_img = frame[y:y+h, x:x+w]
        filename = f"{name}_{timestamp}.jpg"
        filepath = self.session_faces_dir / filename
        cv2.imwrite(str(filepath), face_img)
        
        # Store detection data
        detection_info = {
            'name': name,
            'timestamp': timestamp,
            'image_path': str(filepath),
            'bbox': [x, y, w, h]
        }
        self.detection_data.append(detection_info)
        
        # Display face in GUI
        self.display_face(face_img, name, timestamp)
        
        return filepath
    
    def display_face(self, face_img, name, timestamp):
        # Convert BGR to RGB
        rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        
        # Resize face image to fit in GUI (maintain aspect ratio)
        height, width = rgb_face.shape[:2]
        max_size = 150
        scale = min(max_size/width, max_size/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_face = cv2.resize(rgb_face, (new_width, new_height))
        
        # Convert to PhotoImage
        pil_image = Image.fromarray(resized_face)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Calculate position for new face image
        num_faces = len(self.photo_references)
        row = num_faces // 2
        col = num_faces % 2
        x_pos = col * 190 + 10
        y_pos = row * 190 + 10
        
        # Add image and label to canvas
        self.faces_canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=photo)
        self.faces_canvas.create_text(
            x_pos + new_width//2,
            y_pos + new_height + 10,
            text=f"{name}\n{timestamp}",
            anchor=tk.N
        )
        
        # Keep reference to prevent garbage collection
        self.photo_references.append(photo)
    
    def save_session_data(self):
        if hasattr(self, 'session_dir'):
            # Save detection data to JSON
            data_file = self.session_dir / 'detection_data.json'
            with open(data_file, 'w') as f:
                json.dump(self.detection_data, f, indent=4)
            
            # Save final video
            if self.writer:
                self.writer.release()
                video_dest = self.session_dir / 'detection_video.mp4'
                shutil.move(self.output_video, video_dest)
            
            # Create session summary
            summary_file = self.session_dir / 'session_summary.txt'
            with open(summary_file, 'w') as f:
                f.write(f"Detection Session Summary\n")
                f.write(f"========================\n")
                f.write(f"Session Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Detections: {len(self.detection_data)}\n\n")
                
                for detection in self.detection_data:
                    f.write(f"Name: {detection['name']}\n")
                    f.write(f"Time: {detection['timestamp']}\n")
                    f.write(f"Image: {detection['image_path']}\n")
                    f.write("-" * 50 + "\n")
    
    def toggle_detection(self):
        if not self.is_running:
            # Start detection
            self.is_running = True
            self.start_button.config(text="Stop Detection")
            self.status_label.config(text="Status: Running")
            
            # Clear previous data
            self.faces_canvas.delete("all")
            self.photo_references.clear()
            self.detected_faces.clear()
            self.detection_data = []
            
            # Create new output file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_video = self.output_dir / f"screen_detection_{timestamp}.mp4"
            
            # Initialize video writer
            screen = np.array(ImageGrab.grab())
            height, width = screen.shape[:2]
            self.writer = cv2.VideoWriter(
                str(self.output_video),
                cv2.VideoWriter_fourcc(*'mp4v'),
                20.0, (width, height)
            )
            
            # Start processing
            self.root.after(100, self.process_screen)
        else:
            # Stop detection and save all data
            self.stop_detection()
            self.save_session_data()
            self.status_label.config(text=f"Status: Saved to {self.session_dir}")
    
    def stop_detection(self):
        self.is_running = False
        self.start_button.config(text="Start Detection")
        
        if self.writer:
            self.writer.release()
            self.writer = None
        
        cv2.destroyAllWindows()
    
    def process_screen(self):
        if not self.is_running:
            return
        
        try:
            screen = np.array(ImageGrab.grab())
            frame = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            results = self.face_system.process_frame(frame)
            
            for result in results:
                x, y, w, h = result['box']
                name = result['name'] or 'Unknown'
                confidence = result['confidence']
                
                if name != 'Unknown' and confidence > 0.5:
                    face_id = f"{name}_{timestamp}"
                    if face_id not in self.detected_faces:
                        self.save_detected_face(frame, x, y, w, h, name, timestamp)
                        self.detected_faces.add(face_id)
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                label = f"{name} ({confidence:.2%})"
                cv2.putText(frame, label, (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           (0, 255, 0), 2)
            
            if self.writer:
                self.writer.write(frame)
            
            cv2.imshow('Live Face Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_detection()
                return
            
            self.root.after(1, self.process_screen)
            
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            self.stop_detection()
    
    def run(self):
        try:
            self.root.mainloop()
        finally:
            if self.writer:
                self.writer.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = ScreenProcessor()
    processor.run() 