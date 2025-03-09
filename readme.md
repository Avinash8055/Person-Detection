## ⚙️ System Dependencies (Non-Python)  

Before running the project, ensure the following dependencies are installed:  

### 🔧 **Required Tools**  
- **[Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)**  
- **Windows 11 SDK, MSVC v142 (or v143) C++ Build Tools, CMake Tools for Windows**  
  - These can be installed via the **Visual Studio Installer**:  
    1. Open **Visual Studio Installer** (Download from [here](https://visualstudio.microsoft.com/downloads/) if not installed).  
    2. Select **Modify** on your installed version of Visual Studio.  
    3. Under **Workloads**, choose **Desktop development with C++**.  
    4. In the **Individual Components** tab, ensure the following are checked:  
       - **Windows 11 SDK**  
       - **MSVC v142 (or v143) C++ Build Tools**  
       - **CMake Tools for Windows**  
    5. Click **Modify** to install the required components.  

### 📂 **Folder Setup**  
Before proceeding, create the following directories:  
- **`output/`** → For storing results  
- **`video/`** → For input videos  

Once everything is set up, follow these steps **in order** to ensure a smooth workflow. 🚀  



**Run** 
  ```sh
  modeltraining.py 
   ```
to train the model.

**Run**
  ```sh
face_recognition_system.py
   ```
to initialize the recognition system.

**Execute** 
  ```sh
gputest.py
   ```
to verify if the GPU is activated.

**Finally, you can run(any of these):**

  ```sh
input_video.py
   ```
  ```sh
realtime_processing.py
   ```
  ```sh
syscam_recognition.py
   ```


