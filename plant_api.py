import sqlite3
import requests
import xml.etree.cElementTree as ET

# DB 생성 또는 연결
con = sqlite3.connect('plants_table.db')
cur = con.cursor()

# 식물 정보 저장 테이블 생성
cur.execute('''
    CREATE TABLE IF NOT EXISTS plants_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        name TEXT,
        temperature TEXT,
        lowest_temp TEXT,
        humidity TEXT,
        light TEXT
    )
''')

# 요청 URL 설정
list_url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
detail_url = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'

# 요청 변수 설정
params = {
    'apiKey': '20230502ORXOZHWL2KJR0FHIVQHWG',
    'numOfRows': '220'
}

# 세션 생성
session = requests.Session()

# 이름과 이름 코드 추출
response = session.get(list_url, params=params)
print(response.text)  # API 응답 데이터 확인

root = ET.fromstring(response.content)

# 식물의 이름과 코드 찾기
for plant in root.iter('item'):
    name = plant.find('.//cntntsSj').text
    code = plant.find('.//cntntsNo').text

    detail_params = {
        'apiKey': '20230502ORXOZHWL2KJR0FHIVQHWG',
        'cntntsNo': code
    }

    detail_response = session.get(detail_url, params=detail_params)
    print(detail_response.text)  # API 응답 데이터 확인

    # 응답 결과를 XML 형식으로 파싱
    detail_root = ET.fromstring(detail_response.content)

    # 식물의 정보 추출
    species = detail_root.find('.//fmlCodeNm').text
    temperature = detail_root.find('.//grwhTpCodeNm').text
    lowest_temp = detail_root.find('.//winterLwetTpCodeNm').text
    humidity = detail_root.find('.//hdCodeNm').text
    light = detail_root.find('.//lighttdemanddoCodeNm').text
    
    # 사용자 입력 정보 DB에 저장
    cur.execute("INSERT INTO plants_table (species, name, temperature, lowest_temp, humidity, light) VALUES (?, ?, ?, ?, ?, ?)",
                (species, name, temperature, lowest_temp, humidity, light))
    con.commit()

con.close()
