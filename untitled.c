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

int speed_1 = 9; //bu dörtlü önceden belirlenmek zorunda
int speed_2 = 9;

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
    // bu kod 4 charlık string e göre yazıldı
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
