import cv2
import numpy as np

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, YELLOW_THRESHOLD, GREEN_THRESHOLD

_FONT      = cv2.FONT_HERSHEY_SIMPLEX
_BOX_COLOR = (0, 165, 255)


def _density_bar(frame, density: float, h: int, w: int):
    bar_w = int(w * 0.35)
    bar_h = 14
    x0, y0 = 10, h - 30
    cv2.rectangle(frame, (x0, y0), (x0 + bar_w, y0 + bar_h), (50, 50, 50), -1)
    fill = int(bar_w * min(density, 100) / 100)
    color = (0, 200, 0) if density < GREEN_THRESHOLD else (0, 200, 200) if density < YELLOW_THRESHOLD else (0, 0, 200)
    cv2.rectangle(frame, (x0, y0), (x0 + fill, y0 + bar_h), color, -1)
    cv2.rectangle(frame, (x0, y0), (x0 + bar_w, y0 + bar_h), (180, 180, 180), 1)
    cv2.putText(frame, f"Density: {density:.1f}%", (x0, y0 - 4), _FONT, 0.45, (220, 220, 220), 1)


def draw(frame: np.ndarray, boxes: list, density: float,
         signal: str, signal_color: tuple, fps: float) -> np.ndarray:
    out = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    sx = DISPLAY_WIDTH  / frame.shape[1]
    sy = DISPLAY_HEIGHT / frame.shape[0]
    h, w = out.shape[:2]

    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(out,
                      (int(x1 * sx), int(y1 * sy)),
                      (int(x2 * sx), int(y2 * sy)),
                      _BOX_COLOR, 2)

    # Signal badge (top-right)
    badge_x, badge_y = w - 160, 10
    cv2.rectangle(out, (badge_x, badge_y), (badge_x + 150, badge_y + 50),
                  signal_color, -1)
    cv2.putText(out, signal, (badge_x + 10, badge_y + 36),
                _FONT, 1.1, (255, 255, 255), 2)

    # Stats (top-left)
    cv2.putText(out, f"Vehicles: {len(boxes)}", (10, 24), _FONT, 0.6, (220, 220, 220), 1)
    cv2.putText(out, f"FPS: {fps:.1f}",         (10, 48), _FONT, 0.6, (220, 220, 220), 1)

    _density_bar(out, density, h, w)
    return out
