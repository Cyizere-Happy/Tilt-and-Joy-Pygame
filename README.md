# LitMates: Joystick + MPU6050 Game 🎮

**Team Name:** LitMates

## Description

LitMates is a fun and interactive game where you control a cartoon character on the screen using a **joystick** and an **MPU6050 sensor** connected to an Arduino. Move the character by tilting the sensor or pushing the joystick, and press a button to make the character jump.

**Special Features:**

* Physical input using embedded hardware
* Jump action with **background color flash**
* **Particle effects** when jumping or collecting coins
* Win and Lose conditions with immediate freeze of gameplay
* Optional **audio effects** for jumping, winning, losing, or collecting coins

---

## How to Play

1. Connect your joystick and MPU6050 to Arduino.
2. Run the Python game:

```bash
python game.py
```

**Controls:**

* **Joystick / Tilt MPU6050:** Move the character
* **Button:** Jump
* **Collect coins** to increase your score

**Winning Condition:** Reach the target score before time runs out.
**Losing Condition:** Time runs out before reaching the target score.

---

## Features

* Joystick + MPU6050 tilt movement
* Jump with particle effect and background flash
* Score system with **coin collection**
* Win / Lose conditions with immediate gameplay freeze
* Optional **jump, win, fail, and collect sounds**

---

## Requirements

* Python 3.x
* Pygame (`pip install pygame`)
* Arduino with MPU6050 and joystick
* Optional audio files (`jump.wav`, `winning.wav`, `failing.wav`, `collect.wav`) in the game folder

---

## Serial Configuration

Adjust your Arduino COM port in the Python game:

```python
arduino_serial = serial.Serial('COM5', 9600, timeout=1)
```

Arduino should send data in the following **format**:

```
joystickX,joystickY,button,pitch,roll
```

**Example:**

```
512,400,1,0.05,0.3
```

---

## How It Works

1. The Python program reads real-time sensor data from Arduino via **serial communication**.
2. Character moves according to **joystick values** or **MPU6050 tilt angles**.
3. **Jumping** is triggered by the joystick button.
4. **Coins spawn randomly**, and collecting them increases the score.
5. The game ends when the target score is reached (**win**) or time runs out (**lose**).

---

## Screenshots / GIFs

*Add screenshots or GIFs of gameplay here for better visualization.*

<img width="1186" height="933" alt="image" src="https://github.com/user-attachments/assets/dd4614ea-2d89-4b76-a67e-29fc90b1070c" />
<img width="1189" height="932" alt="image" src="https://github.com/user-attachments/assets/3a2f6dba-6a8c-47fa-89dd-6a876b591358" />



---

## Optional Enhancements

* Add more sounds for win, fail, and coin collection.
* Customize **character size, speed, jump height**, and **coin spawn rate**.
* Add **levels** or **obstacles** for increased challenge.




