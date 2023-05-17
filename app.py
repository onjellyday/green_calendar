from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import sqlite3


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

#입력 모델
class Todo(db.Model):
    title = db.Column(db.String(200), unique=True, primary_key=True,nullable=False)
    start = db.Column(db.String(300))
    water = db.Column(db.String(300))
    species = db.Column(db.String(300))
    ill = db.Column(db.String(300))
    hum = db.Column(db.String(300))
    tem = db.Column(db.String(300))

    def _repr_(self) -> str:
        return f"{self.title}-{self.species}-{self.start}-{self.water}-{self.ill}-{self.hum}-{self.tem}"

#db에 이미 있으면 생기는 오류 처리
@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    return jsonify({'error': str(e)}), 400

#
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/cal')
def cal():
    events=Todo.query.all()
    return render_template("cal.html",events=events)

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
        todo = Todo(title=title, species=species, start=start,water=water, ill=ill,hum=hum,tem=tem)
        try:
            db.session.add(todo)
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()
            return render_template("add_deny.html")
        
    alltodo = Todo.query.all()
    return render_template("add.html",alltodo=alltodo)
    

@app.route('/vacuum')
def vacuum_database():
    conn = sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("VACUUM")
    conn.commit()
    cursor.close()
    conn.close()

    db.session.execute(text('VACUUM'))
    db.session.commit()
    
    return 'Vacuum completed'

@app.route('/delete', methods=['GET','POST'])
def delete_user():
    if request.method == "POST":
        title = request.form['title']
        user = Todo.query.get(title)
        if user:
            db.session.delete(user)
            db.session.commit()
            
        else:
            return "User not found."
    alltodo = Todo.query.all()
    return render_template("delete.html",alltodo=alltodo)



if __name__ == "__main__":
    
    app.run(debug=True,port=5000,use_reloader=True)