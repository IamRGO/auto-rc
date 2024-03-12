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

void setup() {
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(0, address);
  radio.startListening();

  servo.attach(4);
  pinMode(motor_a, OUTPUT);
  pinMode(motor_b, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(100);
  analogWrite(motor_b, 0);
}

void loop() {
  radio.startListening();

  while (radio.available()) {
    int data[2];
    radio.read(&data, sizeof(data));

    int steering_val = map(data[0], 3, 1003, 40, 130);
    servo.write(steering_val);

    int throttle_val = 0;
    int reverse_throttle_val = 0;

    if (data[1] > 520) {
      if (data[1] > 980) {
        data[1] = 980;
      }
      throttle_val = map(data[1], 520, 980, 90, 147);
      analogWrite(motor_a, throttle_val);
      analogWrite(motor_b, 0);
    }

    else {
      analogWrite(motor_b, 0);
      analogWrite(motor_a, 0);
    }

    // fix this
    if (throttle_val >= 90) {
      send_info.give(steering_val, throttle_val);
    }
  }

  delay(20);
}
