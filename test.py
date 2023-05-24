from datetime import date,datetime,timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Todo,db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# 현재 날짜 가져오기
today = date.today()
after = today + timedelta(days=7)
after_str = after.strftime("%Y-%m-%d %H:%M:%S")
todos = Todo.query.all()

for todo in todos:
    print(todo.period)
    if(todo.water<after_str):
        new_water = datetime.strptime(todo.water, "%Y-%m-%d")+timedelta(days=int(todo.period))
        new_water_str = new_water.strftime("%Y-%m-%d")
        new_todo = Todo(title=todo.title+"o", species=todo.species, start=todo.water,water=new_water_str, ill=todo.ill,hum=todo.hum,tem=todo.tem, period=todo.period)        
        try:
            db.session.add(new_todo)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            
            
        
        
#날짜 오래된 거 지울지 말지?    

alltodo = Todo.query.all()
for todos in alltodo :
    print(todos.title)


