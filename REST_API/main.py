from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StudentModel(db.Model):
    __tablename__ = 'students'
    studentID = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
    	return f"{studentID}: {last_name} {first_name}"
 


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app