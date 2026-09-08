# 🪄 Invisible Cloath Using AI

### 🤖 Real-Time Computer Vision Based Invisible Cloak Effect Using Python, OpenCV & NumPy
<img width="540" height="540" alt="InvisibilityGIFbygifnews" src="https://github.com/user-attachments/assets/5506b0a9-c2fa-427c-bbe9-67f0c9aa17b4" />


---

## 📌 Project Overview

**Invisible Cloath Using AI** is a real-time Computer Vision project that creates an **invisible cloak visual effect** using a webcam.

The application captures the background before the user enters the camera view. When the user appears with a **blue-colored cloth**, the system detects the blue region in real time using **HSV color segmentation** and replaces the detected region with the previously captured background.

This creates the illusion that the blue cloth has become invisible. 🪄✨

The project demonstrates how **Artificial Intelligence concepts, Computer Vision, image processing, and real-time video processing** can be combined to create an interactive application.

---

## 🎯 Project Objective

The main objective of this project is to develop a real-time application capable of:

* 🎥 Capturing live webcam video
* 🖼️ Capturing and storing the background
* 🎨 Detecting a blue-colored cloth
* 🧠 Processing the detected region
* 🎭 Replacing the cloth region with the background
* ✨ Creating an invisible-cloak visual effect
* ⚡ Processing everything in real time

---

# ✨ Key Features

### 🎥 Real-Time Webcam Processing

The application continuously receives frames from the webcam and processes them using OpenCV.

### 🖼️ Background Capture

Before using the cloak, the system captures the background.

Multiple frames can be used to create a more stable background instead of relying on only one frame.

### 🎨 Blue Cloth Detection

The application detects the blue cloak using the **HSV color space**.

HSV makes color-based segmentation easier because it separates:

* Hue
* Saturation
* Brightness

### 🎭 Mask Generation

After detecting the blue region, a binary mask is generated.

```text
White → Detected cloak
Black → Remaining scene
```

### 🧹 Morphological Processing

Morphological operations are applied to improve the mask and reduce unwanted noise.

Operations include:

* Erosion
* Dilation
* Opening
* Closing

### 🔎 Noise Removal

Small unwanted regions can be removed from the mask to improve the detected cloak area.

### 🌫️ Mask Refinement

The mask can be processed and smoothed to produce cleaner cloak boundaries.

### 🔄 Temporal Stabilization

Frame-to-frame changes can cause flickering.

Temporal mask processing helps provide a smoother visual effect.

### 🎯 Color Calibration

Different cameras and lighting conditions can produce different blue values.

The project can use calibration to obtain more suitable HSV values for the actual cloak.

### 📊 FPS Monitoring

Real-time FPS information can be displayed to understand application performance.

---

# 🧠 How It Works

The complete process follows this pipeline:

```text
              🎥 Webcam
                  │
                  ▼
        🖼️ Capture Background
                  │
                  ▼
          📹 Capture Live Frame
                  │
                  ▼
             BGR → HSV
                  │
                  ▼
          🎨 Detect Blue Cloth
                  │
                  ▼
             Create Mask
                  │
                  ▼
       🧹 Remove Mask Noise
                  │
                  ▼
       🔎 Morphological Processing
                  │
                  ▼
        🌫️ Refine / Smooth Mask
                  │
                  ▼
      🔄 Replace Blue Region
        With Background
                  │
                  ▼
          ✨ Final Frame
                  │
                  ▼
             🖥️ Display
```

---

# 🔬 Computer Vision Pipeline

## 1. Webcam Initialization

The webcam is opened using OpenCV.

```python
cap = cv2.VideoCapture(0)
```

The camera continuously provides frames to the application.

---

## 2. Background Capture

The application first captures the scene without the blue cloak.

Example:

```text
Empty Scene
     ↓
Capture Multiple Frames
     ↓
Build Background
     ↓
Store Background
```

The captured background is later used to replace the cloak region.

---

## 3. BGR to HSV Conversion

OpenCV captures webcam frames in BGR format.

The frame is converted to HSV:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV consists of:

