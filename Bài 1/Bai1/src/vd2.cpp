//VD2: Ngắt led khi nhấn nút
#include <Arduino.h>

#define BUTTON_PIN 14
#define LED_PIN 12

volatile bool buttonPressed = false;

void IRAM_ATTR handleInterrupt() {
  buttonPressed = true;
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  ledcSetup(0, 5000, 8);
  ledcAttachPin(LED_PIN, 0);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), handleInterrupt, FALLING);
}

void loop() {
  static int brightness = 0, step = 1;

  if (buttonPressed) {
    buttonPressed = false;
    ledcWrite(0, 0); delay(80);
    ledcWrite(0, 255); delay(80);
  }

  brightness += step;
  if (brightness >= 255 || brightness <= 0) step = -step;
  ledcWrite(0, brightness);
  delay(10);
}