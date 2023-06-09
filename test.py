import requests
import xml.etree.ElementTree as ET
import datetime

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
serviceKey = 'NintYLVb0lkZfK3OI2n9UqvNbH7V5jTXlMGX5rz6UY/Z/kC4CH+j1ED2xjMiVbz8JWU7/amPPie/w/jraLWVNg=='
current_date2 = datetime.date(2023, 6, 8)
end_date = datetime.date.today()
while current_date2 <= end_date:
    A = []
    for i in range(24):
        A.append(f'{i:02d}00')
    index = 0
    count = 0
    sum = 0
    avg = 0
    while index < len(A):
        params = {
            'serviceKey': serviceKey,
            'pageNo': '1',
            'numOfRows': '50',
            'dataType': 'XML',
            'base_date': current_date2.strftime('%Y%m%d'),
            'base_time': A[index],
            'nx': '61',
            'ny': '127'
        }
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        sky_code = None
        for item in root.iter("item"):
            category = item.find("category").text
            fcst_value = item.find("fcstValue").text
            if category == "SKY":
                sky_code = fcst_value
        print("일자, 시간 : ",A[index])
        print("하늘 상태(SKY) 값:", sky_code)
        index += 1
    current_date2 += datetime.timedelta(days=1)
