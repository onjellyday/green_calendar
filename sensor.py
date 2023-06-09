import serial
import sqlite3
from datetime import datetime

# 시리얼 포트 설정
serial_port = 'COM5'  # Arduino와 연결된 시리얼 포트 번호로 변경해야 합니다.
baud_rate = 9600

# SQLite3 데이터베이스 연결
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()

# 기존 테이블 삭제
drop_table_query = '''
DROP TABLE IF EXISTS sensor_data;
'''
c.execute(drop_table_query)

# 새로운 테이블 생성
create_table_query = '''
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    temperature REAL,
    humidity REAL,
    brightness INTEGER
);
'''
c.execute(create_table_query)

# 데이터베이스에 데이터 저장하는 함수
def save_to_database(temperature, humidity, brightness):
    timestamp = datetime.now()  # 현재 날짜와 시간 가져오기
    insert_query = '''
    INSERT INTO sensor_data (timestamp, temperature, humidity, brightness)
    VALUES (?, ?, ?, ?)
    '''
    c.execute(insert_query, (timestamp, temperature, humidity, brightness))
    conn.commit()

# 시리얼 통신을 통해 Arduino에서 데이터를 수신하여 데이터베이스에 저장
def receive_data_and_save():
    ser = serial.Serial(serial_port, baud_rate)

    while True:
        # 시리얼 통신으로 데이터 수신
        line = ser.readline().decode().strip()

        # 데이터 파싱
        data = line.split(',')
        sensorValue = int(data[0])
        temp = float(data[1])
        humi = float(data[2])

        # 데이터베이스에 저장
        save_to_database(temp, humi, sensorValue)

# 데이터 수신 및 저장 실행
receive_data_and_save()

# 데이터베이스 연결 종료
conn.close()