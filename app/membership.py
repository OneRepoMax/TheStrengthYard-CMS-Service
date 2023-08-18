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

# Function and Route for getting All Memberships in the DB
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

# Function and Route for getting a Membership by ID
@app.route("/memberships/<int:id>")
def getMembershipByID(id: int):
    membershipList = Memberships.query.filter_by(MembershipTypeId=id).all()
    if len(membershipList):
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": [membership.json() for membership in membershipList]
            }
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no such membership with ID: " + str(id),
            "data": []
        }
    ), 406

# Function and Route to Create a new Membership
@app.route("/memberships", methods=['POST'])
def createMembership():
    """
    Sample Request
    {
        "Type": "Monthly",
        "BaseFee": 100,
        "Description": "Monthly Training Membership"
    }
    """
    data = request.get_json()
    try:
        membershipExists = Memberships.query.filter_by(Description=data["Description"]).first()
        if membershipExists:
            return jsonify(
                {
                    "code": 409,
                    "error": True,
                    "message": "Membership with Description: (" + data["Description"] + ") already exists."
                }
            ), 409
        membership = Memberships(**data)
        db.session.add(membership)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": membership.json()
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while creating the new Membership. " + str(e),
                "data": data
            }
        ), 406

# Function and Route to Update a Membership by ID
@app.route("/memberships/<int:id>", methods=['PUT'])
def updateMembership(id: int):
    """
    Sample Request
    {
        "Type": "Yearly",
        "BaseFee": 1200,
        "Description": "New 2024 Open Gym Membership"
    }
    """
    data = request.get_json()
    try:
        membership = Memberships.query.filter_by(MembershipTypeId=id).first()
        if membership:
            for key, value in data.items():
                setattr(membership, key, value)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "error": False,
                    "data": membership.json()
                }
            ), 200
        return jsonify(
            {
                "code": 406,
                "error": False,
                "message": "There are no such membership with ID: " + str(id),
                "data": []
            }
        ), 406
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while updating the Membership. " + str(e),
                "data": data
            }
        ), 406

#Function and Route to Delete a User by ID
@app.route("/memberships/<int:id>", methods=['DELETE'])
def deleteMembership(id: int):
    try:
        membership = Memberships.query.filter_by(MembershipTypeId=id).first()
        if membership:
            db.session.delete(membership)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "error": False,
                    "message": "Membership with ID: " + str(id) + " has been deleted."
                }
            ), 200
        return jsonify(
            {
                "code": 406,
                "error": False,
                "message": "There are no such membership with ID: " + str(id)
            }
        ), 406
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while deleting the Membership. " + str(e)
            }
        ), 406
