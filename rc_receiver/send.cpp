#include <Arduino.h>
#include "send.h"

void Send::give(int steer, int throttle) {
  if (Serial.available()) {
    String input_data = Serial.readStringUntil('\n');
    input_data.trim();

    if (input_data == "s") {
      Serial.print(steer);
      Serial.print(":");
      Serial.println(throttle);
    } else {
      Serial.println("N");
    }
  }
}
