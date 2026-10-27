#include <Arduino.h>

#define ADC_PIN 34   // ADC1
#define LED     12
#define N       8

int buf[N];
int idx = 0;
long sum = 0;

int loc(int m) {
  sum -= buf[idx];
  buf[idx] = m;
  sum += m;
  idx = (idx + 1) % N;
  return sum / N;
}

void setup() {
  Serial.begin(115200);

  ledcSetup(0, 5000, 8);
  ledcAttachPin(LED, 0);

  int first = analogRead(ADC_PIN);
  for (int i = 0; i < N; i++) buf[i] = first;
  sum = (long)first * N;
}

void loop() {
  int tho = analogRead(ADC_PIN);
  int l = loc(tho);

  ledcWrite(0, map(l, 0, 4095, 0, 255));

  Serial.print(millis());
  Serial.print(',');
  Serial.print(tho);
  Serial.print(',');
  Serial.println(l);

  delay(20);
}