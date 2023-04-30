from utils.arguments import parse_arguments
from utils.audio import AudioRecorder
from utils.detection import HandDetector, ObjectDetector
from utils.visualization import BoxAnnotator

import cv2
import threading
import tempfile

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Set up video capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.webcam_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.webcam_resolution[1])
    #cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    # Initialize detectors, annotator, and audio recorder
    hand_detector = HandDetector(max_num_hands=1, min_detection_confidence=0.5)
    object_detector = ObjectDetector("yolov8l.pt")
    box_annotator = BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    audio_recorder = AudioRecorder()

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        # Detect hands and objects in the frame
        hand_results = hand_detector.detect(frame)
        object_detections = object_detector.detect(frame)

        # Annotate the frame with bounding boxes and labels
        frame = box_annotator.annotate(scene=frame, detections=object_detections['detections'], labels=object_detections['labels'])

        # Listen for the 's' key press to start recording audio
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            print("I am listening, please speak...")
            if not audio_recorder.is_recording:
                temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                audio_thread = threading.Thread(target=audio_recorder.record, args=(temp_audio_file,))
                audio_thread.start()

        # Check if the transcription matches the query and find the closest object
        if audio_recorder.transcription is not None and "What object am I holding" in audio_recorder.transcription:
            if hand_results.multi_hand_landmarks:
                if len(object_detections['labels']) == 0:
                    print("Liar liar pants on fire! You are not holding any objects!")
                else:
                    held_object = hand_detector.find_closest_object(hand_results, object_detections['detections'], object_detections['labels'], args.webcam_resolution)
                    print(f"You are holding: {held_object}")
                

        # Show the annotated frame
        cv2.imshow("frame", frame)

        # Listen for the 'q' key press to quit
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    main()
