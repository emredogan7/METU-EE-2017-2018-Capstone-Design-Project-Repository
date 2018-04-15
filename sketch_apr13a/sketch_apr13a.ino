#define vccl A5
#define gndl A4
#define encal A2
#define encbl A3
#define vccr 7
#define gndr 9
#define encar 6
#define encbr 8

void setup() {
  // put your setup code here, to run once:
  pinMode(vccr,OUTPUT);
  pinMode(gndr,OUTPUT);
  pinMode(vccl,OUTPUT);
  pinMode(gndl,OUTPUT);
  pinMode(encal,INPUT);
  pinMode(encar,INPUT);
  pinMode(encbr,INPUT);
  pinMode(encbl,INPUT);
  Serial.begin(9600);

pinMode (2,INPUT_PULLUP);
 pinMode (3,INPUT_PULLUP);

//attachInterrupt(0, EncoderA, RISING);
//attachInterrupt(1, EncoderB, RISING);

    }

/*void EncoderA()
{
if (digitalRead(encal) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(encbl) == LOW) {  
      encoder0Pos = encoder0Pos + 1;         // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encbl) == HIGH) {   
      encoder0Pos = encoder0Pos + 1;          // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
  Serial.println (encoder0Pos, DEC);          
  

}
*/
void loop() {
  // put your main code here, to run repeatedly:
int encpos1=0;
int encpos2=0;

  digitalWrite(vccr,HIGH);
  digitalWrite(vccl,HIGH);
  digitalWrite(gndr,LOW);
  digitalWrite(gndl,LOW);
  // motorRun.Update();
  if (digitalRead(encal)==HIGH){
encpos1=encpos1 + 1;}
  if (digitalRead(encbl)==HIGH){
encpos2=encpos2 + 1;}
Serial.println(encpos1, DEC);
Serial.println(encpos2, DEC);

}
