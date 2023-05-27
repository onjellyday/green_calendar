import sqlite3

# DB 생성 또는 연결
con = sqlite3.connect('plants_table.db')
cur = con.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS users_plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        name TEXT,
        temperature TEXT,
        lowest_temp TEXT,
        humidity TEXT,
        light TEXT
    )
''')

# 사용자 입력 받기
users_plant = input('식물의 이름을 입력하세요: ')

# 식물 정보 조회
cur.execute("SELECT * FROM plants_table WHERE name=?", (users_plant,))
row = cur.fetchone()

if row:
    species, name, temperature, lowest_temp, humidity, light = row[1:]
    cur.execute("INSERT INTO users_plants (species, name, temperature, lowest_temp, humidity, light) VALUES (?, ?, ?, ?, ?, ?)",
                (species, name, temperature, lowest_temp, humidity, light))
else:
    print('일치하는 식물의 이름을 찾을 수 없습니다. 직접 입력해 주세요')
    species = input('식물의 종을 입력하세요: ')
    name = input('식물의 이름을 입력하세요: ')
    temperature = input('식물의 적정 온도를 입력하세요: ')
    lowest_temp = input('식물의 겨울철 최소 온도를 입력하세요: ')
    humidity = input('식물의 적정 습도를 입력하세요: ')
    light = input('식물의 적정 조도를 입력하세요: ')

    # 사용자 입력 정보 DB에 저장
    cur.execute("INSERT INTO users_plants (species, name, temperature, lowest_temp, humidity, light) VALUES (?, ?, ?, ?, ?, ?)",
                (species, name, temperature, lowest_temp, humidity, light))

con.commit()

# DB 연결 종료
cur.close()
con.close()

# 결과 출력
print('종:', species)
print('이름:', name)
print('온도:', temperature)
print('겨울철 최소 온도:', lowest_temp)
print('습도:', humidity)
print('조도:', light)

exit()
