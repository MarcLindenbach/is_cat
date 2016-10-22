#include <Servo.h>

Servo servo;

const int SERVO_PIN = 9;
const int BAUD = 9600;

const int LOADING = 1;
const int IS_CAT = 2;
const int IS_MAYBE_CAT = 3;
const int IS_NOT_CAT = 4;

const int LOADING_ANGLE = 40;
const int IS_MAYBE_CAT_ANGLE = 85;
const int IS_CAT_ANGLE = 20;
const int IS_NOT_CAT_ANGLE = 160;

void setup() {
  servo.attach(9);
  Serial.begin(BAUD);
}

void loop() {
  unsigned int state = Serial.parseInt();
  int angle = -1;
  
  switch (state) {
    case 1:
      Serial.println("Loading...");
      angle = LOADING_ANGLE;
    break;
    case 2:
      Serial.println("Is Cat");
      angle = IS_CAT_ANGLE;
    break;
    case 3:
      Serial.println("Is Maybe Cat");
      angle = IS_MAYBE_CAT_ANGLE;
    break;
    case 4:
      Serial.println("Is Not Cat");
      angle = IS_NOT_CAT_ANGLE;
    break;
  }
  
  if (angle >= 0) {
    servo.write(angle);
  }
}
