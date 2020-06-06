
byte second = 0;
byte first = 0;
byte d[] = {0,0,0};

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  d[0] = 1;
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_BUILTIN, HIGH); 
  first += 1;
  if (first % 256 == 0) second += 1; 
  d[1] = second;
  d[2] = first;
  Serial.write(d, 3);
  delay(10);                       
  digitalWrite(LED_BUILTIN, LOW);    
  first += 1;
  if (first % 256 == 0) second += 1; 
  d[1] = second;
  d[2] = first;
  Serial.write(d, 3);
  delay(10);                       
}
