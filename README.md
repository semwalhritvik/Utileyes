# Utileyes

Utileyes is an Edge-AI Environment Detection system designed for smart glasses, aimed at assisting visually impaired individuals by providing real-time spatial awareness.

## Architecture (Phase 1)

The current implementation features a real-time, memory-optimized inference engine (`core/detector.py`). It captures live webcam frames and processes them directly in memory. Detected objects' bounding boxes are then sorted spatially from left to right, providing structured environmental context without the overhead of saving frames to disk.

## Phase 2: Spatial Sonar Engine

Building upon the inference engine, Phase 2 integrates a real-time spatial audio feedback system (`core/audio.py` and `main.py`).

*   **Closest Object Filtering:** The system identifies the single closest object using bounding box area. A confidence filter (>0.6) removes false positives to prevent ghost tracking.
*   **Proximity to Pitch Mapping:** The area of the closest object is normalized against the total frame area. This drives the frequency of a generated sine wave (larger/closer = higher pitch, distant = low hum). When no objects are detected, the system smoothly drops to a quiet 100Hz idle state.
*   **Directional Panning:** The X-coordinate of the object's center is normalized from `-1.0` (full left) to `1.0` (full right) and mapped to stereo panning volume.
*   **Audio Generation:** `sounddevice` plays the generated stereo sine wave continuously.

### DSP Challenges and Solutions

During development, we encountered several Digital Signal Processing (DSP) challenges:
1.  **Audio Popping and Clicking:** Initial attempts to generate continuous audio chunks resulted in popping sounds between blocks because the sine wave's phase was not aligned. We fixed this by strictly accumulating and wrapping the `phase` across audio callbacks.
2.  **Tracking Latency and Interpolation Lag:** To smooth out the audio transitions, we originally implemented heavy linear interpolation (lerping) on the target frequencies and pan values. However, this caused the audio panning to lag noticeably behind the webcam footage.
3.  **Final Approach - Low-Latency Tracking:** We abandoned the heavy interpolation and phase-accumulation DSP model for a simpler, zero-latency system. By accepting a minor amount of audio crackle during rapid movements, the `sounddevice` output stream now updates parameters instantly, ensuring real-time proprioceptive accuracy perfectly locked to the video frame rate.

## Tech Stack

*   **Python 3**
*   **OpenCV** (`opencv-python`): For capturing and managing video frames.
*   **Ultralytics YOLO** (`ultralytics`): For efficient, edge-capable object detection using the YOLOv8-nano model.
*   **NumPy & SciPy**: For DSP math and audio generation.
*   **SoundDevice** (`sounddevice`): For real-time, non-blocking stereo audio playback.

## Setup Instructions

Follow these steps to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/semwalhritvik/Utileyes.git
    cd Utileyes
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```
    *Note: The first time you run `main.py`, the `yolov8n.pt` model weights will be downloaded automatically.*

To exit the live stream, press the `q` key while the webcam window is active.
