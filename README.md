# Flying Cursor

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
- Easy keyboard exit using `q`
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

## Troubleshooting
- Ensure your webcam is connected and allowed.
- Good lighting improves tracking accuracy.


