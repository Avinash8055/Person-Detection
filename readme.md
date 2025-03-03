System Dependencies (Non-Python)
Ensure these are installed before running the project:

Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Windows 11 SDK, MSVC v142 (or v143) C++ Build tools, CMake tools for Windows: https://cmake.org/download/

Create an output folder for storing results and a video folder for input videos. Then, follow these steps in order:

1. Run modeltraining.py to train the model.

2. Run face_recognition_system.py to initialize the recognition system.

Execute gputest.py to verify if the GPU is activated.

Finally, you can run(any of these):

[a]input_video.py

[b]realtime_processing.py

[c]syscam_recognition.py

