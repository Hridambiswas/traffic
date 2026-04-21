import argparse
import time

import cv2

from detector import VehicleDetector
from display import draw
from signal import TrafficSignal
from stream import pick_source


def run(source: str | None = None, conf: float | None = None,
        smooth_window: int = 8, stream_height: int = 480):
    stream_url = pick_source() if source is None else source
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open stream: {stream_url}")

    detector = VehicleDetector(conf=conf) if conf else VehicleDetector()
    signal   = TrafficSignal(window=smooth_window)

    t_prev = time.perf_counter()
    print("Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[main] stream ended — reconnecting...")
            cap.release()
            stream_url = pick_source()
            cap = cv2.VideoCapture(stream_url)
            continue

        boxes, density  = detector.detect(frame)
        state, color    = signal.update(density)

        t_now = time.perf_counter()
        fps   = 1.0 / max(t_now - t_prev, 1e-6)
        t_prev = t_now

        out = draw(frame, boxes, density, state, color, fps)
        cv2.imshow("Traffic Signal", out)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live traffic signal decision system")
    parser.add_argument("--source", default=None,
                        help="Direct stream URL or YouTube live URL (default: random from config)")
    parser.add_argument("--conf",   type=float, default=None,
                        help="YOLO confidence threshold override (default: config.CONF_THRESHOLD)")
    parser.add_argument("--window", type=int,   default=8,
                        help="Smoothing window size in frames (default: 8)")
    parser.add_argument("--height", type=int,   default=480,
                        help="Preferred stream height (default: 480)")
    args = parser.parse_args()
    run(source=args.source, conf=args.conf,
        smooth_window=args.window, stream_height=args.height)
