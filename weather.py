import requests
import xml.etree.ElementTree as ET
import sqlite3
import datetime
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'

# SQLite 데이터베이스 연결
con = sqlite3.connect('database.db')
cur = con.cursor()
start_date = datetime.date(2023, 5, 1)
end_date = datetime.date.today()

while True:
    cur.execute("SELECT * FROM calendar WHERE date=?", (start_date,))
    existing_data = cur.fetchone()
    existing_temperature = existing_data[1]
    if existing_temperature is None:
        last_date = existing_data[0]
        break
    start_date += datetime.timedelta(days=1)
current_date = start_date
while current_date <= end_date:
    # 날짜에 해당하는 온도와 습도 정보 가져오기
    params = {
        'serviceKey': 'NintYLVb0lkZfK3OI2n9UqvNbH7V5jTXlMGX5rz6UY/Z/kC4CH+j1ED2xjMiVbz8JWU7/amPPie/w/jraLWVNg==',
        'pageNo': '1',
        'numOfRows': '50',
        'dataType': 'XML',
        'dataCd': 'ASOS',
        'dateCd': 'DAY',
        'startDt': current_date.strftime('%Y%m%d'),
        'endDt': current_date.strftime('%Y%m%d'),
        'stnIds': '108'
    }
    response = requests.get(url, params=params)
    response_xml = response.content.decode('utf-8')
    root = ET.fromstring(response_xml)
    items = root.findall('.//item')

    average_temperature = None
    average_humidity = None

    for item in items:
        avg_ta = item.findtext('avgTa')
        avg_rhm = item.findtext('avgRhm')
        if avg_ta and avg_rhm:
            average_temperature = float(avg_ta)
            average_humidity = float(avg_rhm)
            print(average_temperature)
            break

    cur.execute("SELECT * FROM calendar WHERE date=?", (current_date,))
    existing_data = cur.fetchone()
    existing_temperature = existing_data[1]

    if existing_temperature is None:
        last_date = existing_data[0]
        # 데이터가 없을 경우에만 업데이트
        cur.execute("UPDATE calendar SET temperature=?, humidity=? WHERE date=?", (average_temperature, average_humidity, current_date))
    # 다음 날짜로 이동
    current_date += datetime.timedelta(days=1)

# 변경사항 저장 및 연결 종료
con.commit()
con.close()

def get_tmp_hum(period):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = datetime.date.today() - datetime.timedelta(days=period)
    cur.execute("SELECT * FROM calendar WHERE date=?", (start_date,))
    total_avg_tmp = 0.0
    total_avg_hum = 0.0
    count = 0    
    while start_date <= end_date:
        cur.execute("SELECT * FROM calendar WHERE date=?",(start_date,))
        data = cur.fetchone()
        if data[1] is None:
            break
        else :
            tmp = data[1]
            hum = data[2]
            total_avg_tmp += float(tmp)
            total_avg_hum += float(hum)
            count += 1
            start_date += datetime.timedelta(days=1)
    
    final_avg_tmp = total_avg_tmp / count
    final_avg_hum = total_avg_hum / count
    con.commit()
    con.close()
    return (final_avg_tmp), final_avg_hum
    #return "{:.2f}".format(final_avg_tmp), "{:.2f}".format(final_avg_hum)