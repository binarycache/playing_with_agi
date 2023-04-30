import cv2
import numpy as np

class BoxAnnotator:
    def __init__(self, thickness=2, text_thickness=2, text_scale=1):
        self.thickness = thickness
        self.text_thickness = text_thickness
        self.text_scale = text_scale

    def annotate(self, scene, detections, labels):
        """
        Annotate the given scene with bounding boxes and labels from the detections.

        :param scene: Image frame from the video.
        :param detections: Detections containing bounding box information.
        :param labels: Labels associated with the detections.
        :return: Annotated image frame.
        """
        for i, detection in enumerate(detections):
            #print(detection[0][:4])
            x1, y1, x2, y2 = map(int, detection[0][:4])
            class_id = int(detection[3])
            label = labels[i]
            color = (0, 255, 0)
            cv2.rectangle(scene, (x1, y1), (x2, y2), color, self.thickness)
            t_size = cv2.getTextSize(label, 0, self.text_scale, self.text_thickness)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(scene, (x1, y1), c2, color, -1)
            cv2.putText(scene, label, (x1, y1 - 2), 0, self.text_scale, [0, 0, 0], self.text_thickness, cv2.LINE_AA)
        return scene
