#include <DHT.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

SoftwareSerial bluetooth(2, 3); // Bluetooth 모듈 RX, TX 핀 설정

int address = 0; // EEPROM 주소 변수

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600); // Bluetooth 시리얼 통신 속도 설정
  dht.begin();
}

void loop() {
  float humi, temp; // 온습도 변수
  int sensorValue;

  sensorValue = analogRead(A0); // 조도
  temp = dht.readTemperature(); // 온도
  humi = dht.readHumidity(); // 습도

  // EEPROM에 데이터 저장
  EEPROM.put(address, sensorValue);
  address += sizeof(sensorValue);
  EEPROM.put(address, temp);
  address += sizeof(temp);
  EEPROM.put(address, humi);
  address += sizeof(humi);

  // 시리얼 통신을 통해 데이터 출력
  Serial.print(sensorValue);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.println(humi);

  // 블루투스를 통해 데이터 송신
  bluetooth.print(sensorValue);
  bluetooth.print(",");
  bluetooth.print(temp);
  bluetooth.print(",");
  bluetooth.println(humi);

  delay(5000);
}