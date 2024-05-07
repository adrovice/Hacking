from flask import Flask
#lib for db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://boarduser:morgen000@localhost/boarddb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = 'f1c50cdf58a5ac7024799454'
app.secret_key = "passwordmy"

db = SQLAlchemy(app)
from board import routes