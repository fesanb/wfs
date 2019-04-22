/* update
  WFS - Wind and Forecast Station program by Stefan Bahrawy
  This is developed for measuring wind, and read wather data to predict weather changes.

This is code for the Nano running the Frequency counter via pulseIn(). 

*/

int f;
float w;
String ss = "";
void setup() {
  Serial.begin(19200);

}

void loop() {
  f = 525000 / pulseIn(4, HIGH);
  if(f>0){
  w = f * 0.1;
  ss += "<";
  ss += w;
  ss += ">";
  Serial.println(ss);
  ss = "";
  }
}
