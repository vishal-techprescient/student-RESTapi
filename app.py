from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

students = {
    1: {"name" : "vishal", "mail":"vishal@gmail.com"},
    2: {"name" : "abhishek", "mail":"abhishek@gmail.com"},
    3: {"name" : "kiran", "mail":"kiran@gmail.com"},
}

stud_post_args = reqparse.RequestParser()
stud_post_args.add_argument("name", type=str, help="Enter student name.", required=True)
stud_post_args.add_argument("mail", type=str, help="Enter student mail id.", required=True)

stud_put_args = reqparse.RequestParser()
stud_put_args.add_argument("name", type=str)
stud_put_args.add_argument("mail", type=str)

class Students_List(Resource):
    def get(self):
        return students

class Student(Resource):
    def get(self, stud_id):
        return students[stud_id]

    def post(slef, stud_id):
        args = stud_post_args.parse_args()
        if stud_id in students:
            abort(409, "Student ID already exist")
        students[stud_id] = {"name":args["name"], "mail":args["mail"]}
        return students[stud_id]

    def put(self, stud_id):
        args = stud_put_args.parse_args()
        if stud_id not in students:
            abort(404, message="Student doesn't exist")
        if args['name']:
            students[stud_id]['name'] = args['name']
        if args['mail']:
            students[stud_id]['mail'] = args['mail']
        return students



    def delete(self, stud_id):
        del students[stud_id]
        return students

api.add_resource(Student, '/students/<int:stud_id>')
api.add_resource(Students_List, '/students')

if __name__=='__main__':
    app.run(debug=True)