| Channel | Description |
| ------- | ----------- |
| H       | Hue / Color |
| S       | Saturation  |
| V       | Brightness  |

---

## 4. Blue Color Segmentation

The application defines an HSV range for blue.

The blue region is extracted using:

```python
mask = cv2.inRange(hsv, lower_blue, upper_blue)
```

This creates a binary mask.

```text
Blue pixels       → White
Other pixels      → Black
```

---

## 5. Morphological Operations

The initial mask may contain small unwanted regions.

Morphological processing improves the mask.

### Opening

Used primarily for removing small noise.

```text
Erosion → Dilation
```

### Closing

Used primarily for filling small gaps.

```text
Dilation → Erosion
```

---

## 6. Mask Refinement

The mask can be refined using:

* Noise filtering
* Connected-component filtering
* Smoothing
* Edge refinement
* Temporal stabilization

This helps make the final effect visually cleaner.

---

## 7. Background Replacement

The detected blue region is replaced with the previously captured background.

Conceptually:

```text
If pixel belongs to cloak:
       use background pixel

Otherwise:
       use original frame pixel
```

The result is:

```text
Original Person
      +
Detected Cloak
      ↓
Cloak Region → Background
      ↓
Invisible Effect ✨
```

---

# 🎨 Why HSV Color Space?

RGB/BGR is useful for displaying images, but color segmentation can become more difficult when brightness changes.

HSV separates color information from brightness more clearly.

```text
HSV

H → Hue
S → Saturation
V → Value
```

This makes HSV particularly useful for detecting a specific colored object such as a blue cloth.

---

# 🎯 Accuracy Improvements

The project focuses on improving the reliability and visual quality of the basic invisible-cloak approach.

### Improvements include:

✅ Multi-frame background capture
✅ HSV-based segmentation
✅ Automatic color calibration
✅ Morphological operations
✅ Noise filtering
✅ Connected-component filtering
✅ Mask smoothing
✅ Temporal stabilization
✅ Better edge handling
✅ Real-time processing
✅ FPS monitoring

> ⚠️ The system does not have a fixed universal "accuracy percentage." Its performance depends on lighting, camera quality, cloth color, background objects, and HSV calibration.

---

# 💡 Recommended Setup

For better results:

### 👕 Blue Cloth

Use a cloth that is:

* Clearly blue
* Relatively uniform in color
* Without complex patterns
* Without strong reflections

### 💡 Lighting

Use:

* Stable lighting
* Sufficient brightness
* Minimal shadows
* No rapidly changing illumination

### 🏠 Background

Avoid having large blue objects behind the user.

Examples:

```text
❌ Blue wall
❌ Blue sofa
❌ Blue curtains
❌ Large blue decorations
```

because these can also be detected as cloak regions.

### 📷 Camera

Keep the camera:

* Stationary
* Stable
* Properly focused
* Facing the scene

---

# 🛠️ Technologies Used

| Technology           | Purpose                       |
| -------------------- | ----------------------------- |
| 🐍 Python            | Application development       |
| 👁️ OpenCV           | Computer Vision               |
| 🔢 NumPy             | Numerical/image operations    |
| 🎨 HSV               | Color segmentation            |
| 🎥 Webcam            | Live video input              |
| 🖼️ Image Processing | Mask refinement               |
| 🤖 AI Concepts       | Intelligent visual processing |

---

# 📂 Project Structure

```text
Invisible_Cloath_Using_AI/
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
├── run_invisible_cloak.bat
│
├── assets/
│
├── screenshots/
│   └── reference.jpg
│
└── output/
    └── invisible_cloak_demo.gif
```

### 📄 `main.py`

Contains the main Computer Vision application.

### 📄 `requirements.txt`

Contains the required Python packages.

### 📄 `README.md`

Contains complete project documentation.

### ▶️ `run_invisible_cloak.bat`

Windows batch file for launching the application.

### 📁 `assets/`

Stores supporting project resources.

### 📁 `screenshots/`

Stores project screenshots and visual references.

### 📁 `output/`

Stores generated output such as demonstration GIFs.

---

# 💻 Installation

## Step 1 — Install Python

Install **Python 3.x** on Windows.

