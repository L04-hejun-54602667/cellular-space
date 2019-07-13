//Joystick
const int inX = A0; //analog input for x-axis
const int inY = A1; //analog input for y-axis
const int inPressed =2; //input for whether the joystick is pressed
int xValue = 0;  
int yValue = 0;
int notPressed = 0;

//LED
const int ledPinA = 10;
const int ledPinB = 11;
const int ledPinC = 12;
int incomingByte;

//Time
const long INTERVAL = 1000;  // in ms                
unsigned long previousTime = 0;

void setup() {
  //Joystick
  pinMode(inX, INPUT); 
  pinMode(inY, INPUT);
  pinMode(inPressed, INPUT_PULLUP);

  //LED
  pinMode(ledPinA, OUTPUT);
  pinMode(ledPinB, OUTPUT);
  pinMode(ledPinC, OUTPUT);
  
  Serial.begin(9600); //baud rate
  //Serial.println("Ready"); 

}

void loop() {
  //Joystick
  xValue = analogRead(inX); //reading x value (range: 0--1023)
  int x=map(xValue,0,1023,10,15); // range: 10--15
  yValue = analogRead(inY);
  int y=map(yValue,0,1023,20,25); // range: 20--25
  notPressed = digitalRead(inPressed); //button state: 1 = not pressed,0 = pressed
  
  unsigned long currentTime = millis(); //Updates frequently
  if (currentTime - previousTime >= INTERVAL) {
    if (x == 10 || x == 15) {
      //Serial.print("X: ");
      Serial.println(x, DEC);
      previousTime = currentTime; //update timing 
    }
    if (y == 20 || y == 25) {
      //Serial.print("Y: ");
      Serial.println(y, DEC);
      previousTime = currentTime;
    }
    if (notPressed == 0) {
      //Serial.print("Not pressed: ");
      Serial.println(notPressed);
      previousTime = currentTime;
    }

  
  //LED
  if (Serial.available() > 0){
    incomingByte = Serial.read(); //read the oldest byte in the serial buffer
    if (incomingByte == '3'){ 
      digitalWrite(ledPinA, HIGH); 
      digitalWrite(ledPinB, HIGH);
      digitalWrite(ledPinC, HIGH);
      }

    if (incomingByte == '2'){
      digitalWrite(ledPinA, HIGH);
      digitalWrite(ledPinB, HIGH);
      digitalWrite(ledPinC, LOW);
      }
      
    if (incomingByte == '1'){
      digitalWrite(ledPinA, HIGH);
      digitalWrite(ledPinB, LOW);
      digitalWrite(ledPinC, LOW);
      }

    if (incomingByte == '0'){
      digitalWrite(ledPinA, LOW);
      digitalWrite(ledPinB, LOW);
      digitalWrite(ledPinC, LOW);
      }
    }
  }
}
