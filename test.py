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
#app.config['SQLALCHEMY_DATABASE_URI_1']='sqlite:///calendar.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)




pap=users_plants.query.get["개운죽"]
print(pap.temperature)