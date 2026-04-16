# AI Football Control - Complete Guide

## Features Added

### 1. **Real MediaPipe Pose Detection**
- Replaced simulated landmarks with real MediaPipe pose detection
- Now detects actual body movements from your camera
- 33 keypoints tracked for accurate gesture recognition

### 2. **New Football Gestures**

#### Heading Gestures:
- **Head Right** → `HEADING RIGHT!` (Key: H)
- **Head Left** → `HEADING LEFT!` (Key: G)

#### Kicking Gestures:
- **Left Leg Raise** → `LEFT KICK!` (Key: Q)
- **Right Leg Raise** → `RIGHT KICK!` (Key: E)

#### Movement Gestures:
- **Left Shoulder Forward** → `MOVE LEFT!` (Key: A)
- **Right Shoulder Forward** → `MOVE RIGHT!` (Key: D)
- **Hips Raised** → `SPRINTING!` (Key: Shift)

#### New Actions:
- **Both Arms Raised** → `THROW-IN!` (Key: T)
- **Body Lean Right** → `SLIDE TACKLE RIGHT!` (Key: R)
- **Body Lean Left** → `SLIDE TACKLE LEFT!` (Key: L)
- **Elbows Raised** → `DEFENSIVE STANCE!` (Key: D)

### 3. **Configurable Sensitivity**
Edit `config.py` to adjust detection thresholds:
```python
HEAD_RIGHT_THRESHOLD = 0.55  # Adjust head movement sensitivity
LEG_KICK_THRESHOLD = 0.03    # Adjust kick detection
SHOULDER_LEFT_THRESHOLD = 0.01  # Adjust shoulder movement
```

### 4. **Gesture Recording & Playback**
- **Press R** to start/stop recording
- **Press S** to save recorded gestures
- **Press L** to view available recordings
- Recordings saved in `gesture_recordings/` folder as JSON

## Keyboard Controls

| Key | Action |
|-----|--------|
| R | Start/Stop Recording |
| S | Save Recording |
| L | List Recordings |
| ESC | Exit Program |

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Tips for Best Results

1. **Lighting**: Ensure good lighting for accurate pose detection
2. **Distance**: Stand 1-2 meters away from your camera
3. **Space**: Need clear space to move freely
4. **Sensitivity**: Adjust thresholds in `config.py` if gestures aren't detecting
5. **Smoothness**: Use controlled, deliberate movements for better detection

## File Structure

```
AI_FOOTBALL_CONTROL/
├── main.py                  # Main application
├── pose_detector.py         # MediaPipe pose detection
├── gesture_logic.py         # Gesture recognition logic
├── gesture_signals.py       # Visual feedback system
├── gesture_recorder.py      # Recording/playback system
├── config.py               # Adjustable thresholds
├── controller.py           # Keyboard input control
├── requirements.txt        # Dependencies
└── gesture_recordings/     # Saved gesture recordings
```

## Troubleshooting

### Pose Not Detecting?
- Check lighting and camera angle
- Ensure you're fully visible in frame
- Try adjusting MediaPipe confidence in `pose_detector.py`

### Gestures Not Registering?
- Adjust thresholds in `config.py`
- Make movements more pronounced
- Check that landmarks are being detected

### Poor Performance?
- Close other applications
- Reduce camera resolution
- Comment out landmark drawing in `pose_detector.py` line 36

## Advanced Configuration

### Adjust Detection Confidence
In `pose_detector.py`, modify:
```python
min_detection_confidence=0.5,  # Range: 0.0-1.0
min_tracking_confidence=0.5,   # Higher = stricter
```

### Change Model Complexity
```python
model_complexity=1,  # 0=Lite, 1=Full, 2=Heavy
```

Enjoy your AI-powered football control system!
