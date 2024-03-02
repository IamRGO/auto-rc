#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int a = A0;
int b = A1;

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

int steering_input = A0;
int throttle_input = A1;

void setup() {
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.stopListening();
}

void loop() {
  int steering_value = analogRead(a);
  int throttle_value = analogRead(b);
  int data[] = { steering_value, throttle_value };
  radio.write(&data, sizeof(data));  
  delay(50);
}
