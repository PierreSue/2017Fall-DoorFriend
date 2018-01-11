#include <U8glib.h>
#include <Wire.h>

#include "images.h"

#define LOCK_PIN 2
#define BEEP_PIN 3
#define GREEN_PIN 4
#define RED_PIN 5

#define RX_OPEN_PIN 8
#define RX_ALARM_PIN 9

uint8_t rx_status;

unsigned long last_open_check;
unsigned long opened_since;
unsigned long alarmed_since;
bool opened;
bool alarmed;

U8GLIB_SH1106_128X64 u8g;

void setup() {
  rx_status = 0;
  
  pinMode(BEEP_PIN, OUTPUT);
  pinMode(LOCK_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);

  pinMode(RX_OPEN_PIN, INPUT);
  pinMode(RX_ALARM_PIN, INPUT);

  Serial.begin(9600);

  last_open_check = millis();
  opened = false;
}

void draw() {
  if(opened) {
    u8g.drawBitmapP(0, 0, 16, 64, img_open);
  } else if(alarmed) {
    u8g.drawBitmapP(0, 0, 16, 64, img_alarm);
  } else {
    //u8g.setFont(u8g_font_unifont);
    //u8g.drawStr(0, 20, "Hello World!");
    u8g.drawBitmapP(0, 0, 16, 64, img_pierre);
  }
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
  if(millis() - last_open_check > 500) {
    last_open_check = millis();
    bool should_open = false;
    bool should_alarm = false;
    
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
  if(digitalRead(RX_ALARM_PIN) == LOW) rx_status = 2;
  else if(digitalRead(RX_OPEN_PIN) == LOW) rx_status = 1;
}
