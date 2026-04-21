<div align="center">

# 🚦 Real-Time Traffic Signal Decision System

**Live public traffic camera → YOLO11n vehicle detection → density-based signal control**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![YOLO](https://img.shields.io/badge/YOLO11n-Ultralytics-FF6B35?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11+-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-public_streams-FF0000?logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

*Hridam Biswas · KIIT University*

</div>

---

## The Problem

Traffic signals in most cities run on fixed timers — a car sits at a **red light on an empty road for 2 minutes** while no one crosses the other way. This system reads a live traffic camera, counts how much road is covered by vehicles, and makes a real-time signal decision. **No fixed timers. No wasted time.**

---

## Pipeline

```
 Public YouTube Traffic Camera (yt-dlp)
             │
             ▼
  ┌──────────────────────┐
  │   Frame Capture      │  OpenCV VideoCapture → raw BGR frame
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────┐
  │   YOLO11n Detection  │  Detects: car · truck · bus · motorcycle
  │   (COCO classes)     │  Outputs: bounding boxes + class IDs
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────────────────────────┐
  │   Density Calculation                    │
  │                                          │
  │   density = Σ(bbox areas) / frame_area   │
  │             ───────────────────────────  │
  │                      × 100 %             │
  └──────────┬───────────────────────────────┘
             │
             ▼
  ┌──────────────────────┐
  │  Rolling Average     │  Last N frames smoothed → removes flicker
  │  Smoothing (N=8)     │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────────────────────────┐
  │   Signal Decision                        │
  │                                          │
  │   density < 10%  →  🟢  GREEN            │
  │   density < 30%  →  🟡  YELLOW           │
  │   density ≥ 30%  →  🔴  RED              │
  └──────────┬───────────────────────────────┘
             │
             ▼
  ┌──────────────────────┐
  │   Live Display       │  Bounding boxes · signal badge
  │   (OpenCV window)    │  density bar · vehicle count · FPS
  └──────────────────────┘
```

---

## Signal Logic

| Smoothed Density | Signal | Meaning |
|:---:|:---:|---|
| `< 10 %` | 🟢 **GREEN** | Road is clear — let traffic through immediately |
| `10 % – 30 %` | 🟡 **YELLOW** | Moderate traffic — prepare to stop or go |
| `≥ 30 %` | 🔴 **RED** | Heavy congestion — hold all crossing traffic |

> Density is **rolling-averaged over the last 8 frames** to prevent the signal flickering on every detection jitter.

---

## Live Window Layout

```
┌────────────────────────────────────────────────────┐
│  Vehicles: 7                          ┌──────────┐ │
│  FPS: 24.3                            │  GREEN   │ │
│                                       └──────────┘ │
│                                                    │
│          [ live camera feed + bounding boxes ]     │
│                                                    │
│  Density: 8.4%  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
└────────────────────────────────────────────────────┘
```

| Element | Description |
|---|---|
| **Bounding boxes** | Orange rectangles around every detected vehicle |
| **Signal badge** | Top-right color block — GREEN / YELLOW / RED |
| **Density bar** | Bottom-left progress bar; color matches signal state |
| **Vehicle count** | Total vehicles detected in current frame |
| **FPS** | Live inference + display frame rate |

---

## Quick Start

```bash
git clone https://github.com/Hridambiswas/traffic.git
cd traffic
pip install -r requirements.txt

# Random public camera from config
python main.py

# Specific YouTube live stream
python main.py --source "https://www.youtube.com/watch?v=ByED80IKdIU"

# Stricter detection + wider smoothing window
python main.py --conf 0.5 --window 12

# Lower resolution stream (faster)
python main.py --height 360
```

Press **Q** to quit.

---

## CLI Reference

| Flag | Default | Description |
|---|---|---|
| `--source` | random from `config.py` | YouTube live URL or direct stream URL |
| `--conf` | `0.40` | YOLO confidence threshold (higher → fewer false positives) |
| `--window` | `8` | Rolling average window size in frames |
| `--height` | `480` | Preferred stream resolution height |

---

## Configuration

All tunable parameters live in **`config.py`**:

```python
VEHICLE_CLASSES   = {2, 3, 5, 7}   # car, motorcycle, bus, truck (COCO IDs)

GREEN_THRESHOLD   = 10.0            # % density below which signal is GREEN
YELLOW_THRESHOLD  = 30.0            # % density below which signal is YELLOW

SMOOTH_WINDOW     = 8               # rolling average frame count
CONF_THRESHOLD    = 0.40            # YOLO detection confidence

DISPLAY_WIDTH     = 960             # output window width
DISPLAY_HEIGHT    = 540             # output window height
```

| Parameter | Lower value | Higher value |
|---|---|---|
| `GREEN_THRESHOLD` | More likely to stay yellow/red | Easier to get green signal |
| `YELLOW_THRESHOLD` | Red trips sooner | More tolerance before red |
| `SMOOTH_WINDOW` | Reacts faster, more flicker | Stable signal, slower response |
| `CONF_THRESHOLD` | Detects more vehicles | Only high-confidence detections |

---

## Camera Sources

Public live traffic cameras are configured in `config.py`:

| Camera | Location | URL |
|---|---|---|
| Cam 1 | NYC Times Square | `youtube.com/watch?v=ByED80IKdIU` |
| Cam 2 | Chicago Traffic | `youtube.com/watch?v=AdUw5RdyZxI` |
| Cam 3 | LA Highway | `youtube.com/watch?v=1EiC9bvVGnk` |

> Add any public YouTube live stream to `CAMERA_SOURCES` in `config.py`. The system randomly picks one on start and auto-reconnects if the stream drops.

---

## YOLO Vehicle Classes

| COCO Class ID | Label | Included |
|:---:|---|:---:|
| 2 | car | ✅ |
| 3 | motorcycle | ✅ |
| 5 | bus | ✅ |
| 7 | truck | ✅ |
| 0 | person | ❌ |
| 9 | traffic light | ❌ |

Only vehicle classes contribute to density. Pedestrians and static objects are ignored.

---

## Project Structure

```
traffic/
│
├── main.py          ← entry point · CLI args · stream reconnect loop
├── config.py        ← all thresholds, paths, camera URLs
│
├── stream.py        ← yt-dlp handler · random source with fallback
├── detector.py      ← YOLO11n detection · bbox-area density calc
├── signal.py        ← rolling-average smoothed signal decision
├── display.py       ← OpenCV overlay renderer
│
└── requirements.txt
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `ultralytics` | ≥ 8.4.0 | YOLO11n model + inference |
| `opencv-python` | ≥ 4.11.0 | Frame capture, rendering, live window |
| `numpy` | ≥ 1.26.0 | Array ops for density computation |
| `yt-dlp` | ≥ 2026.1.0 | Public YouTube stream URL extraction |

---

<div align="center">

*Built by Hridam Biswas · KIIT University*

</div>
