from flask import Flask,render_template,request,redirect,jsonify,url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import sqlite3
from datetime import date,datetime,timedelta
from weather import get_tmp_hum
from plant_crawling import get_plant_info


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///calendar.db'
app.config['SQLALCHEMY_DATABASE_URI_2']='sqlite:///database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'database1': 'sqlite:///calendar.db',  
    'database2': 'sqlite:///database.db'  
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

    def _repr_(self) -> str:
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
    

#db에 이미 있으면 생기는 오류 처리
@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    return jsonify({'error': str(e)}), 400

#홈
@app.route('/')
def home():
    
    return render_template("home.html")
#캘린더에서 이름 클릭 시 날씨로 이동
@app.route('/weather')
def weather():
    ptitle = request.args.get('title')
    plant = Todo.query.get(ptitle)
    #날씨 데이터 예시
    weather = {
        'ill': "80",
        'tem': '',
        'hum': ''
    }
    # get_tmp_hum 안에 식물 주기를 입력하면 지금까지의 평균 온도습도 뽑아냄
    temperature, humidity = get_tmp_hum(int(plant.period))
    weather['tem'] = temperature
    weather['hum'] = humidity

    #아두이노 예시
    adu_weather = {
    'ill' : "40",
    'hum' : "30",
    'tem' : "40"
}
    return render_template("weather.html",weather=weather,plant=plant,adu=adu_weather)

#캘린더
@app.route('/cal')
def cal():
    today = date.today()
    after = today + timedelta(days=7)
    after_str = after.strftime("%Y-%m-%d")
    
    number=Todo.query.count()
    for n in range(number):
        todos = Todo.query.all()
        for todo in todos:
            for day in range(7):
                if(todo.water==str(today + timedelta(days=day))) :
                    #for todo in todos:
                    #    if(todo.water<after_str):
                    new_water = datetime.strptime(todo.water, "%Y-%m-%d")+timedelta(days=int(todo.period))
                    new_water_str = new_water.strftime("%Y-%m-%d")
                    new_todo = Todo(title=todo.title+"_", species=todo.species, start=todo.water,water=new_water_str, ill=todo.ill,hum=todo.hum,tem=todo.tem, period=todo.period)        
                    try:
                        db.session.add(new_todo)
                        db.session.commit()
                    except IntegrityError as e:
                        db.session.rollback()
    events=Todo.query.all()
    return render_template("cal.html",events=events)

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
    new_plant=User.query.filter_by(name=species).first()
    if new_plant is not None:
        weatherd = {
            'ill': new_plant.light,
            'tem': new_plant.temperature,
            'hum': new_plant.humidity,
            'period':new_plant.watercycle
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
        #water = request.form['water']
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
@app.route('/delete', methods=['GET','POST'])
def delete_user():
    if request.method == "POST":
        title = request.form['title']
        user = Todo.query.get(title)
        if user:
            db.session.delete(user)
            db.session.commit()
        elif(title=="0"):
            db.session.query(Todo).delete()
            db.session.commit()
        else:
            return "User not found.",render_template("home.html")
    alltodo = Todo.query.all()
    return render_template("delete.html",alltodo=alltodo)



if __name__ == "__main__":
    
    app.run(debug=True,port=5000,use_reloader=True)