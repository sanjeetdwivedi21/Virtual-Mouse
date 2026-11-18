# Virtual Mouse

A virtual mouse that lets you control your computer cursor using hand gestures captured through a webcam. The project uses OpenCV and MediaPipe for hand tracking and AutoPy for mouse control.

## Features

- Real-time hand detection and landmark tracking
- Cursor movement using the index finger
- Adaptive cursor smoothing for more responsive movement
- Left-click using the index and middle finger pinch gesture
- Click cooldown to reduce rapid repeated clicks
- Live FPS display
- Press `Q` to close the application

## Tech Stack

- Python 3.11
- OpenCV
- MediaPipe
- NumPy
- AutoPy

## Project Structure

```text
Virtual-Mouse/
├── main.py
├── HandTrackingModule.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Keep `HandTrackingModule.py` in the same project folder as `main.py`. It contains the hand-tracking helper class used by the application.

## Requirements

- Windows computer
- Python 3.11 (recommended for this project setup)
- Working webcam
- Internet connection for installing dependencies

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sanjeetdwivedi21/Virtual-Mouse.git
cd Virtual-Mouse
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```powershell
python main.py
```

Allow webcam access if Windows asks for permission. Press `Q` while the camera window is active to exit.

## Gesture Controls

| Gesture | Action |
|---|---|
| Index finger up, middle finger down | Move the cursor |
| Index and middle fingers up, then bring their tips close together | Left-click |

## How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe detects the hand and returns hand landmarks.
3. The index-finger tip coordinates are mapped to screen coordinates.
4. Adaptive smoothing helps reduce cursor jitter while retaining responsiveness.
5. The distance between the index and middle fingertips is used to detect a click.
6. AutoPy sends the corresponding mouse movement and click actions to the operating system.

## Troubleshooting

- **Camera not detected:** Check that the webcam is connected and camera permission is enabled.
- **`No module named ...`:** Activate the virtual environment and run `pip install -r requirements.txt`.
- **MediaPipe has no `solutions` attribute:** Use the compatible dependency versions in `requirements.txt` and make sure no local file or folder is named `mediapipe`.
- **OpenCV DLL blocked by Windows:** Check Windows Security or your organization's Application Control logs. Do not disable security controls to run an untrusted binary.
- **Mouse movement is unavailable:** Check operating-system permissions and whether another application is controlling the mouse.

## Future Improvements

- Right-click gesture
- Scroll up and down
- Drag-and-drop gesture
- Pinch-state detection to prevent repeated clicks while holding a pinch
- Gesture-based mode switching
- Improved tracking stability and performance

## Disclaimer

This project controls the system mouse. Keep your hand movements deliberate, save your work before testing, and stop the program if the cursor behaves unexpectedly.

## Author

**YOUR NAME**

- GitHub: https://github.com/sanjeetdwivedi21/Virtual-Mouse.git

---

If you find this project useful, feel free to ⭐ the repository.
