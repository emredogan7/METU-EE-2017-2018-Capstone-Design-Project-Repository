unsigned long volatile encodercount;
unsigned long encodercount_previous;
unsigned long volatile timer;
unsigned int angle;
boolean first;
boolean firstencodertick;
void setup() {
      angle=3;
      encodercount=0;
      encodercount_previous=0;
      Serial.begin(9600);
      while (!Serial); 
      pinMode(21,INPUT);  //Pin#21=interrupt pin, matched to interrupt#2
      attachInterrupt(digitalPinToInterrupt(2),speed,FALLING);
      first=true;
      firstecnodertick=true;
        }

  void loop() {
     delay(100); 

   if(encodercount==encodercount_previous&&encodercount!=0)
    {
   if(first)
     {
   Serial.println(millis()-timer);  //Steady State Time Taken 
   first=false;
     }
  Serial.println((encodercount); //Angle Moved in 0.1second.  
    }
  encodercount_previous=encodercount;
  encodercount=0;   
   }


  void speed(void)
 {
 if(firstencodertick)
 {
 timer=millis();
 firstencodertick=false;
  }
 encodercount++; 
}
