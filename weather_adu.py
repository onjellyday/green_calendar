import sqlite3
import datetime
import os
def get_sensor_data(file_path):
    # 파일이 존재하는지 확인
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    else:
        return None

# 파일 경로 목록
file_paths = ['D:/sensor-2.txt', 'E:/sensor-2.txt', 'F:/sensor-2.txt', 'G:/sensor-2.txt']

# 데이터 가져오기
lines = None
for file_path in file_paths:
    lines = get_sensor_data(file_path)
    if lines:
        break

# 데이터 파싱 및 날짜별 평균 계산
data = {}
for line in lines:
    line = line.strip()
    values = line.split(',')
    date = values[0]
    temperature = float(values[2])
    humidity = float(values[3])
    brightness = int(values[4])

    if date not in data:
        data[date] = {'temperature': [], 'humidity': [], 'brightness': []}

    data[date]['temperature'].append(temperature)
    data[date]['humidity'].append(humidity)
    data[date]['brightness'].append(brightness)

# 평균 계산
averages = {}
for date, values in data.items():
    averages[date] = {
        'temperature': sum(values['temperature']) / len(values['temperature']),
        'humidity': sum(values['humidity']) / len(values['humidity']),
        'brightness': sum(values['brightness']) / len(values['brightness'])
    }

# sensor-average.txt 파일에 저장
output_file_path = 'sensor-average.txt'
with open(output_file_path, 'w') as output_file:
    for date, values in averages.items():
        output_line = f"{date},{values['temperature']:.2f},{values['humidity']:.2f},{values['brightness']:.2f}\n"
        output_file.write(output_line)

# 데이터베이스 연결
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 테이블 생성 쿼리
create_table_query = '''
CREATE TABLE IF NOT EXISTS weather (
    datetime TEXT,
    temperature REAL,
    humidity REAL,
    lux INTEGER
);
'''

# 테이블 생성
cursor.execute(create_table_query)

# 커밋 및 연결 종료
conn.commit()
conn.close()
def get_adu(period):
    # 데이터베이스 연결
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 텍스트 파일 읽기
    with open(output_file_path, 'r') as file:
        lines = file.readlines()

    # 데이터 삽입
    for line in lines:
        line = line.strip()  # 줄바꿈 문자 제거
        data = line.split(',')  # 데이터 분리
        query = '''
        INSERT INTO weather (datetime, temperature, humidity, lux)
        VALUES (?, ?, ?, ?);
        '''
        cursor.execute(query, (data[0], data[2], data[1], data[3]))

    # 커밋 및 연결 종료
    conn.commit()
    conn.close()

    # 데이터베이스 연결
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 가장 최신의 값부터 period 개 이전의 값 가져오기
    query = f'''
    SELECT temperature, humidity, lux
    FROM weather
    ORDER BY datetime DESC
    LIMIT {period};
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # 각 센서 값의 평균 계산
    temperature_sum = 0
    humidity_sum = 0
    lux_sum = 0
    count = 0
    for row in rows:
        temperature_sum += row[0]
        humidity_sum += row[1]
        lux_sum += row[2]
        count += 1
    temperature_avg = temperature_sum / count
    humidity_avg = humidity_sum / count
    lux_avg = lux_sum / count

    # 연결 종료
    conn.close()

    return temperature_avg, humidity_avg, lux_avg

