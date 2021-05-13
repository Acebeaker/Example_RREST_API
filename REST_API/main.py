from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Declartion for database models for students, classes and grades 
# (used as a link between the previous two)

class StudentModel(db.Model):
    __tablename__ = 'students'
    studentID = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    grades = db.relationship('GradesModel', backref='studentmodel', lazy=True)

    def __repr__(self):
    	return f"{studentID}: {last_name} {first_name}"
 
class ClassesModel(db.Model):
    __tablename__ = 'classes'
    code = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    grades = db.relationship('GradesModel', backref='classesmodel', lazy=True)

    def __repr__(self):
        return f"{name}: {description}"
    
class GradesModel(db.Model):
    __tablename__ = 'grades'
    gradeID = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.studentID'), nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.code'), nullable = False)

    def __repr__(self):
        return f"..."

#db.create_all()

# Fields declarations for marshal decorator
 
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

grades_fields = {
	'gradeID': fields.Integer,
	'student_id': fields.Integer,
	'class_id': fields.Integer
}

# Students Classes with REST Methods
class StudentLastName(Resource):
    @marshal_with(student_fields)
    def get(self,last_name):
        result = StudentModel.query.filter(StudentModel.last_name.startswith(last_name)).all()
        if not result:
            abort(404, message="No students were found")
        return result
    
class StudentFirstName(Resource):
    @marshal_with(student_fields)
    def get(self,first_name):
        result = StudentModel.query.filter(StudentModel.first_name.startswith(first_name)).all()
        if not result:
            abort(404, message="No students were found")
        return result

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

# Class Classes with REST Methods

class ClasseTitle(Resource):
    @marshal_with(classes_fields)
    def get(self,title):
        result = ClassesModel.query.filter(ClassesModel.title.startswith(title)).all()
        if not result:
            abort(404, message="No class were found")
        return result
    
class ClasseDescription(Resource):
    @marshal_with(classes_fields)
    def get(self,description):
        result = ClassesModel.query.filter(ClassesModel.description.startswith(description)).all()
        if not result:
            abort(404, message="No class were found")
        return result

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
    
#Grades Classes with REST Methods

class GradesClasses(Resource):
    @marshal_with(student_fields) 
    def get(self, code):
        #results = GradesModel.query.filter(GradesModel.class_id == code).all()
        results = StudentModel.query.filter(StudentModel.grades.any(GradesModel.class_id == code)).all()
        if not results:
            abort(404, message="Class not found")
        return results
      
class GradesStudents(Resource):
    @marshal_with(classes_fields) 
    def get(self, studentID):
        #results = GradesModel.query.filter(GradesModel.class_id == code).all()
        results = ClassesModel.query.filter(ClassesModel.grades.any(GradesModel.student_id == studentID)).all()
        if not results:
            abort(404, message="Class not found")
        return results
 
class Grades(Resource):
    @marshal_with(grades_fields)
    def get(self):
        result = GradesModel.query.all()
        if not result:
            abort(404, message="No assignments were found")
        return result
    
    @marshal_with(grades_fields)
    def post(self):
        parser = reqparse.RequestParser()  
        parser.add_argument('student_id', type = str, required=True)
        parser.add_argument('class_id', type = str, required=True)
        args = parser.parse_args()  #parse arguments

        studentResult = StudentModel.query.filter_by(studentID=args['student_id']).first()
        if not studentResult:
            abort(404, message="The student you are looking for does not exist")
            
        classResult = ClassesModel.query.filter_by(code=args['class_id']).first()
        if not classResult:
            abort(404, message="The class you are looking for does not exist")
        
        grades = GradesModel(student_id=args['student_id'], class_id=args['class_id'])
        db.session.add(grades)
        db.session.commit()
        return grades, 201

#ENDPOINTS Declaration

api.add_resource(Students, '/students')  # Students Endpoint - Methods (GET (all), POST)
api.add_resource(Student, '/students/<int:studentID>') # Students Endpoint - Methods (GET (single by ID), PUT, DELETE)
api.add_resource(StudentLastName, '/students/lastname/<string:last_name>') # Students Endpoint - Methods (GET (looking for each LASTNAME starting with it))
api.add_resource(StudentFirstName, '/students/firstname/<string:first_name>') # Students Endpoint - Methods (GET (looking for each FIRSTNAME starting with it))

api.add_resource(Classes, '/classes') # Classes Endpoint - Methods (GET (all), POST)
api.add_resource(Classe, '/classes/<int:code>') # Classes Endpoint - Methods (GET (single by ID), PUT, DELETE)
api.add_resource(ClasseTitle, '/classes/title/<string:title>') # Classes Endpoint - Methods (GET (looking for each TITLE starting with it))
api.add_resource(ClasseDescription, '/classes/description/<string:description>') # Classes Endpoint - Methods (GET (looking for each DESCRIPTION starting with it))

api.add_resource(Grades, '/grades') # Grades Endpoint - Methods (GET (all), POST)
api.add_resource(GradesClasses, '/grades/classes/<int:code>') # Students of a Class Endpoint - Methods (GET (single by Class' Code))
api.add_resource(GradesStudents, '/grades/students/<int:studentID>') # Classes of a Student Endpoint - Methods (GET (single by Student's ID))

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app