from ultralytics import YOLO
import mediapipe as mp
import numpy as np
import supervision as sv
import cv2

class HandDetector:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.5):
        # Initialize MediaPipe hands model
        self.hands = mp.solutions.hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence)

    def detect(self, frame):
        # Convert frame to RGB and process it with the hand detection model
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_results = self.hands.process(frame_rgb)
        return hand_results

    def find_closest_object(self, hand_results, detections, labels, resolution):
        if hand_results.multi_hand_landmarks and len(detections) == 0:
            return None

        if hand_results.multi_hand_landmarks and len(detections) > 0:
            # Get hand landmarks from the detected hand
            hand_landmarks = hand_results.multi_hand_landmarks[0]  # Only one hand is detected

            # Calculate the center of the hand (wrist position)
            hand_center = np.array(
                [
                    hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x * resolution[0],
                    hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y * resolution[1],
                ]
            )

            # Compute distances from the hand center to each detected object's bounding box
            object_distances = [
                np.linalg.norm(hand_center - np.array(detection[0][:2]))
                for detection in detections
            ]

            # Find the index of the closest object
            closest_object_index = np.argmin(object_distances)

            # Get the label of the closest object
            held_object = labels[closest_object_index].split(" ")[0]

            return held_object

        return None

class ObjectDetector:
    def __init__(self, model_path):
        # Load YOLO model
        self.model = YOLO(model_path)

    def detect(self, frame):
        # Detect objects in the frame using the YOLO model
        result = self.model(frame, agnostic_nms=True, verbose=False)[0]

        # Convert YOLOv8 detection results to a Detections object
        detections = sv.Detections.from_yolov8(result)

        # Filter out 'person' class detections
        detections = detections[detections.class_id != 0]

        # Create labels for the detected objects
        labels = [
            f"{self.model.model.names[class_id]} {confidence:0.2f}"
            for xyxy, mask, confidence, class_id, tracker_id
            in detections if class_id != 0
        ]

        return {'detections': detections, 'labels': labels}
