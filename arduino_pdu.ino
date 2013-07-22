int ledPin = 13;
int PinBase = 2; 
int PinCount = 8 ;

void setup() {
  int i;
  // Setup a continuous bank of Pins for output
  for (i = PinBase; i < (PinBase+PinCount); i++)
      pinMode(i, OUTPUT);      // sets the digital pin as output
  // Enable Serial port 9600 8n1
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // read incoming serial data:
    char cmd = Serial.read();
    if (cmd = 'o'){
      char port = Serial.read();
      Serial.write("Port: ");
      Serial.write(port);

      char state = Serial.read();
      int iport = port - '0' + (PinBase-1);
       
      
      //usage:  o11 <== port 1 = on (1), off(0), toggle (2)
      //Read an 'o', we are good to go
      switch(state){
        case '0':
          Serial.write(" Off\n");
          digitalWrite(iport, LOW);
          break;
        case '1':
          Serial.write(" On\n");
          digitalWrite(iport, HIGH);
          break;
        case '2':
          Serial.write(" Toggle\n");
          digitalWrite(iport, LOW);
          delay(1000);
          digitalWrite(iport, HIGH);
          break;
      } 
    }
  }  
}
