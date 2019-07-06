/*
  WFS - Wind and Forecast Station program by Stefan Bahrawy
  This is developed for measuring wind, and read wather data to predict weather changes.

  WFS consists of:
  - 1pcs Arduino Mega
  - 1pcs Arduino Nano
  - 1pcs Raspberry Pi 3

  Mega handles:
  - GPS via serial
  - Wind via serial from Nano
  - DHT22
  - BMP320
  # Mega collects data to serial strings and sends to RPI

   NANO
   - for now uses Pulsein() to read wind unintereupted and sends via serial to Mega.

*/
// == INCLUDES =====================================
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <DHT.h>;
#include <Adafruit_BMP280.h>
#include <SPI.h>
// ===========

// == GPS SETTINGS =====================================
static const int RXPin = 19, TXPin = 18;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

//GPS
float gpslong;
float gpslat;
float gpsalt;
int gpssat;
int gpsdo = 0;
// ===========

// == SENSOR SETTINGS =====================================
Adafruit_BMP280 bme;
//DHT22 - Defenitions
#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

float temp;
float hum;
int atp;
int sensdoboot = 1;
// ===========

// == INTERVALS =====================================
//Intervals - Keep arduino from reading and sending data constantly
unsigned long sensorinterval = 2000; // org int: "180000", current only for testing forecast check interval
unsigned long sensorMillis = 0; //forecast check interval

unsigned long GPSinterval = 60000; //GPS check interval 900000
unsigned long GPSduration = 50;
unsigned long GPSMillis = 0; //GPS check interval

// ===============

// == SERIAL FROM NANO =====================================
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing
float wind = 0.0;                // variables to hold the parsed data
boolean newData = false;
// ===============

// == SERIAL TO RPI =====================================
String windserial;
String gpsserial;
String sensorserial;
int handshake = 0;
// ===============

void setup() {
  Serial.begin(19200);
  Serial2.begin(19200);
  ss.begin(GPSBaud);
  dht.begin();
  bme.begin();

}
//============

void serialhandshake() {
  unsigned long handshakemillis = 0;
  String handshakecode = "S"; // Capital S
  String receive;

  while (handshake == 0) {

    if ((millis() - handshakemillis) > 1000) {
      Serial.println(handshakecode);
      handshakemillis = millis();
    }
    
    while(Serial.available()) {
      receive = Serial.read();
      if(receive = handshakecode){
        handshake = 1;
      }
    }}
}

void loop() {
  if (handshake == 0) { // makes sure the serial connection between the Androind and RPI is established before startting. 
    serialhandshake();
  } else {

    if ((millis() - GPSMillis) > GPSinterval) {
      readgpsdata();
      gpsserial += "GPS,";
      gpsserial += gpslat;
      gpsserial += ",";
      gpsserial += gpslong;
      gpsserial += ",";
      gpsserial += gpsalt;
      gpsserial += ",";
      gpsserial += gpssat;
      Serial.println(gpsserial);
      gpsserial = "";
      GPSMillis = millis();
      if (GPSinterval < 3840000) {
        if (gpslat > 0.00) {
          GPSinterval = GPSinterval * 2;
        }
      }
    }


    if (sensdoboot == 1) {
      readsensors();
      sensorserial += "SENS,";
      sensorserial += temp;
      sensorserial += ",";
      sensorserial += hum;
      sensorserial += ",";
      sensorserial += atp;
      Serial.println(sensorserial);
      sensorserial = "";
      sensdoboot = 0;
    }

    if ((millis() - sensorMillis) > sensorinterval) {
      readsensors();
      sensorserial += "SENS,";
      sensorserial += temp;
      sensorserial += ",";
      sensorserial += hum;
      sensorserial += ",";
      sensorserial += atp;
      Serial.println(sensorserial);
      sensorserial = "";
      sensorMillis = millis();
    }

    recvWithStartEndMarkers();
    if (newData == true) {
      strcpy(tempChars, receivedChars);
      parseData();
      newData = false;
      showParsedData();
    }

  }
}
  //============

  void readgpsdata() {
    while (ss.available() > 0)
      if (gps.encode(ss.read()))
        gpslat = gps.location.lat();
    gpslong = gps.location.lng();
    gpsalt = gps.altitude.meters();
    gpssat = gps.satellites.value();
  }

  void readsensors() {
    temp = bme.readTemperature();
    hum = dht.readHumidity();
    atp = bme.readPressure() / 100;
  }

  void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial2.available() > 0 && newData == false) {
      rc = Serial2.read();

      if (recvInProgress == true) {
        if (rc != endMarker) {
          receivedChars[ndx] = rc;
          ndx++;
          if (ndx >= numChars) {
            ndx = numChars - 1;
          }
        }
        else {
          receivedChars[ndx] = '\0'; // terminate the string
          recvInProgress = false;
          ndx = 0;
          newData = true;
        }
      }

      else if (rc == startMarker) {
        recvInProgress = true;
      }
    }
  }

  //============

  void parseData() {      // split the data into its parts
    char * strtokIndx; // this is used by strtok() as an index
    strtokIndx = tempChars;      // get the first part - the string
    wind = atof(strtokIndx);     // convert this part to a float
  }

  void showParsedData() {
    windserial += "w,";
    windserial += wind;
    windserial += "";
    Serial.println(windserial);
    windserial = "";
  }
