# 🪄 Invisible Cloak AI Pro

A real-time **Computer Vision** project that creates an invisible-cloak effect with a webcam using **Python, OpenCV, and NumPy**.

The idea is simple: first capture a clean view of the room. During live video, the program detects the **blue cloak** in HSV color space and replaces only that detected region with the corresponding pixels from the saved background.

## ✨ What this version improves

- 🎥 Real-time mirrored webcam preview
- 🖼️ Multi-frame median background capture for a cleaner reference image
- 🎨 HSV-based blue-cloth segmentation
- 🧹 Morphological opening/closing to reduce noise and holes
- 🔎 Connected-component filtering to reject tiny false detections
- 🌫️ Feathered mask edges for smoother blending
- 🎞️ Temporal mask smoothing to reduce flicker
- 🎯 Optional automatic HSV calibration using a center ROI
- 🔄 Background recapture without restarting the program
- 📊 Live FPS and cloak-mask coverage display
- 🪟 Designed to run directly from Python IDLE on Windows

> **Important:** No color-segmentation method can guarantee perfect results in every room. Accuracy depends heavily on lighting, camera quality, background movement, and how different the cloak color is from other blue objects in the scene.

## 📁 Project structure

```text
Invisible_Cloak_AI_Pro/
│
├── main.py                    # Complete application
├── requirements.txt           # Python packages
├── run_invisible_cloak.bat    # Windows double-click launcher
├── README.md                  # Documentation
├── assets/                    # Optional project assets
├── screenshots/               # Add your screenshots here
└── output/                    # Add exported demo files here
```

## 💻 Requirements

- Windows 10/11
- Python 3.10+ recommended
- A working webcam
- Internet connection only for the first package installation

## 🚀 Installation in Python IDLE

Open **Command Prompt** and run:

```text
python --version
python -m pip install -r "C:\path\to\Invisible_Cloak_AI_Pro\requirements.txt"
```

Then open `main.py` with **Python IDLE** and choose:

**Run → Run Module (F5)**

You can also double-click `run_invisible_cloak.bat`.

## 🧙 How to use

### Step 1 — Background capture

When the program starts, move completely out of the camera view. A 5-second countdown appears, followed by a multi-frame background capture.

### Step 2 — Enter with the blue cloth

Wear/hold a **blue cloth** and enter the same scene. Keep the camera and background as still as possible.

### Step 3 — Improve detection if needed

Place the blue cloth inside the white calibration box and press **C**. The program estimates a more suitable HSV range from the current lighting.

### Step 4 — Recapture the background

If the background changed, move out of frame and press **R**. The application will capture a fresh background.

### Step 5 — Exit

Press **Q** or **ESC**.

## 🎯 Tips for the best effect

1. Use a **solid blue cloth** rather than patterned fabric.
2. Avoid blue objects in the background.
3. Keep lighting reasonably even.
4. Do not move furniture after the background is captured.
5. Keep the webcam fixed on a stable surface.
6. Avoid very dark or extremely reflective blue cloth.
7. For difficult lighting, use the **C calibration** option.

## 🧠 Computer Vision pipeline

```text
Webcam
   ↓
Mirrored BGR Frame
   ↓
HSV Conversion
   ↓
Blue Color Segmentation
   ↓
Morphological Cleanup
   ↓
Connected-Component Filtering
   ↓
Temporal Smoothing + Edge Feathering
   ↓
      ┌───────────────────────┐
      │ Blue region → BACKGROUND │
      │ Other region → LIVE FRAME│
      └───────────────────────┘
   ↓
Invisible Cloak Result
```

## 🔧 If the webcam does not open

Open `main.py` and change:

```python
CAMERA_INDEX = 0
```

to:

```python
CAMERA_INDEX = 1
```

Try `2` if you have multiple cameras.

## 🛠️ Technologies

- **Python** — application logic
- **OpenCV** — webcam capture, HSV conversion, masking, morphology, blending
- **NumPy** — image arrays, median background construction, numerical operations

## ⚠️ Limitations

This is a **color-segmentation visual effect**, not a true physical invisibility system. If another object has a similar blue color, it can also be detected. Likewise, moving objects in the background can remain visible because the reference background is captured before the effect begins.

## 📌 Suggested project title for GitHub / LinkedIn

**Invisible Cloak AI Pro – Real-Time Blue Cloth Detection & Background Replacement using Computer Vision** 🪄🎥🤖
