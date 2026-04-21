from collections import deque

from config import GREEN_THRESHOLD, YELLOW_THRESHOLD, SMOOTH_WINDOW

_COLORS = {
    "GREEN":  (0,   200,  0),
    "YELLOW": (0,   200, 200),
    "RED":    (0,     0, 200),
}


class TrafficSignal:
    def __init__(self, window: int = SMOOTH_WINDOW):
        self._history: deque[float] = deque(maxlen=window)
        self._state = "GREEN"

    def update(self, density: float) -> tuple[str, tuple[int, int, int]]:
        self._history.append(density)
        avg = self.smoothed

        if avg < GREEN_THRESHOLD:
            self._state = "GREEN"
        elif avg < YELLOW_THRESHOLD:
            self._state = "YELLOW"
        else:
            self._state = "RED"

        return self._state, _COLORS[self._state]

    @property
    def state(self) -> str:
        return self._state

    @property
    def smoothed(self) -> float:
        return sum(self._history) / len(self._history) if self._history else 0.0
