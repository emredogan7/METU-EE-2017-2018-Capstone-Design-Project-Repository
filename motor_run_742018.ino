#define enA A0
#define enB A1
#define in1 2
#define in2 3
#define in3 4
#define in4 5

void setup() {
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(enA,OUTPUT);
  pinMode(enB,OUTPUT);
}

void loop() {
/*
  digitalWrite(2,HIGH);
  delayMicroseconds(1500);
  digitalWrite(2,LOW);
  delayMicroseconds(500);
*/

  int potValue = 100;
  int pwmOutput = map(potValue, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  analogWrite(enA, pwmOutput); // Send PWM signal to L298N Enable pin
  analogWrite(enB, pwmOutput);
  // Read button - Debounce

  // If button is pressed - change rotation direction
  
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in4, HIGH);
    digitalWrite(in3, LOW);
    delay(5);
    
}
