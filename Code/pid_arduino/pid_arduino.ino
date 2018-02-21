#include <TimerOne.h>
#include "TimerObject.h"
#include <PID_v1.h>

#define Kmes         2.55 // 255/100 from speed to duty constant       
#define PWM1          6                     // PWM motor pin ,Be careful in case of change to put the PWM to a pin able to generate PWM
#define encoder0PinA  2                      // DO NOT CHANGE THIS, FOR INTERRUPT NECESSARY!!

#define TIMERSTEP       1000000           // Defined as 1 sec (Arduino counts the time in microsecs) in order to set the frequency in a more user friendly way
//#define TIMERSTEP       8265            // Defined as 1 sec (Arduino counts the time in microsecs) in order to set the frequency in a more user friendly way

 TimerObject *timer1 = new TimerObject(4000);                        // If you change the TIMERSTEP, change the velocity equation as well accordingly

//volatile unsigned long int :if you dont get a desired value or accuracy for encoder readings change float to this


double timercounterA=0;  // counts the rising edges of the encoder reading
double velocityA=0;
double Setpoint=30;

double position1A=0;  // stores the previous position in order to calculate the velocity
double position2A=0;  // latest position
double D;
double count=0;
double Input;
double aggKp=1.16, aggKi=0.16, aggKd=0.44;
//double consKp=4.2, consKi=0.05, consKd=0;

//Specify the links and initial tuning parameters
PID myPID(&Input, &D, &Setpoint, aggKp, aggKi, aggKd, DIRECT);



void setup() {
  
  Timer1.initialize(TIMERSTEP);
  
  pinMode(PWM1, OUTPUT);
  pinMode(encoder0PinA, INPUT_PULLUP); // set the encoder 0 so that it is not floating
 

  Serial.begin(115200);
  setPwmFrequency(6, 8); //Sets the pwm output of 5 to around 8 to 9 kHz
  
    timer1->setOnTimer(&duty);
    timer1->Start();
       
  Timer1.attachInterrupt(callback);       //start interrupt on main using initialized Timer, helps to mask the variables also, if used somewhere else, the operation is not affected 
  // encoder pin on interrupt 0 (pin 2)
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoderA, CHANGE); // at each Timer1 period go to interrupt execute doEncoderA
  // encoder pin on interrupt 1 (pin 3)

  //turn the PID on
  myPID.SetMode(AUTOMATIC);

}

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x07; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}


void callback(){
   position2A=timercounterA;
  //velocityA=(position2A-position1A)*60/TIMERSTEP;  // DÖN GERİ
  velocityA=(position2A-position1A)*60/(182*3);
  position1A=position2A;
    Serial.print(Setpoint);
    Serial.print(",");
    Serial.print(D);
    Serial.print(",");
    Serial.println(velocityA);
 
    
  }

 void duty(){
  

 
      D=100;
  }
  
void loop() {


         if (Serial.available()>0){
        Setpoint=Serial.parseInt();
        }

        
// put your main code here, to run repeatedly:
       timer1->Update(); 
         Input = velocityA;

  double gap = abs(Setpoint-Input)*Kmes; //distance away from duty setpoint

     myPID.SetTunings(aggKp, aggKi, aggKd);

       myPID.Compute();  
       analogWrite(PWM1, D);


}

void doEncoderA() {
  timercounterA ++;
}
