from bs4 import BeautifulSoup as BS
import requests as req
import sqlite3
def get_plant_info(plants_name):
    url_1 = "https://fuleaf.com/search?term=" + plants_name
    res = req.get(url_1)
    soup = BS(res.text, 'html.parser')

    links = []
    for a in soup.find_all('a'):
        link = a.get('href')
        if link is not None and '/plants/count/' in link:
            links.append(link)

    if not links:
        print("식물 정보가 존재하지 않습니다.")
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        # 식물 정보 저장 테이블 생성
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users_plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                temperature TEXT,
                humidity TEXT,
                light TEXT,
                watercycle TEXT,
                water_detail TEXT
            )
        ''')
        cur.execute("INSERT INTO users_plants (name, temperature, humidity, light, watercycle, water_detail) VALUES (?, ?, ?, ?, ?, ?)",
                    (plants_name, None, None, None, None, None))
        con.commit()
        con.close
    else:
        print(links[0])
        code = links[0].split('/')[-1]
        url_2 = "https://fuleaf.com/plants/detail/" + code

        res_2 = req.get(url_2)
        soup_2 = BS(res_2.text, 'html.parser')

        plant_info = soup_2.select('.table-item-title')
        plant_info2 = soup_2.select('.table-item-desc')

        if not plant_info:
            print("식물 정보가 존재하지 않습니다.")
            con = sqlite3.connect('database.db')
            cur = con.cursor()

            # 식물 정보 저장 테이블 생성
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users_plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    temperature TEXT,
                    humidity TEXT,
                    light TEXT,
                    watercycle TEXT,
                    water_detail TEXT
                )
            ''')
            cur.execute("INSERT INTO users_plants (name, temperature, humidity, light, watercycle, water_detail) VALUES (?, ?, ?, ?, ?, ?)",
                    (plants_name, None, None, None, None, None))
            con.commit()
            con.close
        plant_info_text = []
        for info in plant_info:
            plant_info_text.append(info.text.strip())

        plant_info2_text = []
        for info2 in plant_info2:
            plant_info2_text.append(info2.text.strip())

        if plant_info_text[1] == "양지":
            plant_info_text[1] = "양지 (75~100)"
        elif plant_info_text[1] == "반양지":
            plant_info_text[1] = "반양지 (50~75)"
        elif plant_info_text[1] == "반음지":
            plant_info_text[1] = "반음지 (25~50)"
        elif plant_info_text[1] == "음지":
            plant_info_text[1] = "음지 (0~25)"

        temperature = plant_info2_text[3]
        temperature = temperature.split("℃")[0]
        humidity = plant_info_text[2]
        light = plant_info_text[1]
        watercycle = plant_info_text[0]
        water_detail = plant_info2_text[0]


        print("식물 이름 : ", plants_name,) 
        print("적정 온도 : ", temperature,"℃")
        print("습도 : ", humidity)
        print("광선량 : ", light)
        print("물주기 : ", watercycle)
        print("물주는 방법 : ", water_detail)
        # DB 생성 또는 연결
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        # 식물 정보 저장 테이블 생성
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users_plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                temperature TEXT,
                humidity TEXT,
                light TEXT,
                watercycle TEXT,
                water_detail TEXT
            )
        ''')
        cur.execute("INSERT INTO users_plants (name, temperature, humidity, light, watercycle, water_detail) VALUES (?, ?, ?, ?, ?, ?)",
                    (plants_name, temperature + "℃", humidity, light, watercycle, water_detail))
        con.commit()
    con.close