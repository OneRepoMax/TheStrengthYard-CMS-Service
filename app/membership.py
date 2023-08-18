from app import app, db
from flask import jsonify, request

class Memberships(db.Model):
    __tablename__ = 'Memberships'

    MembershipTypeId = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String)
    BaseFee = db.Column(db.Float)
    Description = db.Column(db.String)

    def json(self):
        return {
            "MembershipTypeId": self.MembershipTypeId,
            "Type": self.Type,
            "BaseFee": self.BaseFee,
            "Description": self.Description
        }
    
@app.route("/memberships/test")
def testMembership():
    return "membership route is working"

# Function and Route for getting All Users in the DB
@app.route("/memberships")
def getAllMemberships():
    membershipList = Memberships.query.all()
    if len(membershipList):
        return jsonify(
            {
                "code": 200,
                "data": [membership.json() for membership in membershipList],
                "error": False
            }
        )
    return jsonify(
        {
            "code": 200,
            "data": [],
            "message": "There are no Memberships.",
            "error": False
        }
    ), 200

