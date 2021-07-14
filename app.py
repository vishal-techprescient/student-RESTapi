from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from model import db,StudentModel

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db.init_app(app)

#db.create_all()

stud_post_args = reqparse.RequestParser()
stud_post_args.add_argument("name", type=str, help="Enter student name.", required=True)
stud_post_args.add_argument("mail", type=str, help="Enter student mail id.", required=True)

stud_put_args = reqparse.RequestParser()
stud_put_args.add_argument("name", type=str)
stud_put_args.add_argument("mail", type=str)

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'mail' : fields.String,
}

class Students_List(Resource):
    def get(self):
        student_data = StudentModel.query.all()
        students = {}
        for student in student_data:
            students[student.id] = {"name": student.name, "mail": student.mail}
        return students 

class Student(Resource):
    @marshal_with(resource_fields)
    def get(self, stud_id):
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if not stud:
            abort(404, message="No student found with this id")
        return stud

    @marshal_with(resource_fields)
    def post(slef, stud_id):
        args = stud_post_args.parse_args()
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if stud:
            abort(409, "Student ID already exist")

        stud = StudentModel(id=stud_id, name=args['name'], mail=args['mail'])
        db.session.add(stud)
        db.session.commit()
        return stud, 201

    @marshal_with(resource_fields)
    def put(self, stud_id):
        args = stud_put_args.parse_args()
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if not stud:
            abort(404, message="Student doesn't exist")
        if args['name']:
            stud.name = args['name']
        if args['mail']:
            stud.mail = args['mail']
        db.session.commit()
        return stud

    def delete(self, stud_id):
        StudentModel.query.filter_by(id=stud_id).delete()
        db.session.commit()
        return 'Student Deleted', 204

api.add_resource(Student, '/students/<int:stud_id>')
api.add_resource(Students_List, '/students')

if __name__=='__main__':
    app.run(debug=True)