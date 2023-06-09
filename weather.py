import requests
import xml.etree.ElementTree as ET
import sqlite3
import datetime
# SKY
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
url2 = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
serviceKey = 'NintYLVb0lkZfK3OI2n9UqvNbH7V5jTXlMGX5rz6UY/Z/kC4CH+j1ED2xjMiVbz8JWU7/amPPie/w/jraLWVNg=='

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
while current_date <= end_date + datetime.timedelta(days=1):
    # 날짜에 해당하는 온도와 습도 정보 가져오기
    params = {
        'serviceKey': serviceKey,
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
    average_lux = None
    for item in items:
        avg_ta = item.findtext('avgTa')
        avg_rhm = item.findtext('avgRhm')
        avg_lux = item.findtext('avgTca')
        if avg_ta and avg_rhm and avg_lux:
            average_temperature = float(avg_ta)
            average_humidity = float(avg_rhm)
            average_lux = float(avg_lux)
            print(average_temperature)
            break

    cur.execute("SELECT * FROM calendar WHERE date=?", (current_date,))
    existing_data = cur.fetchone()
    existing_lux = existing_data[3]
    if existing_lux is None:
        last_date = existing_data[0]
        # 데이터가 없을 경우에만 업데이트
        cur.execute("UPDATE calendar SET temperature=?, humidity=?, lux=? WHERE date=?", (average_temperature, average_humidity, average_lux, current_date))
    # 다음 날짜로 이동
    current_date += datetime.timedelta(days=1)
con.commit()
con.close()

def get_tmp_hum_lux(period):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = datetime.date.today() - datetime.timedelta(days=period)
    cur.execute("SELECT * FROM calendar WHERE date=?", (start_date,))
    total_avg_tmp = 0.0
    total_avg_hum = 0.0
    total_avg_lux = 0.0
    count = 0 
    while start_date <= end_date:
        cur.execute("SELECT * FROM calendar WHERE date=?",(start_date,))
        data = cur.fetchone()
        if data[1] is None:
            break
        else :
            tmp = data[1]
            hum = data[2]
            lux = data[3]
            total_avg_tmp += float(tmp)
            total_avg_hum += float(hum)
            total_avg_lux += float(lux)
            count += 1
            start_date += datetime.timedelta(days=1)
    
    final_avg_tmp = total_avg_tmp / count
    final_avg_hum = total_avg_hum / count
    final_avg_lux = total_avg_lux / count
    con.commit()
    con.close()
    return final_avg_tmp, final_avg_hum, final_avg_lux
    #return "{:.2f}".format(final_avg_tmp), "{:.2f}".format(final_avg_hum)