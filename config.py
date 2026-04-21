from pathlib import Path

MODEL_PATH = Path(__file__).parent / "yolo11n.pt"

CAMERA_SOURCES = [
    "https://www.youtube.com/watch?v=ByED80IKdIU",  # NYC Times Square
    "https://www.youtube.com/watch?v=AdUw5RdyZxI",  # Chicago traffic
    "https://www.youtube.com/watch?v=1EiC9bvVGnk",  # LA highway
]

VEHICLE_CLASSES = {2, 3, 5, 7}  # car, motorcycle, bus, truck (COCO)

GREEN_THRESHOLD  = 10.0   # density % below this → GREEN
YELLOW_THRESHOLD = 30.0   # density % below this → YELLOW, else RED

SMOOTH_WINDOW = 8         # rolling average over N frames to reduce flicker

CONF_THRESHOLD = 0.40
IMGSZ          = 640
DISPLAY_WIDTH  = 960
DISPLAY_HEIGHT = 540
RECONNECT_DELAY_S = 3   # seconds to wait before reconnecting a dropped stream
