
/*
  SHELFNEX - Fixed Path Rover
  Arduino UNO starter firmware

  Serial commands:
  F = Forward
  B = Backward
  L = Turn left
  R = Turn right
  S = Stop

  IMPORTANT:
  Motor-driver pins below are placeholders.
  Confirm your driver wiring before connecting motors.
*/

const int LEFT_IN1  = 2;
const int LEFT_IN2  = 3;
const int RIGHT_IN1 = 4;
const int RIGHT_IN2 = 5;

const int LEFT_PWM  = 9;
const int RIGHT_PWM = 10;

const int MOTOR_SPEED = 120;

void stopRover() {
  analogWrite(LEFT_PWM, 0);
  analogWrite(RIGHT_PWM, 0);

  digitalWrite(LEFT_IN1, LOW);
  digitalWrite(LEFT_IN2, LOW);
  digitalWrite(RIGHT_IN1, LOW);
  digitalWrite(RIGHT_IN2, LOW);
}

void forward() {
  digitalWrite(LEFT_IN1, HIGH);
  digitalWrite(LEFT_IN2, LOW);
  digitalWrite(RIGHT_IN1, HIGH);
  digitalWrite(RIGHT_IN2, LOW);

  analogWrite(LEFT_PWM, MOTOR_SPEED);
  analogWrite(RIGHT_PWM, MOTOR_SPEED);
}

void backward() {
  digitalWrite(LEFT_IN1, LOW);
  digitalWrite(LEFT_IN2, HIGH);
  digitalWrite(RIGHT_IN1, LOW);
  digitalWrite(RIGHT_IN2, HIGH);

  analogWrite(LEFT_PWM, MOTOR_SPEED);
  analogWrite(RIGHT_PWM, MOTOR_SPEED);
}

void turnLeft() {
  digitalWrite(LEFT_IN1, LOW);
  digitalWrite(LEFT_IN2, HIGH);
  digitalWrite(RIGHT_IN1, HIGH);
  digitalWrite(RIGHT_IN2, LOW);

  analogWrite(LEFT_PWM, MOTOR_SPEED);
  analogWrite(RIGHT_PWM, MOTOR_SPEED);
}

void turnRight() {
  digitalWrite(LEFT_IN1, HIGH);
  digitalWrite(LEFT_IN2, LOW);
  digitalWrite(RIGHT_IN1, LOW);
  digitalWrite(RIGHT_IN2, HIGH);

  analogWrite(LEFT_PWM, MOTOR_SPEED);
  analogWrite(RIGHT_PWM, MOTOR_SPEED);
}

void setup() {
  Serial.begin(9600);

  pinMode(LEFT_IN1, OUTPUT);
  pinMode(LEFT_IN2, OUTPUT);
  pinMode(RIGHT_IN1, OUTPUT);
  pinMode(RIGHT_IN2, OUTPUT);

  pinMode(LEFT_PWM, OUTPUT);
  pinMode(RIGHT_PWM, OUTPUT);

  stopRover();

  Serial.println("SHELFNEX READY");
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  char command = Serial.read();

  switch (command) {
    case 'F':
      forward();
      Serial.println("FORWARD");
      break;

    case 'B':
      backward();
      Serial.println("BACKWARD");
      break;

    case 'L':
      turnLeft();
      Serial.println("LEFT");
      break;

    case 'R':
      turnRight();
      Serial.println("RIGHT");
      break;

    case 'S':
      stopRover();
      Serial.println("STOPPED");
      break;

    default:
      break;
  }