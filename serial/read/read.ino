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


void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
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

void loop()
{
  if (Serial.available () > 0)
  {
    /*digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);
    Serial.read();
    delay(1000); */
    /*
  digitalWrite(2,HIGH);
  delayMicroseconds(1500);
  digitalWrite(2,LOW);
  delayMicroseconds(500);
*/
  
  int potValue1 = Serial.readString().toInt(); 
  
  //delay(100);
  //int potValue2 = Serial.read();
  int pwmOutput1 = map(potValue1, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  int pwmOutput2 = map(potValue1, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  analogWrite(enA, pwmOutput1); // Send PWM signal to L298N Enable pin
  analogWrite(enB, pwmOutput2);
  // Read button - Debounce

  // If button is pressed - change rotation direction
  
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in4, HIGH);
    digitalWrite(in3, LOW);
    delay(10);
     
  }
  
}

