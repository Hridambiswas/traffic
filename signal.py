from collections import deque

from config import GREEN_THRESHOLD, YELLOW_THRESHOLD, SMOOTH_WINDOW

_COLORS = {
    "GREEN":  (0,   200,  0),
    "YELLOW": (0,   200, 200),
    "RED":    (0,     0, 200),
}


class TrafficSignal:
    def __init__(self):
        self._history: deque[float] = deque(maxlen=SMOOTH_WINDOW)

    def update(self, density: float) -> tuple[str, tuple[int, int, int]]:
        self._history.append(density)
        avg = sum(self._history) / len(self._history)

        if avg < GREEN_THRESHOLD:
            state = "GREEN"
        elif avg < YELLOW_THRESHOLD:
            state = "YELLOW"
        else:
            state = "RED"

        return state, _COLORS[state]

    @property
    def smoothed(self) -> float:
        return sum(self._history) / len(self._history) if self._history else 0.0
