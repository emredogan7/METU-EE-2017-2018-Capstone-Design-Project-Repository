#include <PID_v1.h>

#define enA 10
#define enB 11
#define in1 2
#define in2 3
#define in3 4
#define in4 5
#define trigr 13
#define echor 12
#define trigl A0
#define echol A1


void setup() {
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(enA,OUTPUT);
  pinMode(enB,OUTPUT);
  pinMode(trigr,OUTPUT);
  pinMode(trigl,OUTPUT);
  pinMode(echor,INPUT);
  pinMode(echol,INPUT);
  Serial.begin(9600);
}

void loop() {
/*
  digitalWrite(2,HIGH);
  delayMicroseconds(1500);
  digitalWrite(2,LOW);
  delayMicroseconds(500);
*/

  int potValue1 = 20;
  int potValue2 = 80;
  int pwmOutput1 = map(potValue1, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  int pwmOutput2 = map(potValue2, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  analogWrite(enA, pwmOutput1); // Send PWM signal to L298N Enable pin
  analogWrite(enB, pwmOutput2);
  // Read button - Debounce

  // If button is pressed - change rotation direction
  
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in4, HIGH);
    digitalWrite(in3, LOW);
    delay(5);
    
}
