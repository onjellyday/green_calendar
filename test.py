import sqlite3
# sensor-2.txt 파일 경로
file_path = 'D:/sensor-2.txt'

# 파일 열기
with open(file_path, 'r') as file:
    # 파일의 모든 내용 읽기
    lines = file.readlines()

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
output_file_path = 'D:/sensor-average.txt'
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
