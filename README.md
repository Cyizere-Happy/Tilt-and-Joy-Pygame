# Joystick-MPU6050-Game

A small Pygame project that allows you to control a character on the screen using a **joystick** and an **MPU6050 gyroscope/accelerometer** connected via Arduino.

---

## Features

- Real-time character movement using joystick input.
- Tilt-based movement using MPU6050 sensor (pitch and roll).
- Button input handling for actions (e.g., fire or jump).
- Boundaries to keep the character inside the window.
- Simple, cartoonish character drawn with Pygame.

---

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/news)
- PySerial (`pip install pyserial`)
- Arduino board with MPU6050 sensor and joystick

---

## Usage

1. Connect your Arduino with MPU6050 and joystick.
2. Update the COM port in `Charcter_Preview.py`:

<img width="1190" height="930" alt="image" src="https://github.com/user-attachments/assets/0d1dfcae-d967-47a2-a453-f8ac9325ce5f" />
```python
arduino_serial = serial.Serial('COM5', 9600, timeout=1)


