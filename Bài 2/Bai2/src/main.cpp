//Debounce 60ms
#include <Arduino.h>

#define BUTTON_PIN 14
#define LED_PIN 12

#define DEBOUNCE_MS 60

volatile bool buttonPressed = false;
volatile uint32_t debouncedCount = 0;
volatile uint32_t rawEdgeCount = 0;
volatile unsigned long lastInterruptTime = 0;

void IRAM_ATTR handleInterrupt() {
  rawEdgeCount++;

  unsigned long now = millis();

  if (now - lastInterruptTime >= DEBOUNCE_MS) {
    debouncedCount++;
    lastInterruptTime = now;
    buttonPressed = true;
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  ledcSetup(0, 5000, 8);
  ledcAttachPin(LED_PIN, 0);

  attachInterrupt(
    digitalPinToInterrupt(BUTTON_PIN),
    handleInterrupt,
    FALLING
  );

  Serial.println("Bat dau kiem tra chong doi nut nhan");
  Serial.print("Nguong debounce: ");
  Serial.print(DEBOUNCE_MS);
  Serial.println(" ms");
}

void loop() {
  static int brightness = 0;
  static int step = 1;
  static uint32_t lastRaw = 0;
  static uint32_t lastDebounced = 0;

  bool pressed;

  noInterrupts();
  pressed = buttonPressed;
  buttonPressed = false;

  uint32_t raw = rawEdgeCount;
  uint32_t debounced = debouncedCount;
  interrupts();

  if (pressed) {
    ledcWrite(0, 0);
    delay(80);
    ledcWrite(0, 255);
    delay(80);
  }

  brightness += step;

  if (brightness >= 255) {
    brightness = 255;
    step = -1;
  } else if (brightness <= 0) {
    brightness = 0;
    step = 1;
  }

  ledcWrite(0, brightness);

  if (raw != lastRaw || debounced != lastDebounced) {
    Serial.print(millis());
    Serial.print(',');
    Serial.print(raw);
    Serial.print(',');
    Serial.println(debounced);

    lastRaw = raw;
    lastDebounced = debounced;
  }

  delay(10);
}