#include <SPI.h>
#include <SD.h>
#include "DHT.h"
#include<DS1302.h>
#define DHTPIN 8
#define DHTTYPE DHT11
#define DS1302_CLK_PIN 5
#define DS1302_DAT_PIN 6
#define DS1302_RST_PIN 7
DHT dht(DHTPIN, DHTTYPE);

const int chipSelect = 10;
DS1302 rtc(DS1302_RST_PIN,DS1302_DAT_PIN, DS1302_CLK_PIN);

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  rtc.halt(false);
  rtc.writeProtect(false);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    // don't do anything more:
    while (1);
  }
 // Serial.println("card initialized.");
    dht.begin();
}

void loop() {
  File dataFile = SD.open("sensor-2.txt", FILE_WRITE);

  if (dataFile) {
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      int lux = analogRead(A0);
      String strBuff1 = String(rtc.getDateStr(2,1,'-')); 
      String strBuff2 = String(rtc.getTimeStr());
      //String strBuff = String(rtc.getDateStr(2,1,'-')); //�����δ� ��¥�� �ʿ� 

    String data = strBuff1+ ","+ strBuff2 + "," + String(h) + "," + String(t) + "," + String(lux); // ���� �µ� ����
    dataFile.println(data);
    dataFile.close();
    Serial.println(data);
  }
  else {
    Serial.println("error opening datalog.txt");
  }

  delay(60000);
}

