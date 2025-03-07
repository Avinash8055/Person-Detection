System Dependencies (Non-Python)
Ensure these are installed before running the project:

Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Windows 11 SDK, MSVC v142 (or v143) C++ Build tools, CMake tools for Windows: https://cmake.org/download/

Create an output folder for storing results and a video folder for input videos. Then, follow these steps in order:

Run 
  ```sh
  modeltraining.py 
   ```
to train the model.

Run
  ```sh
face_recognition_system.py
   ```
to initialize the recognition system.

Execute 
  ```sh
gputest.py
   ```
to verify if the GPU is activated.

Finally, you can run(any of these):

  ```sh
input_video.py
   ```
  ```sh
realtime_processing.py
   ```
  ```sh
syscam_recognition.py
   ```


