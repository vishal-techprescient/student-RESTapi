from flask import Flask, request
from flask_restx import Resource, Api, abort, fields, marshal_with
from model import db,StudentModel

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db.init_app(app)

#db.create_all()

model = api.model('Student Record', 
				  {'name': fields.String(required = True, 
    					  				 description="Name of the person", 
    					  				 help="Name cannot be blank.")},
                  {'mail': fields.String(required = True, 
    					  				 description="Mail Id of the person", 
    					  				 help="Mail Id cannot be blank.")}
                )

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'mail' : fields.String,
}
ns = api.namespace('students', description='Operations related to student record')

@ns.route('')
class Students_List(Resource):
    
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    def get(self):
        student_data = StudentModel.query.all()
        students = {}
        for student in student_data:
            students[student.id] = {"name": student.name, "mail": student.mail}
        return students 

@ns.route('/<int:stud_id>')
class Student(Resource):

    @marshal_with(resource_fields)
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
                params={ 'stud_id': 'Specify the Id associated with the Student' })
    def get(self, stud_id):
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if not stud:
            abort(404, message="No student found with this id")
        return stud

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'stud_id': 'Specify the Id associated with the Student' })
    @api.expect(model)
    @marshal_with(resource_fields)
    def post(self, stud_id):
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if stud:
            abort(409, "Student ID already exist")
        stud = StudentModel(id=stud_id, name=request.json['name'], mail=request.json['mail'])
        db.session.add(stud)
        db.session.commit()
        return stud, 201

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'stud_id': 'Specify the Id associated with the Student' })
    @api.expect(model)
    @marshal_with(resource_fields)
    def put(self, stud_id):
        stud = StudentModel.query.filter_by(id=stud_id).first()
        if not stud:
            abort(404, message="Student doesn't exist")
        if request.json['name']:
            stud.name = request.json['name']
        if request.json['mail']:
            stud.mail = request.json['mail']
        db.session.commit()
        return stud

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'stud_id': 'Specify the Id associated with the Student' })
    def delete(self, stud_id):
        StudentModel.query.filter_by(id=stud_id).delete()
        db.session.commit()
        return 'Student Deleted', 204


if __name__=='__main__':
    app.run(debug=True)