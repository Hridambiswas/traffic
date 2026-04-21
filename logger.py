import csv
import time
from pathlib import Path

from config import GREEN_THRESHOLD, YELLOW_THRESHOLD

_LOG_PATH = Path(__file__).parent / "output" / "congestion_log.csv"
_FIELDS   = ["timestamp", "vehicles", "density_pct", "smoothed_pct", "signal"]


class CongestionLogger:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        if enabled:
            _LOG_PATH.parent.mkdir(exist_ok=True)
            self._file = open(_LOG_PATH, "w", newline="")
            self._writer = csv.DictWriter(self._file, fieldnames=_FIELDS)
            self._writer.writeheader()

    def log(self, vehicles: int, density: float, smoothed: float, signal: str):
        if not self.enabled:
            return
        self._writer.writerow({
            "timestamp":    round(time.time(), 3),
            "vehicles":     vehicles,
            "density_pct":  round(density, 2),
            "smoothed_pct": round(smoothed, 2),
            "signal":       signal,
        })

    def close(self):
        if self.enabled:
            self._file.close()
