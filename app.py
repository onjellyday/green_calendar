from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///databse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    title = db.Column(db.String(200), primary_key=True)
    desc = db.Column(db.String(300), nullable=False)
    def _repr_(self) -> str:
        return f"{self.title}-{self.desc}"

@app.route('/')
def home():
    return render_template("cal.html")

@app.route('/cal')
def cal():
    return render_template("cal.html",events=events)

@app.route('/add', methods=['GET',"POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("add.html",alltodo=alltodo)

if __name__ == "__main__":
    app.run(debug=True,port=5000)