# Flying Cursor - AI-Based Virtual Mouse using Hand Gesture Recognition

Python-based virtual mouse project that allows users to control the mouse cursor using hand gestures captured through a webcam.
This project uses real-time hand tracking to detect finger positions and convert gestures into mouse actions such as cursor movement and clicking. It is a beginner-friendly Computer Vision project and a practical example of Human-Computer Interaction.

---

## Project Overview

Traditional mouse control requires physical hardware. Flying Cursor removes that dependency by using hand gestures as input.

The webcam captures hand movement, detects hand landmarks, and maps the movement of the index finger to the screen cursor. A pinch gesture between the index finger and thumb is used to perform a mouse click.

---

## Features

- Real-time hand gesture detection
- Cursor movement using index finger
- Mouse click using pinch gesture
- Webcam-based hand tracking
- Contactless computer control
- Beginner-friendly Python project


## Installation

1.  Make sure you have Python installed.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Move**: Raise your index finger and move your hand.
3.  **Click**: pinch your index finger and thumb together.
4.  **Exit**: Press `q`.

## How It Works

1. The webcam captures live video.
2. The hand tracking model detects hand landmarks.
3. The system identifies the index finger position.
4. The index finger movement is mapped to the screen coordinates.
5. The cursor moves according to hand movement.
6. When the index finger and thumb come close, a click action is performed.

---

## Troubleshooting
- Ensure your webcam is connected and allowed.
- Good lighting improves tracking accuracy.


![Flying Cursor Gesture Controls](image.png)
