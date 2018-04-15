#include <Stepper.h>


#define outputA 52
#define outputB 50

int counter = 0; 
int dir = 0; 
int aState;
int aLastState;

Stepper myStepper(200, 47, 49, 51, 53);

void setup() { 

  pinMode (outputA,INPUT);
  pinMode (outputB,INPUT);

  Serial.begin (9600);
  // Reads the initial state of the outputA
  aLastState = digitalRead(outputA);

  // set the speed at 60 rpm:
  myStepper.setSpeed(60);

} 

void loop() { 

  aState = digitalRead(outputA); // Reads the "current" state of the outputA
  // If the previous and the current state of the outputA are different, that means a Pulse has occured

  if (aState != aLastState){     
    // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise

    if (digitalRead(outputB) != aState) { 

      counter ++;
      myStepper.step(50);

    } else {

      counter --;
      myStepper.step(-50);

    }

    Serial.print("Position: ");
    Serial.println(counter);
  } 

  aLastState = aState; // Updates the previous state of the outputA with the current state
}