During installation, enable:

```text
☑ Add Python to PATH
```

---

## Step 2 — Open Command Prompt

Navigate to the project directory.

```bash
cd path\to\Invisible_Cloath_Using_AI
```

---

## Step 3 — Install Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

Or install the required libraries directly:

```bash
python -m pip install opencv-python numpy
```

---

# ▶️ Running the Project Using Python IDLE

This project can be executed using **Python IDLE**.

### Step 1

Open:

```text
main.py
```

using Python IDLE.

### Step 2

Select:

```text
Run → Run Module
```

or press:

```text
F5
```

### Step 3

The webcam window will open.

### Step 4

Keep yourself out of the camera view while the background is captured.

### Step 5

Enter the camera view with the blue cloth.

### Step 6

The detected blue region will be replaced with the captured background.

🎉 **The Invisible Cloath effect is active!**

---

# 🎮 Controls

Depending on the implementation, the application provides controls such as:

| Key   | Function                 |
| ----- | ------------------------ |
| `Q`   | Quit application         |
| `ESC` | Exit application         |
| `B`   | Capture background again |
| `C`   | Calibrate blue color     |
| `R`   | Reset processing         |

---

# 🎯 HSV Calibration

HSV values can change depending on:

* Camera
* Lighting
* Cloth material
* Camera exposure
* Indoor/outdoor environment

Therefore, calibration can improve the detection.

### Recommended calibration process

```text
Place Blue Cloth
       ↓
Start Calibration
       ↓
Sample Blue Region
       ↓
Calculate HSV Range
       ↓
Apply HSV Threshold
       ↓
Improved Detection
```

---

# 🚨 Troubleshooting

## ❌ Webcam Does Not Open

Try another camera index.

```python
cap = cv2.VideoCapture(1)
```

instead of:

```python
cap = cv2.VideoCapture(0)
```

Also make sure another application is not already using the webcam.

---

## ❌ Blue Cloth Is Not Detected

Possible reasons:

* Poor lighting
* Incorrect HSV range
* Cloth is too dark
* Cloth has multiple colors
* Camera exposure changes

### Solution

Use HSV calibration and improve the lighting.

---

## ❌ Too Much of the Background Becomes Invisible

The background may contain blue objects.

Try:

* Narrowing the HSV range
* Using calibration
* Removing blue objects from the background

---

## ❌ Flickering Mask

Possible reasons:

* Camera noise
* Changing illumination
* Motion blur
* Incorrect HSV threshold

Use mask smoothing and temporal stabilization.

---

## ❌ Rough Cloak Edges

Use appropriate morphological processing and mask smoothing.

Avoid excessive dilation because it can make the detected area larger than the actual cloak.

---

# ⚡ Performance Optimization

Real-time performance depends on:

* CPU
* Webcam resolution
* Python version
* OpenCV version
* Number of processing operations

For better performance, use a moderate resolution such as:

```text
640 × 480
```

instead of unnecessarily high resolutions.

---

# 🔐 Privacy

The core application processes the webcam stream locally using Python and OpenCV.

No cloud-based Computer Vision service is required for the basic invisible-cloak effect.

---

# 📚 Concepts Learned

This project provides hands-on experience with:

* 🐍 Python Programming
* 👁️ Computer Vision
* 🎥 Real-Time Video Processing
* 🎨 HSV Color Space
* 🔍 Color Segmentation
* 🎭 Binary Masking
* 🧹 Morphological Operations
* 🔎 Connected Components
* 🖼️ Background Modeling
* 🔄 Image Compositing
* 🌫️ Mask Smoothing
* ⚡ Real-Time Optimization
* 📊 FPS Monitoring
* 🎯 Parameter Calibration

---

# 🌍 Real-World Applications

The techniques used in this project can be applied to:

### 🎬 Visual Effects

Creating real-time video effects.

### 🏭 Industrial Computer Vision

Color-based object detection.

### 🤖 Robotics

Object segmentation based on visual properties.

### 🎥 Video Processing

Real-time image manipulation.

### 🖥️ Human–Computer Interaction

Camera-based interactive systems.

### 🧪 Computer Vision Education

