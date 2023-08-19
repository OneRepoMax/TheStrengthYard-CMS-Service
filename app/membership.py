from app import app, db
from flask import jsonify, request
from app.user import User

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
    
    def jsonWithUser(self):
        return {
            "MembershipTypeId": self.MembershipTypeId,
            "Type": self.Type,
            "BaseFee": self.BaseFee,
            "Description": self.Description,
            "User": [user.json() for user in self.User]
        }
    
class MembershipRecord(db.Model):
    __tablename__ = 'MembershipRecord'

    MembershipRecordId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), primary_key=True)
    MembershipTypeId = db.Column(db.Integer, db.ForeignKey('Memberships.MembershipTypeId'), primary_key=True)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    User = db.relationship('User', backref=db.backref('memberships', cascade='all, delete-orphan'))
    Membership = db.relationship('Memberships', backref=db.backref('memberships', cascade='all, delete-orphan'))

    def json(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate
        }

    def jsonWithUserAndMembership(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "User": self.User.json(),
            "Membership": self.Membership.json()
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

#Function and Route to get the Membership for every User
@app.route("/membershiprecord")
def getAllMembershipRecords():
    membershipRecordList = MembershipRecord.query.all()
    if len(membershipRecordList):
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": [membershipRecord.jsonWithUserAndMembership() for membershipRecord in membershipRecordList]
            }
        ), 200
    return jsonify(
        {
            "code": 200,
            "error": False,
            "message": "There are no Memberships.",
            "data": []
        }
    ), 200

# Function and Route to get the all Membership Records by individual User ID
@app.route("/membershiprecord/<int:id>")
def getMembershipRecordsByID(id: int):
    membershipRecordList = MembershipRecord.query.filter_by(UserId=id).all()
    if len(membershipRecordList):
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": [membershipRecord.jsonWithUserAndMembership() for membershipRecord in membershipRecordList]
            }
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existings memberships with User ID: " + str(id),
            "data": []
        }
    ), 406

# Function and Route to get all Membership Records by Membership Type ID
@app.route("/membershiprecord/membership/<int:id>")
def getMembershipRecordsByMembershipID(id: int):
    membershipRecordList = MembershipRecord.query.filter_by(MembershipTypeId=id).all()
    if len(membershipRecordList):
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": [membershipRecord.jsonWithUserAndMembership() for membershipRecord in membershipRecordList]
            }
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existing memberships with Membership Type ID: " + str(id),
            "data": []
        }
    ), 406

#Function and Route to create a new Membership Record
@app.route("/membershiprecord", methods=['POST'])
def createMembershipRecord():
    """
    Sample Request
    {
        "UserId": 100,
        "MembershipTypeId": 4,
        "StartDate": "2021-01-01",
        "EndDate": "2021-12-31"
    }
    """
    data = request.get_json()
    try:
        # Get the selected User and check if they exist first
        SelectedUser = User.query.filter_by(UserId=data["UserId"]).first()
        if not SelectedUser:
            return jsonify(
                {
                    "code": 406,
                    "error": True,
                    "message": "User with ID: " + str(data["UserId"]) + " does not exist."
                }
            ), 406
        # Get the selected Membership and check if it exists first
        SelectedMembership = Memberships.query.filter_by(MembershipTypeId=data["MembershipTypeId"]).first()
        if not SelectedMembership:
            return jsonify(
                {
                    "code": 407,
                    "error": True,
                    "message": "Membership with ID: " + str(data["MembershipTypeId"]) + " does not exist."
                }
            ), 407
        # Check if the User already has an existing Membership
        ExistingMembership = MembershipRecord.query.filter_by(UserId=data["UserId"], MembershipTypeId=data["MembershipTypeId"]).first()
        if ExistingMembership:
            return jsonify(
                {
                    "code": 408,
                    "error": True,
                    "message": "User with ID: " + str(data["UserId"]) + " already has an existing Membership with ID: " + str(data["MembershipTypeId"])
                }
            ), 408
        # Create the new Membership Record and add into the DB
        membershipRecord = MembershipRecord(**data)
        db.session.add(membershipRecord)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "error": False,
                "data": data
            }
        ), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 410,
                "error": True,
                "message": "An error occurred while creating the new Membership Record. " + str(e),
                "data": data
            }
        ), 410