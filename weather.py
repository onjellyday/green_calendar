import requests
import xml.etree.ElementTree as ET

start_day = 20230510
end_day = 20230519
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params ={'serviceKey' : 'NintYLVb0lkZfK3OI2n9UqvNbH7V5jTXlMGX5rz6UY/Z/kC4CH+j1ED2xjMiVbz8JWU7/amPPie/w/jraLWVNg==',
        'pageNo' : '1',
        'numOfRows' : '50',
        'dataType' : 'XML',
        'dataCd' : 'ASOS',
        'dateCd' : 'DAY',
        'startDt' : start_day,
        'endDt' : end_day,
        'stnIds' : '108' }
                        
response = requests.get(url, params=params)
response_xml = response.content.decode('utf-8')

root = ET.fromstring(response_xml)
items = root.findall('.//item')

total_avg_ta = 0.0
total_avg_rhm = 0.0
count = 0

for item in items:
    avg_ta = float(item.findtext('avgTa'))
    avg_rhm = float(item.findtext('avgRhm'))
    total_avg_ta += avg_ta
    total_avg_rhm += avg_rhm
    count += 1

final_avg_ta = total_avg_ta / count
final_avg_rhm = total_avg_rhm / count

print(f'최종 평균 온도: {final_avg_ta:.2f}')
print(f'최종 평균 습도: {final_avg_rhm:.2f}')