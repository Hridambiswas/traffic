import numpy as np
from ultralytics import YOLO

from config import MODEL_PATH, VEHICLE_CLASSES, CONF_THRESHOLD, IMGSZ


class VehicleDetector:
    def __init__(self, conf: float = CONF_THRESHOLD):
        self.model = YOLO(str(MODEL_PATH))
        self.conf  = conf

    def detect(self, frame: np.ndarray) -> tuple[list, float]:
        """Return (boxes, density_pct).
        boxes: list of [x1,y1,x2,y2] ints for vehicle detections
        density_pct: sum of vehicle bbox areas / frame area * 100
        """
        h, w = frame.shape[:2]
        frame_area = h * w

        results = self.model(frame, imgsz=IMGSZ, conf=self.conf, verbose=False)[0]

        boxes = []
        vehicle_area = 0
        if results.boxes is not None:
            for box in results.boxes:
                cls = int(box.cls[0])
                if cls not in VEHICLE_CLASSES:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                boxes.append([x1, y1, x2, y2])
                vehicle_area += (x2 - x1) * (y2 - y1)

        density = min((vehicle_area / frame_area) * 100.0, 100.0)
        return boxes, density
