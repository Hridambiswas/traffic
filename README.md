# Traffic Signal Decision System

Real-time traffic density analysis using public live camera feeds and YOLO11n vehicle detection.

## How it works

1. **Stream** — pulls a public YouTube live traffic camera via `yt-dlp`
2. **Detect** — YOLO11n finds vehicles (car, bus, truck, motorcycle) in each frame
3. **Density** — `Σ(vehicle bbox areas) / frame area × 100 %`
4. **Signal** — rolling-average smoothed decision:
   - **GREEN** — density < 10 %
   - **YELLOW** — 10 % ≤ density < 30 %
   - **RED** — density ≥ 30 %
5. **Display** — live OpenCV window with bounding boxes, density bar, signal badge, FPS

## Quick start

```bash
pip install -r requirements.txt
python main.py                        # random source from config
python main.py --source <youtube_url> # specific camera
python main.py --conf 0.5             # stricter detection
```

Press **Q** to quit.

## Tuning

| Parameter | Location | Effect |
|-----------|----------|--------|
| `GREEN_THRESHOLD` | `config.py` | density % for green signal |
| `YELLOW_THRESHOLD` | `config.py` | density % for yellow signal |
| `SMOOTH_WINDOW` | `config.py` | frames to average (higher = less flicker) |
| `CONF_THRESHOLD` | `config.py` | YOLO confidence (higher = fewer false positives) |

## Project structure

```
traffic/
├── main.py       # entry point
├── config.py     # thresholds, paths, sources
├── stream.py     # yt-dlp stream URL extraction
├── detector.py   # YOLO11n detection + density
├── signal.py     # rolling-average signal decision
├── display.py    # OpenCV overlay rendering
└── requirements.txt
```
