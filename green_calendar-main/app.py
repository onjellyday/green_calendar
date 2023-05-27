from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import sqlite3
from datetime import date,datetime,timedelta
from weather import get_tmp_hum
from plant_crawling import get_plant_info

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

#식물 입력 모델
class Todo(db.Model):
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
    temperature, humidity = get_tmp_hum(3)
    weather['tem'] = temperature
    weather['hum'] = humidity

    #아두이노 예시
    adu_weather = {
    'ill' : "10",
    'hum' : "30",
    'tem' : "20"
}
    return render_template("weather.html",weather=weather,plant=plant,adu=adu_weather)

#캘린더
@app.route('/cal')
def cal():
    today = date.today()
    after = today + timedelta(days=7)
    after_str = after.strftime("%Y-%m-%d %H:%M:%S")
    todos = Todo.query.all()
    
    for todo in todos:
        if(todo.start<after_str) :
            for todo in todos:
                if(todo.water<after_str):
                    new_water = datetime.strptime(todo.water, "%Y-%m-%d")+timedelta(days=int(todo.period))
                    new_water_str = new_water.strftime("%Y-%m-%d")
                    new_todo = Todo(title=todo.title+"o", species=todo.species, start=todo.water,water=new_water_str, ill=todo.ill,hum=todo.hum,tem=todo.tem, period=todo.period)        
                    try:
                        db.session.add(new_todo)
                        db.session.commit()
                    except IntegrityError as e:
                        db.session.rollback()
    events=Todo.query.all()
    return render_template("cal.html",events=events)

#식물 추가
@app.route('/add', methods=['GET',"POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        species = request.form['species']
        start = request.form['start']
        water = request.form['water']
        ill = request.form['ill']
        hum = request.form['hum']
        tem = request.form['tem']
        instart = start[8:10]
        inwater = water[8:10]
        if(inwater>instart) :
                period = int(inwater) - int(instart)
        else :
            if(start[5:7]=="02") :
                period =  28- int(instart) + int(inwater)
            elif(int(start[5:7])%2==0) :     
                period = 30 - int(instart) + int(inwater)
            else : 
                period = 31 - int(instart) + int(inwater)

        todo = Todo(title=title, species=species, start=start,water=water, ill=ill,hum=hum,tem=tem, period=period)        
        try:
            db.session.add(todo)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return render_template("add_deny.html")
            
    alltodo = Todo.query.all()
    return render_template("add.html",alltodo=alltodo)
    
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