import insightface

recognizer = insightface.app.FaceAnalysis(
    name='buffalo_l',  # Pre-trained model name
    root='./models',  # Where models will be stored
    allowed_modules=['detection', 'recognition']
)
recognizer.prepare(ctx_id=0)  # 0 = GPU, -1 = CPU
