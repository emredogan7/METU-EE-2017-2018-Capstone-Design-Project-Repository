
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

int speed_1 = 0;
int speed_2 = 0;

int dir_1   = 1;
int dir_2   = 1;


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
  if(Serial.available() > 0)
  {
    String str = Serial.readStringUntil('\n');
    int val = str.toInt();
    int data_1 = val / 100;
    int data_2 = val - ( data_1 * 100 );

    speed_1 = data_1 / 10;
    speed_2 = data_2 / 10;

    dir_1 = data_1 - ( speed_1 * 10 );
    dir_2 = data_2 - ( speed_2 * 10 );
  }

  int pwmOutput1 = map(speed_1 * 20, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  int pwmOutput2 = map(speed_2 * 20, 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  analogWrite(enA, pwmOutput1); // Send PWM signal to L298N Enable pin
  analogWrite(enB, pwmOutput2);


  digitalWrite(in1,  dir_1);
  digitalWrite(in2, !dir_1);
  digitalWrite(in4,  dir_2);
  digitalWrite(in3, !dir_2);


}
/*
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
  while(!Serial){}
}
////////////

int input = 0;
  
int data_1= 0;
int data_2= 0;

int potValue_1 = 0;
int potValue_2 = 0;



bool dir_1 = 0;
bool dir_2 = 0;


int pwmOutput1 = 0; // Map the potentiometer value from 0 to 255
int pwmOutput2 = 0; // Map the potentiometer value from 0 to 255

////////////
void loop()
{
  if (Serial.available () > 3)
  {

  
  //int potValue1 = Serial.readString().toInt(); 
  //int dir =  potValue1 / 100 ;
  //potValue1 = potValue1 - dir * 100;

  input = Serial.readString().toInt();
  
  data_1 = input / 100;
  data_2 = input - ( data_1 * 100 );


  potValue_1 = data_1 / 10 ;
  potValue_2 = data_2 / 10 ;

  

  dir_1 = bool ( data_1 - (potValue_1 * 10) );
  dir_2 = bool ( data_2 - (potValue_2 * 10) );


  pwmOutput1 = map(potValue_1 * 20 , 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  pwmOutput2 = map(potValue_2 * 20 , 0, 1023, 0 , 255); // Map the potentiometer value from 0 to 255
  analogWrite(enA, pwmOutput1); // Send PWM signal to L298N Enable pin
  analogWrite(enB, pwmOutput2);
    
  digitalWrite(in1,  dir_1);
  digitalWrite(in2, !dir_1); 
  digitalWrite(in4,  dir_2);
  digitalWrite(in3, !dir_2); 






   
 

  //delay(10);
     
  }

  
}

*/