Learning practical image-processing techniques.

---

# 🔮 Future Enhancements

The project can be further upgraded with advanced AI techniques.

### 🤖 AI-Based Segmentation

Replace basic color thresholding with deep-learning-based segmentation.

Possible approaches include:

* Semantic segmentation
* Instance segmentation
* Human segmentation
* Neural background removal

### 🧍 Human Segmentation

A human-segmentation model could distinguish the person from the environment and make the effect more robust.

### 🌈 Multi-Color Cloak

Support:

```text
🔵 Blue
🔴 Red
🟢 Green
🟡 Yellow
```

instead of only blue.

### 🎥 Video Recording

Add the ability to save the final invisible-cloak video.

### 🖥️ Graphical User Interface

A GUI could provide:

* Camera selection
* HSV controls
* Calibration
* Background capture
* FPS information
* Recording controls

### 🌐 Web Application

The project could be extended into a browser-based Computer Vision application.

---

# 🧠 Future AI Architecture

A more advanced version could combine multiple Computer Vision techniques:

```text
             🎥 Webcam
                 │
                 ▼
       ┌───────────────────┐
       │ Color Segmentation│
       └─────────┬─────────┘
                 │
       ┌─────────▼─────────┐
       │ Person Segmentation│
       └─────────┬─────────┘
                 │
       ┌─────────▼─────────┐
       │ Object Detection │
       └─────────┬─────────┘
                 │
       ┌─────────▼─────────┐
       │ Temporal Tracking │
       └─────────┬─────────┘
                 │
       ┌─────────▼─────────┐
       │ Background Replace│
       └─────────┬─────────┘
                 │
                 ▼
             ✨ Output
```

This could provide a more advanced and robust invisible-cloak system.

---

# 📊 Project Workflow

```text
START
  │
  ▼
Initialize Webcam
  │
  ▼
Capture Background
  │
  ▼
Read Live Frame
  │
  ▼
Convert BGR → HSV
  │
  ▼
Detect Blue Cloth
  │
  ▼
Generate Mask
  │
  ▼
Clean Mask
  │
  ▼
Remove Noise
  │
  ▼
Smooth Mask
  │
  ▼
Replace Cloak Region
  │
  ▼
Generate Final Frame
  │
  ▼
Display Result
  │
  └───────────────► Repeat
```

---

# 📈 Project Outcome

The final system demonstrates how fundamental Computer Vision techniques can be combined to create an impressive real-time visual effect.

The core concept is:

```text
Webcam
   ↓
HSV Color Detection
   ↓
Mask Generation
   ↓
Mask Refinement
   ↓
Background Replacement
   ↓
Invisible Cloath Effect ✨
```

The project provides practical experience in **Python, OpenCV, NumPy, image segmentation, background modeling, and real-time Computer Vision**.

---

# 👨‍💻 Skills Demonstrated

```text
Python
OpenCV
NumPy
Computer Vision
Image Processing
HSV Segmentation
Binary Masking
Morphological Operations
Background Modeling
Image Compositing
Real-Time Video Processing
Mask Refinement
Color Calibration
Performance Optimization
Debugging
```

---

# ⭐ Project Highlights

🪄 **Invisible Cloath Using AI**
🎥 Real-Time Webcam Processing
🤖 Computer Vision Based System
🎨 HSV Color Segmentation
🖼️ Background Modeling
🎭 Image Masking
🧹 Morphological Processing
🔎 Noise Reduction
🌫️ Mask Refinement
🔄 Temporal Stabilization
🎯 HSV Calibration
📊 FPS Monitoring
🐍 Python + OpenCV + NumPy
💻 Python IDLE Compatible

---

# 🏁 Conclusion

**Invisible Cloath Using AI** is an interactive Computer Vision project that demonstrates how a simple visual idea can be transformed into a real-time application using Python.

By combining **HSV color segmentation, background capture, image masking, morphological processing, noise reduction, and background replacement**, the system creates an invisible-cloak illusion using a standard webcam.

The project is a practical demonstration of how **AI and Computer Vision concepts can be transformed into real-world interactive applications.** 🚀🤖

