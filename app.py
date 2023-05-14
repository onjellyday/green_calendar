from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    title = db.Column(db.String(200), unique=True, primary_key=True,nullable=False)
    start = db.Column(db.String(300))
    water = db.Column(db.String(300))
    ill = db.Column(db.String(300))
    hum = db.Column(db.String(300))
    tem = db.Column(db.String(300))

    def _repr_(self) -> str:
        return f"{self.title}-{self.start}-{self.water}-{self.ill}-{self.hum}-{self.tem}"

@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    return jsonify({'error': str(e)}), 400

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
        start = request.form['start']
        water = request.form['water']
        ill = request.form['ill']
        hum = request.form['hum']
        tem = request.form['tem']
        todo = Todo(title=title, start=start,water=water, ill=ill,hum=hum,tem=tem)
        try:
            db.session.add(todo)
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()
            return render_template("add_deny.html")
        
    alltodo = Todo.query.all()
    return render_template("add.html",alltodo=alltodo)
    

#@app.route('/vacuum')
#def vacuum_database():
#    db.session.execute(text('VACUUM'))
#    db.session.commit()
#    return 'Vacuum completed'

#@app.route('/delete_event/<string:title>', methods=['POST'])
#def delete_event(title):
#    event = Todo.query.get_or_404(title)
#    db.session.delete(event)
#    db.session.commit()
#    return redirect(url_for('add'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port=5000)