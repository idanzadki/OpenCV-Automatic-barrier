
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position
// defines arduino pins numbers
const int trigPin = 12;
const int echoPin = 11;

bool isClose;
bool toOpen;
int count=0;
unsigned long time;


int sensor()
{
  // defines variables
  long duration;
  int distance;
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  //Serial.print("Distance from the object = ");
  //Serial.print(distance);
  //Serial.println(" cm");
  return distance;
}

bool isAbove()
{
  int dis = sensor();
  //Serial.println(dis);
  if (dis < 600)
  {
    Serial.println("Car above");
    return true;
  }
  else
  {
    Serial.println("No car detected");
    return false;
  }
}

void closeGate(int deg)
{
  for (pos = 0; pos < deg; pos += 1)
  { // goes from 0 degrees to x degrees
    myservo.write(pos);               // tell servo to go to position in variable 'pos'
    delay(5);                       // waits 15ms for the servo to reach the position
  }
}

void openGate(int deg)
{
  for (pos = deg; pos >= 1; pos -= 1)
  { // goes from x degrees to 0 degrees
    myservo.write(pos);               // tell servo to go to position in variable 'pos'
    delay(5);                        // waits 15ms for the servo to reach the position
  }
}

void setup()
{
  isClose = true;
  toOpen = false;
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication
}


void loop()
{

  
//  Serial.print("Time: ");
//  time = millis();
//  Serial.println(time); //prints time since program started
//  
  
  char input = Serial.read();
  Serial.println(isAbove());
  if(!isAbove())
  {
    
     if(!isClose)
      {
        if(count==0)
          Serial.println("Car leaved");
        count+=1;
      
        if(count==4)
        {
          closeGate(90);
          isClose = true;
          Serial.println("Gate close");
          count=0;
        }
      }
  }
  if (Serial.available() > 0)
  {
    if (input == 'o')
    {
      if (isClose)
      {
        openGate(90);
        isClose = false;
        Serial.println(" ");
      }
    }
    
  }


  delay(1000);
}
