System Dependencies (Non-Python)
Ensure these are installed before running the project:
Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

1.Windows 11 SDK

2.MSVC v142 (or v143) C++ Build tools

3.CMake tools for Windows: https://cmake.org/download/

Create an output folder for storing results and a video folder for input videos. Then, follow these steps in order:

Run modeltraining.py to train the model.

Run face_recognition_system.py to initialize the recognition system.

Execute gputest.py to verify if the GPU is activated.

Finally, you can run(any of these):
input_video.py
realtime_processing.py
syscam_recognition.py

This ensures everything is set up correctly before processing videos in real time.
