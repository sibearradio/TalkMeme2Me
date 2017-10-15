const int buttonPin = 2;

boolean sent = false;
int buttonState = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) 
  {
      if(sent == false)
      {
        sent = true;
        Serial.println("nuke");
      }
      
  }
}
