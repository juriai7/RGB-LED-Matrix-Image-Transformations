# RGB LED Matrix Image Transformations

### Real-Time Geometric Image Transformations using Raspberry Pi and RGB LED Matrix Panels

This project demonstrates real-time image processing transformations on an RGB LED matrix using a Raspberry Pi.  
The system displays animated geometric transformations such as movement, rotation, scaling, and shearing on a 32×32 or 64×32 LED matrix panel.

---

## Project Overview

The project uses the `rgbmatrix` library to control RGB LED matrix panels connected to a Raspberry Pi.  
A simple diamond or square shape is drawn on the matrix and transformed in real time using mathematical transformation functions.

The project includes three Python scripts:

| File | Description |
|---|---|
| `Demo .py` | Runs an automatic transformation sequence on a 32×32 LED matrix |
| `Button .py` | Uses a physical button to switch between transformations |
| `2disply.py` | Runs transformations on a wider 64×32 display, such as two connected 32×32 panels |

---

## Transformations Included

The project applies the following geometric transformations:

- **Translation** — moves the shape up/down or left/right
- **Rotation** — rotates the shape around the center of the display
- **Scaling** — increases and decreases the shape size
- **Shearing** — skews the shape horizontally

---

## How It Works

```text
Raspberry Pi
↓
RGB LED Matrix Library
↓
Draw shape pixels
↓
Apply transformation equations
↓
Display animated result on LED matrix
```

Each point is transformed mathematically before being displayed on the LED matrix.

---

## Hardware Requirements

- Raspberry Pi
- RGB LED Matrix Panel
- Adafruit RGB Matrix HAT or compatible connection
- Jumper wires / power supply
- Optional push button for manual mode switching

---

## Software Requirements

- Python 3
- RGB Matrix Python library
- RPi.GPIO for button control
- math and time Python modules

---

## How to Run

### Automatic demo mode

```bash
python "Demo .py"
```

### Button-controlled mode

```bash
python "Button .py"
```

### Wider 64×32 display mode

```bash
python "2disply.py"
```

Some Raspberry Pi LED matrix setups may require running with `sudo`.

---

## File Details

### `Demo .py`

This script runs an automatic animation loop.  
It switches between movement, rotation, scaling, and shearing without needing a button.

### `Button .py`

This script uses a push button connected to GPIO pin 22.  
Each button press changes the transformation phase.

### `2disply.py`

This script is designed for a wider 64×32 display, such as two 32×32 panels connected together.  
It includes scaling, shearing, rotation, and translation animations.

---

## Skills Demonstrated

- Raspberry Pi hardware programming
- RGB LED matrix control
- Image processing
- Geometric transformations
- Real-time animation
- GPIO button interaction
- Python programming

---

## Project Structure

```text
RGB-LED-Matrix-Image-Transformations/
│
├── README.md
├── requirements.txt
├── Demo .py
├── Button .py
└── 2disply.py
```

---

## Future Improvements

- Add a menu system for selecting transformations
- Add more shapes and colors
- Add image input support
- Add speed control using buttons
- Improve multi-panel display resolution
- Add video demo and wiring diagram to the README
