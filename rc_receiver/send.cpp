#include <Arduino.h>
#include "send.h"
//#include <Servo.h>
//
//Servo servo;
//int motor_a = 3;
//int motor_b = 2;
//
//void setup() {
//  servo.attach(4);
//  pinMode(motor_a, OUTPUT);
//  pinMode(motor_b, OUTPUT);
//
//  Serial.begin(9600);
//  analogWrite(motor_b, 0);
//}

void Send::give(int steer, int throttle) {
  if (Serial.available()) {
    String input_data = Serial.readString();
    input_data.trim();

    if (input_data == "stats") {
      Serial.println(steer);
      Serial.println(throttle);
    }
//    else if (input_data[0] == "D") {
//      float auto_steer = input_data[1] + input_data[2] + input_data[3];
//      int auto_throttle = input_data[12];
//
//      analogWrite(motor_a, auto_throttle);
//      analogWrite(motor_b, 0);
//
//      auto_throttle = map(auto_throttle, 3, 1003, 40, 130);
//      servo.write(auto_throttle);
//    }
    else {
      Serial.println("I don't understand");
      Serial.println(input_data);
    }
  }
}
