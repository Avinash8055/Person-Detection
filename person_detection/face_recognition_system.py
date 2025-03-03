import cv2
import numpy as np
import torch
import insightface
import onnxruntime
from facenet_pytorch import MTCNN
from datetime import datetime
from pathlib import Path
import re

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir, detection_threshold=0.6, recognition_threshold=0.5, use_gpu=True):
        try:
            # Initialize InsightFace app with more lenient detection settings
            self.recognizer = insightface.app.FaceAnalysis(
                name='buffalo_l',
                root='./models',
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider'] if use_gpu else ['CPUExecutionProvider'],
                allowed_modules=['detection', 'recognition'],
                det_size=(640, 640)  # Larger detection size for better angle coverage
            )
            self.recognizer.prepare(ctx_id=0 if use_gpu else -1)
        except Exception as e:
            print(f"Error initializing InsightFace model: {str(e)}")
            raise RuntimeError(f"Failed to initialize face recognition model: {str(e)}")
        
        # Adjust thresholds for better angle tolerance
        self.detection_threshold = detection_threshold
        self.recognition_threshold = recognition_threshold * 0.8  # More lenient recognition threshold
        
        # Load known faces
        self.known_faces = self._load_known_faces(known_faces_dir)
    
    def _load_known_faces(self, known_faces_dir):
        known_faces = {}
        known_faces_path = Path(known_faces_dir)
        
        print("\nLoading known faces:")
        name_pattern = re.compile(r'(.+?)(?:_\w+)?\.(?:jpg|jpeg|png)$', re.IGNORECASE)
        
        for face_img_path in known_faces_path.glob("*.[jp][pn][g]"):
            match = name_pattern.match(face_img_path.name)
            if not match:
                continue
            
            base_name = match.group(1)
            print(f"- Loading {face_img_path.name} for {base_name}")
            
            img = cv2.imread(str(face_img_path))
            faces = self.recognizer.get(img)
            
            if len(faces) > 0:
                embedding = faces[0].embedding
                if base_name not in known_faces:
                    known_faces[base_name] = []
                known_faces[base_name].append(embedding)
                print(f"  Successfully loaded {face_img_path.name}")
        
        # Add summary at the end
        print("\nSummary of loaded faces:")
        for name, embeddings in known_faces.items():
            print(f"- {name}: {len(embeddings)} angles loaded")
        
        return known_faces
    
    def process_frame(self, frame):
        # Process frame using InsightFace
        faces = self.recognizer.get(frame)
        
        results = []
        for face in faces:
            # Get face coordinates
            bbox = face.bbox.astype(int)
            x1, y1, x2, y2 = bbox
            
            # Get embedding and find best match
            embedding = face.embedding
            best_match = None
            best_score = 0
            
            # Compare with all known faces
            for name, embeddings_list in self.known_faces.items():
                # Calculate similarity with all angles of this person
                for known_embedding in embeddings_list:
                    score = np.dot(embedding, known_embedding) / (
                        np.linalg.norm(embedding) * np.linalg.norm(known_embedding)
                    )
                    if score > best_score and score > self.recognition_threshold:
                        best_score = score
                        best_match = name
            
            # Only append results if we have a match or want to show unknown faces
            if best_match or self.detection_threshold > 0:
                results.append({
                    'box': (x1, y1, x2-x1, y2-y1),  # Convert to (x,y,w,h) format
                    'name': best_match if best_match else 'Unknown',
                    'confidence': best_score
                })
                
        return results 