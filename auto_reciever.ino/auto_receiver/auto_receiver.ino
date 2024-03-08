// CE -> D7
// CSN -> D8
// SCK -> D13
// MO -> D11
// MI -> D12
#include <Servo.h>
// #include<SPI.h>
// #include<nRF24L01.h>
// #include<Rf24.h>

// RF24 radio(7, 8);//CE, CSN
// const byte address[6] = "00001";

Servo servo;

int motor_a = 3;
int motor_b = 2;

void setup() {
  servo.attach(4);
  pinMode(motor_a, OUTPUT);
  pinMode(motor_b, OUTPUT);

  Serial.begin(19200);
  Serial.setTimeout(100);
  analogWrite(motor_b, 0);
}

void loop() {
  if (Serial.available()) {
    String input_data = Serial.readString();
    input_data.trim();

    if (input_data.charAt(0) == 'D') {
      int space_loc = input_data.indexOf(' ');
      String steering_str = input_data.substring(1, space_loc);
      String throttle_str = input_data.substring(space_loc + 1);


      int auto_steer = steering_str.toInt();
      int auto_throttle = throttle_str.toInt();

      analogWrite(motor_a, auto_throttle);
      analogWrite(motor_b, 0);

      servo.write(auto_steer);
    }
  }
  // delay(20);
}
