import torch
import cv2
import insightface
from facenet_pytorch import MTCNN
from pathlib import Path

def test_setup():
    print("Testing CUDA availability:", torch.cuda.is_available())
    print("CUDA device count:", torch.cuda.device_count())
    if torch.cuda.is_available():
        print("CUDA device name:", torch.cuda.get_device_name(0))
    
    print("\nTesting MTCNN...")
    try:
        detector = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
        print("MTCNN initialized successfully")
    except Exception as e:
        print("MTCNN error:", str(e))
    
    print("\nTesting InsightFace...")
    try:
        # Initialize InsightFace app
        app = insightface.app.FaceAnalysis(
            name='buffalo_l',
            root='./models',  # Point to the models directory
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider'],
            allowed_modules=['detection', 'recognition']
        )
        app.prepare(ctx_id=0 if torch.cuda.is_available() else -1)
        print("InsightFace model loaded successfully")
        
        # Test with a sample image if available
        test_image_path = Path('known_faces').glob('*.[jp][pn][g]')
        test_image = next(test_image_path, None)
        if test_image:
            print("\nTesting face detection with sample image...")
            img = cv2.imread(str(test_image))
            faces = app.get(img)
            print(f"Detected {len(faces)} faces in sample image")
            
    except Exception as e:
        print("InsightFace error:", str(e))
        print("Detailed error info:", str(type(e)))

if __name__ == "__main__":
    test_setup()
