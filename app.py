from flask import Flask,render_template,request,redirect,jsonify,url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import sqlite3
from datetime import date,datetime,timedelta
from weather import get_tmp_hum_lux
from plant_crawling import get_plant_info


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///calendar.db'
#app.config['SQLALCHEMY_DATABASE_URI_2']='sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI_3']='sqlite:///sensor_data.db'
app.config['SQLALCHEMY_BINDS'] = {
    'database1': 'sqlite:///calendar.db',  
    'database2': 'sqlite:///database.db',
    'database3': 'sqlite:///sensor_data.db'    
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key = '1q2w3e4r'
db=SQLAlchemy(app)
#app.app_context().push()

#식물 입력 모델
class Todo(db.Model):
    __bind_key__ = 'database1'
    title = db.Column(db.String(200), unique=True, primary_key=True,nullable=False)
    start = db.Column(db.String(300))
    water = db.Column(db.String(300))
    species = db.Column(db.String(300))
    ill = db.Column(db.String(300))
    hum = db.Column(db.String(300))
    tem = db.Column(db.String(300))
    period = db.Column(db.String(300))

    def __repr__(self) -> str:
        return f"{self.title}-{self.species}-{self.start}-{self.water}-{self.ill}-{self.hum}-{self.tem}-{self.period}"

class User(db.Model):
    __tablename__ = 'users_plants'
    __bind_key__ = 'database2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    temperature = db.Column(db.Text)
    humidity = db.Column(db.Text)
    light = db.Column(db.Text)
    watercycle = db.Column(db.Text)
    water_detail = db.Column(db.Text)
    
class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    __bind_key__ = 'database3'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    brightness = db.Column(db.Integer)


#db에 이미 있으면 생기는 오류 처리
@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    return jsonify({'error': str(e)}), 400
 # 500 오류에 대한 핸들러
@app.errorhandler(500) 
def internal_server_error(error):
    return render_template('add_deny.html', error=error), 500




#캘린더에서 이름 클릭 시 날씨로 이동
@app.route('/weather')
def weather():
    ptitle = request.args.get('title')
    
    plant = Todo.query.get(ptitle)
    sensor_data = SensorData.query.first()
    temperature, humidity, lux = get_tmp_hum_lux(int(plant.period))
    convert_lux = 100 - lux *10
    weathers = {
        'ill': convert_lux, #햇빛 기준 lux -> micromol 
        'tem': temperature,
        'hum': humidity
    }

    
    adu_weather = {
        'ill': (sensor_data.brightness)*0.0135,# 형광등 기준 lux -> micromol 
        'hum': sensor_data.humidity,
        'tem': sensor_data.temperature
    }
    return render_template("weather.html", weather=weathers, plant=plant, adu=adu_weather)
'''
    if plant and plant.period is not None:
        temperature, humidity = get_tmp_hum(int(plant.period))
    else:
        temperature, humidity = 50, 50
'''
    

#캘린더
@app.route('/')
@app.route('/cal')
def cal():
    today = date.today()
    after = today + timedelta(days=7)
    after_str = after.strftime("%Y-%m-%d")
    
    todos = Todo.query.all()
    for todo in todos:
        for day in range(14):
            if todo.water == str(today + timedelta(days=day)):
                new_water = datetime.strptime(todo.water, "%Y-%m-%d") + timedelta(days=int(todo.period))
                new_water_str = new_water.strftime("%Y-%m-%d")
                
                # Check if title already contains a suffix
                if "_" in todo.title:
                    prefix, suffix = todo.title.rsplit("_", 1)
                    try:
                        suffix = int(suffix[:-2]) + 1  # Remove the "일차" suffix before converting to an integer
                    except ValueError:
                        suffix = 1
                else:
                    prefix = todo.title
                    suffix = 1

                new_title = f"{prefix}_{suffix}회차"
                new_todo = Todo(
                    title=new_title,
                    species=todo.species,
                    start=todo.water,
                    water=new_water_str,
                    ill=todo.ill,
                    hum=todo.hum,
                    tem=todo.tem,
                    period=todo.period
                )        
                
                try:
                    db.session.add(new_todo)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()

    events = Todo.query.all()
    return render_template("cal.html", events=events)

#식물 추가
@app.route('/set',methods=['GET','POST'])
def set():
    if request.method=='POST':
        
        species = request.form['species']
        session['species'] = species
        return redirect(url_for('add'))
    return render_template('set.html')

@app.route('/add', methods=['GET','POST'])
def add():
    
    species=session.get('species',None)
    
    get_plant_info(species)
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users_plants WHERE name=?", (species,))
    plants_data = cur.fetchone()
    if plants_data[2] is not None:
        weatherd = {
            'ill': plants_data[4].replace(" ",""),
            'tem': plants_data[2].replace(" ",""),
            'hum': plants_data[3].replace(" ",""),
            'period':plants_data[5].replace(" ","")
        }
    else:
        weatherd = {
            'ill': "입력바랍니다",
            'tem': "입력바랍니다",
            'hum': "입력바랍니다",
            'period':"입력바랍니다"
        }
    
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        period= request.form['period']
        ill = request.form['ill']
        hum = request.form['hum']
        tem = request.form['tem']
        instart = start[8:10]
        water_day=int(instart)+int(period)
        if(start[5:7]=="02"):
            if(water_day>28):
                water=start[0:5]+"03"+"-"+str(water-28)
            else:
                water=start[0:8]+str(water_day)
        elif(int(start[5:7])%2==0):
            if(water_day>30):
                water=start[0:5]+str(int(start[5:7])+1)+"-"+str(water_day-30)
            else:
                water=start[0:8]+str(water_day)
        else :
            if(water_day>31):
                water=start[0:5]+str(int(start[5:7])+1)+"-"+str(water_day-31)
            else:
                water=start[0:8]+str(water_day)
        water_datetime=datetime.strptime(water, "%Y-%m-%d")
        water=str(water_datetime)[0:10]


        todo = Todo(title=title, species=species, start=start,water=water, ill=ill,hum=hum,tem=tem, period=period)        
        try:
            db.session.add(todo)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return render_template("add_deny.html")
            
    alltodo = Todo.query.all()
    return render_template("add.html",alltodo=alltodo,species=species,wea=weatherd)
    
#식물 삭제
@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        title = request.form['title']

        # Find all data with titles starting with the specified title
        todos = Todo.query.filter(or_(Todo.title == title, Todo.title.like(f"{title}_%"))).all()

        # Delete all matching data
        for todo in todos:
            db.session.delete(todo)

        db.session.commit()

    alltodo = Todo.query.all()
    return render_template("delete.html", alltodo=alltodo)

if __name__ == "__main__":
    
    app.run(debug=True,port=5000,use_reloader=True)