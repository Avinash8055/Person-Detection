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
Before proceeding, clone the repository and create the necessary directories:  

### 🔹 **Clone the Repository**  
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

- **`output/`** → For storing results  
- **`video/`** → For input videos  
- **`known_faces/`** → Add images of known individuals here before running the recognition system.

### 🚀 **Running the Project** 

🔹 **Step 0: Install Dependencies**  

Before running the project, install the required Python packages:  

```bash
pip install -r requirements.txt
```

🔹 **Step 1: Train the Model**
```sh
python modeltraining.py
```
**🔹 Step 2: Add Known Faces**

Before running the face recognition system, add images of known individuals inside the known_faces/ folder. This ensures the system can identify them during recognition.

**🔹 Step 3: Initialize the Recognition System**
```sh
python face_recognition_system.py
```
**🔹 Step 4: Verify GPU Activation (Optional but Recommended)**
```sh
python gputest.py
```
**🔹 Step 5: Run the Recognition System**

You can run any of the following based on your use case:

For video input:
```sh
python input_video.py
```
For real-time processing:
```sh
python realtime_processing.py
```
For system camera recognition:
```sh
python syscam_recognition.py
```


