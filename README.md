# Utileyes

Utileyes is an Edge-AI Environment Detection system designed for smart glasses, aimed at assisting visually impaired individuals by providing real-time spatial awareness.

## Architecture (Phase 1)

The current implementation features a real-time, memory-optimized inference engine (`core/detector.py`). It captures live webcam frames and processes them directly in memory. Detected objects' bounding boxes are then sorted spatially from left to right, providing structured environmental context without the overhead of saving frames to disk.

## Tech Stack

*   **Python 3**
*   **OpenCV** (`opencv-python`): For capturing and managing video frames.
*   **Ultralytics YOLO** (`ultralytics`): For efficient, edge-capable object detection using the YOLOv8-nano model.

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
