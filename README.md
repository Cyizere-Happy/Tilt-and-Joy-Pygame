# LitMates: Joystick + MPU6050 Game

![Game Preview GIF](preview.gif)  <!-- Replace with your GIF file -->

## Team Name

**LitMates**

## Description

This game lets you control a cartoon character on the screen using a **joystick** and an **MPU6050 sensor** connected to an Arduino. You can move the character by pushing the joystick or tilting the sensor, and press a button to make the character jump.

**Special features:**

* Physical input using **embedded hardware**
* **Jump action** with background color flash
* **Particle effects** when jumping or collecting coins
* **Win and Lose conditions** with immediate freeze of gameplay
* Optional **audio effects** for jumping

---

## How to Play

1. Connect your joystick + MPU6050 to Arduino.
2. Run the Python game using `pygame` with serial communication:

   ```bash
   python game.py
   ```
3. Controls:

   * **Joystick / Tilt MPU6050:** Move the character
   * **Button:** Jump
   * **Collect coins** to increase your score
4. **Win condition:** Reach the target score before time runs out.
5. **Lose condition:** Time runs out before reaching the target score.

---

## Features

* Joystick + MPU6050 tilt movement
* Jump with particle effect and background flash
* Score system with coin collection
* Win / Lose conditions with immediate freeze
* Optional jump sound

---

## Requirements

* Python 3.x
* Pygame (`pip install pygame`)
* Arduino with MPU6050 and joystick
* Optional `jump.wav` sound file in the same folder

---

## Serial Configuration

* Adjust your Arduino COM port in the game file:

  ```python
  arduino_serial = serial.Serial('COM5', 9600, timeout=1)
  ```
* Arduino should send data in the following format:

  ```
  joystickX,joystickY,button,pitch,roll
  ```

  Example:

  ```
  512,400,1,0.05,0.3
  ```

---

## How It Works

* The Python program reads **real-time sensor data** from Arduino via serial.
* Character moves according to joystick values or MPU6050 tilt angles.
* Jumping is triggered by the joystick button.
* Coins spawn randomly, and collecting them increases score.
* The game ends when the target score is reached (win) or time runs out (lose).

---

## Screenshots / GIF

<img width="1200" height="950" alt="image" src="https://github.com/user-attachments/assets/8ac612f6-7b41-42b8-ac70-4abdd5978156" />

