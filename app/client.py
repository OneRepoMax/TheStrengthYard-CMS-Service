from app import app, db
from flask import jsonify


class Client(db.Model):
    __tablename__ = 'Client'

# TO DO
#     Staff_ID = db.Column(db.Integer, primary_key=True)
#     Staff_FName = db.Column(db.String)
#     Staff_LName = db.Column(db.String)
#     Dept = db.Column(db.String)
#     Email = db.Column(db.String)
#     Role_ID = db.Column(db.Integer, db.ForeignKey('Access_Role.Role_ID'))
#     LearningJourney = db.relationship('LearningJourney', backref='Staff')
#     Registrations = db.relationship('Registration', backref='Staff')

#     def json(self):
#         return {
#             "Staff_ID": self.Staff_ID,
#             "Staff_FName": self.Staff_FName,
#             "Staff_LName": self.Staff_LName,
#             "Dept": self.Dept,
#             "Email": self.Email,
#         }

#     def jsonWithAccessRole(self):
#         return {
#             "Staff_ID": self.Staff_ID,
#             "Staff_FName": self.Staff_FName,
#             "Staff_LName": self.Staff_LName,
#             "Dept": self.Dept,
#             "Email": self.Email,
#             "Access_Role": self.Access_Role.json()
#         }


# @app.route("/staff/test")
# def testStaff():
#     return "staff route is working"


# @app.route("/staff")
# def getStaff():
#     staffList = Staff.query.all()
#     if len(staffList):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [staff.jsonWithAccessRole() for staff in staffList],
#                 "error": False
#             }
#         )
#     return jsonify(
#         {
#             "code": 200,
#             "data": [],
#             "message": "There are no staff.",
#             "error": False
#         }
#     ), 200
