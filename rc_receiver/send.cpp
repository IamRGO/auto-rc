#include <Arduino.h>
#include "send.h"

void Send::give(int steer, int throttle) {
  if (Serial.available()) {
    String input_data = Serial.readString();
    input_data.trim();

    if (input_data == "stats") {
      Serial.print(steer);
      Serial.print(":");
      Serial.println(throttle);
    } else {
      Serial.println("I don't understand");
    }
  }
}
