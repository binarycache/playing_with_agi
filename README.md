---

# ChatGPT with Eyes

A real-time object detection and interaction system using OpenCV, MediaPipe, YOLO, and OpenAI's Whisper ASR.

This project demonstrates how to combine computer vision and natural language processing to create a system that recognizes objects in a user's hand and answers questions based on the detected objects.

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- YOLO
- OpenAI's Whisper ASR
- soundfile
- sounddevice
- ultralytics
- supervision

## Installation

1. Create a virtual environment and activate it:

```sh
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

2. Install the required packages:

```sh
pip install -r requirements.txt
```

## Usage

Run the main script:

```sh
python main.py
```

Press 's' to start recording your question (e.g., "What object am I holding?"). The application will transcribe your question using the Whisper ASR model and detect the object you are holding using YOLO and MediaPipe.

Press 'q' to quit the application.

## License

This project is licensed under the terms of the MIT License.

---