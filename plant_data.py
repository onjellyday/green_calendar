import sqlite3
import requests
import xml.etree.cElementTree as ET

# 요청 URL 설정
list_url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
detail_url = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'

# 사용자 입력 받기
user_garden = input('식물의 이름을 입력하세요: ')

# 요청 변수 설정
params = {
    'apiKey': '20230502ORXOZHWL2KJR0FHIVQHWG',
    'numOfRows': '220'
}

# 세션 생성
session = requests.Session()

# 이름과 이름 코드 추출
response = session.get(list_url, params=params)
root = ET.fromstring(response.content)

# 식물의 이름과 코드 찾기
for plant in root.iter('item'):
    name = plant.find('.//cntntsSj').text
    if user_garden == name:
        name_code = plant.find('.//cntntsNo').text
        print('식물의 이름:', name)
        break
else:
    print('일치하는 식물의 이름을 찾을 수 없습니다.')
    exit()

# API 호출
params = {
    'apiKey': '20230502ORXOZHWL2KJR0FHIVQHWG',
    'cntntsNo': name_code,
}
response = session.get(detail_url, params=params)

# 응답 결과를 XML 형식으로 파싱
root = ET.fromstring(response.content)

# 식물의 정보 추출
species = root.find('.//fmlCodeNm').text
temperature = root.find('.//grwhTpCodeNm').text
lowest_temp = root.find('.//winterLwetTpCodeNm').text
humidity = root.find('.//hdCodeNm').text
light = root.find('.//lighttdemanddoCodeNm').text

# DB 생성 또는 연결
con = sqlite3.connect('plants.db')
cur = con.cursor()

# 식물 정보 저장 테이블 생성
cur.execute('''
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        name TEXT,
        temperature TEXT,
        humidity TEXT,
        light TEXT
    )
''')

# 사용자 입력 정보 DB에 저장
cur.execute("INSERT INTO plants (species, name, temperature, humidity, light) VALUES (?, ?, ?, ?, ?)",
            (species, name, temperature, humidity, light))
con.commit()

# 결과 출력
print(' 종:', species)
print(' 이름:', name)
print(' 온도:', temperature)
print(' 습도:', humidity)
print(' 조도:', light)

# DB 연결 종료
cur.close()
con.close()
