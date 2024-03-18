// CE -> D7
// CSN -> D8
// SCK -> D13
// MO -> D11
// MI -> D12
#include <Servo.h>
#include<SPI.h>
#include<nRF24L01.h>
#include<Rf24.h>
#include "send.h"

Send send_info;

RF24 radio(7, 8);//CE, CSN
const byte address[6] = "00001";

Servo servo;

int motor_a = 3;
int motor_b = 2;
int throttle_val = 0;

void setup() {
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(0, address);
  radio.startListening();

  servo.attach(4);
  pinMode(motor_a, OUTPUT);
  pinMode(motor_b, OUTPUT);

  Serial.begin(2400);
  Serial.setTimeout(250);
  analogWrite(motor_b, 0);
}

void kick_start() {
  analogWrite(motor_a, 160);
  analogWrite(motor_b, 0);
  delay(500);
}

void loop() {
  while (radio.available()) {
    int data[2];
    radio.read(&data, sizeof(data));

    int steering_val = map(data[0], 3, 1003, 40, 130);
    servo.write(steering_val);

    int reverse_throttle_val = 0;

    if (data[1] > 520) {
      if (data[1] > 980) {
        data[1] = 980;
      }

      if (throttle_val == 0) {
        kick_start();
      }
      
      throttle_val = map(data[1], 520, 980, 90, 130);
      analogWrite(motor_a, throttle_val);
      analogWrite(motor_b, 0);
    } else {
      throttle_val = 0;
      analogWrite(motor_b, 0);
      analogWrite(motor_a, 0);
    }

    send_info.give(steering_val, throttle_val);
  }

  delay(5);
}
