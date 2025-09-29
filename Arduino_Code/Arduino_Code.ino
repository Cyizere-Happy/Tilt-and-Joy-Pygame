#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const int joyXPin = A0;
const int joyYPin = A1;
const int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);

  // Initialize MPU6050
  Wire.begin();
  Serial.println("Initialize MPU6050");
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
}

void loop() {
  // --- Joystick ---
  int joyX = analogRead(joyXPin);
  int joyY = analogRead(joyYPin);
  int buttonState = digitalRead(buttonPin);

  // --- MPU6050 ---
  Vector normAccel = mpu.readNormalizeAccel();
  float pitch = normAccel.XAxis;  // forward/back tilt
  float roll  = normAccel.YAxis;  // left/right tilt

  // --- Send all data in one line ---
  // Format: joyX,joyY,button,pitch,roll
  Serial.print(joyX);
  Serial.print(",");
  Serial.print(joyY);
  Serial.print(",");
  Serial.print(buttonState);
  Serial.print(",");
  Serial.print(pitch, 2);  // 2 decimal places
  Serial.print(",");
  Serial.println(roll, 2);

  delay(50); // adjust refresh rate
}
