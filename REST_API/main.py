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
 
class ClassesModel(db.Model):
    __tablename__ = 'classes'
    code = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{name}: {description}"

#db.create_all()

 
student_fields = {
	'studentID': fields.Integer,
	'last_name': fields.String,
	'first_name': fields.String
}

classes_fields = {
	'code': fields.Integer,
	'title': fields.String,
	'description': fields.String
}


class Student(Resource):
    @marshal_with(student_fields)
    def get(self,studentID):
        result = StudentModel.query.filter_by(studentID=studentID).first()
        if not result:
            abort(404, message="No students were found")
        return result
    
    

    @marshal_with(student_fields)
    def put(self, studentID):
        parser = reqparse.RequestParser()  
        parser.add_argument('last_name', type = str )
        parser.add_argument('first_name', type = str )
        args = parser.parse_args()  #parse arguments
        print(args)
        result = StudentModel.query.filter_by(studentID=studentID).first()
        if not result:
            abort(404, message="Student doesn't exist, cannot update")

        if args['last_name']:
            result.last_name = args['last_name']
        if args['first_name']:
            result.first_name = args['first_name']

        db.session.commit()

        return result
    
    @marshal_with(student_fields)
    def delete(self,studentID):
        result = StudentModel.query.filter_by(studentID=studentID).first()
        if not result:
            abort(404, message="Student doesn't exist, cannot delete")
        
        db.session.delete(result)
        db.session.commit()
        return {}, 204
        
class Students(Resource):
    @marshal_with(student_fields)
    def get(self):
        result = StudentModel.query.all()
        if not result:
            abort(404, message="No students were found")
        return result
    
    @marshal_with(student_fields)
    def post(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('last_name', type = str, required=True)
        parser.add_argument('first_name', type = str, required=True)
        args = parser.parse_args()  #parse arguments
            
        student = StudentModel(last_name=args['last_name'], first_name=args['first_name'])
        db.session.add(student)
        db.session.commit()
        return student, 201

class Classe(Resource):
    @marshal_with(classes_fields)
    def get(self,code):
        result = ClassesModel.query.filter_by(code=code).first()
        if not result:
            abort(404, message="No class were found")
        return result
    
    
    @marshal_with(classes_fields)
    def put(self, code):
        parser = reqparse.RequestParser()  
        parser.add_argument('title', type = str )
        parser.add_argument('description', type = str )
        args = parser.parse_args()  #parse arguments
        print(args)
        
        result = ClassesModel.query.filter_by(code=code).first()
        if not result:
            abort(404, message="Class doesn't exist, cannot update")

        if args['title']:
            result.title = args['title']
        if args['description']:
            result.description = args['description']

        db.session.commit()
        return result
    
    @marshal_with(classes_fields)
    def delete(self,code):
        result = ClassesModel.query.filter_by(code=code).first()
        if not result:
            abort(404, message="Class doesn't exist, cannot delete")
        
        db.session.delete(result)
        db.session.commit()
        return {}, 204

class Classes(Resource):
    @marshal_with(classes_fields)
    def get(self):
        result = ClassesModel.query.all()
        if not result:
            abort(404, message="No classes were found")
        return result
    
    @marshal_with(classes_fields)
    def post(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('title', type = str, required=True)
        parser.add_argument('description', type = str, required=True)
        args = parser.parse_args()  #parse arguments

        classs = ClassesModel(title=args['title'], description=args['description'])
        db.session.add(classs)
        db.session.commit()
        return classs, 201

api.add_resource(Students, '/students')    # add endpoints
api.add_resource(Student, '/students/<int:studentID>')
api.add_resource(Classes, '/classes')
api.add_resource(Classe, '/classes/<int:code>')

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app