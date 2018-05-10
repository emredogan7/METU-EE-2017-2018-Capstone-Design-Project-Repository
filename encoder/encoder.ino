#define vccl A5
#define gndl A4
#define encal A2
#define encbl A3
#define vccr 7
#define gndr 9
#define encar 6
#define encbr 8


volatile long encoder0Pos=0;
long newposition;
long oldposition = 0;
unsigned long newtime;
unsigned long oldtime = 0;
long vel;

void setup()
{
  pinMode(vccr,OUTPUT);
  pinMode(gndr,OUTPUT);
  pinMode(vccl,OUTPUT);
  pinMode(gndl,OUTPUT);
  pinMode(encal,INPUT);
  pinMode(encar,INPUT);
  pinMode(encbr,INPUT);
  pinMode(encbl,INPUT);
  /* pinMode(encoder0PinA, INPUT_PULLUP);
  pinMode(encoder0PinB, INPUT_PULLUP); */
  
  //digitalWrite(encoder0PinA, HIGH);       // turn on pullup resistor
 
  //digitalWrite(encoder0PinB, HIGH);       // turn on pullup resistor
  attachInterrupt(0, doEncoder, RISING);    // encoDER ON PIN 2
  Serial.begin (9600);
  
}

void loop()
{
/* 
   noInterrupts();
 
  */

digitalWrite(vccr,HIGH);
digitalWrite(vccl,HIGH);
digitalWrite(gndr,LOW);
digitalWrite(gndl,LOW); 
/*newposition = encoder0Pos;
newtime = millis();
//vel = (newposition-oldposition)*1000/(newtime-oldtime);
//Serial.print ("speed = ");
//Serial.println (vel);

oldposition = newposition;
oldtime = newtime;
delay(250);*/
}

void doEncoder()
{
  if (digitalRead(encar) == HIGH) {
    encoder0Pos++;
  /*} else {
    encoder0Pos--;*/
  }
  Serial.println (encoder0Pos);
}

