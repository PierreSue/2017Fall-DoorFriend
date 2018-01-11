#include <Ultrasonic.h>

#include <U8glib.h>
#include <Wire.h>

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

#include "images.h"

#define LOCK_PIN 2
#define BEEP_PIN 3
#define GREEN_PIN 4
#define RED_PIN 5
#define STRIP_PIN 6

#define RX_OPEN_PIN 8
#define RX_ALARM_PIN 9
#define RX_SPEAK_PIN 7
#define RX_BUSY_PIN 16

#define US_TRIG 14
#define US_ECHO 15

uint8_t rx_status;
uint8_t notify_status = 0;

unsigned long last_open_check;
unsigned long opened_since;
unsigned long alarmed_since;
unsigned long spinned_since;
bool opened;
bool alarmed;
bool fingerEnable = false;

SoftwareSerial fpSerial(11, 10);
U8GLIB_SH1106_128X64 u8g;
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fpSerial);
Ultrasonic hcsr04(US_TRIG, US_ECHO, 40000UL);

char busy_spinner[4][2] = { "|", "/", "-", "\\" };
uint8_t busy_idx = 0;
uint8_t busy_status = 0;

void setup() {
  rx_status = 0;
  
  pinMode(BEEP_PIN, OUTPUT);
  pinMode(LOCK_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(STRIP_PIN, OUTPUT);

  pinMode(RX_OPEN_PIN, INPUT);
  pinMode(RX_ALARM_PIN, INPUT);
  pinMode(RX_SPEAK_PIN, INPUT);
  pinMode(RX_BUSY_PIN, INPUT);

  Serial.begin(9600);
  finger.begin(57600);

  if(finger.verifyPassword()) fingerEnable = true;

  last_open_check = millis();
  spinned_since = millis();
  opened = false;
}

void draw() {
  if(opened) {
    u8g.drawBitmapP(0, 0, 16, 64, img_open);
  } else if(alarmed) {
    u8g.drawBitmapP(0, 0, 16, 64, img_alarm);
  } else if(notify_status == 0) {
    u8g.drawBitmapP(0, 0, 16, 64, img_pierre);
    u8g.setFont(u8g_font_unifont);
    if(busy_status == 1) {
      u8g.drawStr(0, 20, busy_spinner[busy_idx]);
    }
  } else if(notify_status == 1) {
    u8g.setFont(u8g_font_unifont);
    u8g.drawStr(0, 20, "Please speak");
    u8g.drawStr(0, 55, "something...");
  }
}

int getFingerprintIDez() {
  if(!fingerEnable) return -1;
  
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK) {
    return -1;
  }

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) {
    return -1;
  }

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK) {
    return -1;
  }
  
  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID); 
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID; 
}

void loop() {
  u8g.firstPage();  
  do {
    draw();
  } while( u8g.nextPage() );
  
  if(alarmed) {
    if(millis() - alarmed_since > 1500) {
      digitalWrite(RED_PIN, LOW);
      digitalWrite(BEEP_PIN, LOW);
      alarmed = false;
    }
    return;
  }
  if(opened) {
    if(millis() - opened_since > 150) {
      digitalWrite(BEEP_PIN, LOW);
    }
    if(millis() - opened_since > 1500) {
      digitalWrite(GREEN_PIN, LOW);
      digitalWrite(LOCK_PIN, LOW);
      opened = false;
    }
    return;
  }
  if(millis() - spinned_since > 100) {
    spinned_since = millis();
    busy_idx++;
    busy_idx %= 4;
  }
  if(millis() - last_open_check > 500) {
    last_open_check = millis();
    bool should_open = false;
    bool should_alarm = false;
    if(getFingerprintIDez() >= 0) should_open = true;
    
    if(rx_status == 2) {
      should_alarm = true;
    } else if(rx_status == 1) {
      should_open = true;
    }

    rx_status = 0;
    
    if(should_alarm) {
      alarmed_since = millis();
      alarmed = true;
      digitalWrite(BEEP_PIN, HIGH);
      digitalWrite(RED_PIN, HIGH);
      return;
    } else if(should_open) {
      opened_since = millis();
      opened = true;
      digitalWrite(LOCK_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);
      digitalWrite(BEEP_PIN, HIGH);
      return;
    }
  }
  if(hcsr04.distanceRead() < 100) {
    digitalWrite(STRIP_PIN, HIGH);
  } else {
    digitalWrite(STRIP_PIN, LOW);
  }
  
  if(digitalRead(RX_SPEAK_PIN) == LOW) notify_status = 1;
  else notify_status = 0;

  if(digitalRead(RX_BUSY_PIN) == LOW) busy_status = 1;
  else busy_status = 0;
  
  if(digitalRead(RX_ALARM_PIN) == LOW) rx_status = 2;
  else if(digitalRead(RX_OPEN_PIN) == LOW) rx_status = 1;
}
