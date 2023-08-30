from app import app, db
from flask import jsonify, request
from app.user import User
from datetime import datetime

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
    ActiveStatus = db.Column(db.String, default='Inactive')
    User = db.relationship('User', backref=db.backref('memberships', cascade='all, delete-orphan'))
    Membership = db.relationship('Memberships', backref=db.backref('memberships', cascade='all, delete-orphan'))

    def json(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "ActiveStatus": self.ActiveStatus
        }

    def jsonWithUserAndMembership(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "ActiveStatus": self.ActiveStatus,
            "User": self.User.json(),
            "Membership": self.Membership.json()
        }
    
class MembershipLog(db.Model):
    __tablename__ = 'MembershipLog'

    MembershipLogId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    ActionType = db.Column(db.String)
    Description = db.Column(db.String)
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))

    def json(self):
        return {
            "MembershipLogId": self.MembershipLogId,
            "Date": self.Date,
            "ActionType": self.ActionType,
            "Description": self.Description,
            "MembershipRecordId": self.MembershipRecordId
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
                [membership.json() for membership in membershipList]    
        ), 200
    return jsonify(
             "There are no Memberships."
    ), 200

# Function and Route for getting a Membership by ID
@app.route("/memberships/<int:id>")
def getMembershipByID(id: int):
    membershipList = Memberships.query.filter_by(MembershipTypeId=id).all()
    if len(membershipList):
        return jsonify(
                [membership.json() for membership in membershipList]
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no such membership with ID: " + str(id),
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
                membership.json()
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while creating the new Membership. " + str(e),
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
                    membership.json()
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

#Function and Route to Delete a Membership by ID
@app.route("/memberships/<int:id>", methods=['DELETE'])
def deleteMembership(id: int):
    try:
        membership = Memberships.query.filter_by(MembershipTypeId=id).first()
        if membership:
            db.session.delete(membership)
            db.session.commit()
            return jsonify(
                    "Membership with ID: " + str(id) + " has been deleted."
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
                [membershipRecord.json() for membershipRecord in membershipRecordList]
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
                    [membershipRecord.json() for membershipRecord in membershipRecordList]
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
                [membershipRecord.json() for membershipRecord in membershipRecordList]
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existing memberships with Membership Type ID: " + str(id),
            "data": []
        }
    ), 406

# Function and Route to get a specific Membership Record by MembershipRecordId
@app.route("/membershiprecord/record/<int:id>")
def getMembershipRecordByRecordID(id: int):
    membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=id).first()
    if membershipRecord:
        return jsonify(
                membershipRecord.json()
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no such membership record with ID: " + str(id),
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
            data
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
    
# Function and Route to Update a Membership Record by ID
@app.route("/membershiprecord/<int:id>", methods=['PUT'])
def updateMembershipRecord(id: int):
    """
    Sample Request
    {
        "MembershipRecordId": 1,
        "StartDate": "2021-01-01",
        "EndDate": "2023-12-31"
    }
    """
    data = request.get_json()
    try:
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=id).first()
        if membershipRecord:
            for key, value in data.items():
                setattr(membershipRecord, key, value)
            db.session.commit()
            return jsonify(
                    membershipRecord.json()
            ), 200
        return jsonify(
            {
                "code": 406,
                "error": False,
                "message": "There are no such membership record with ID: " + str(id),
                "data": []
            }
        ), 406
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while updating the Membership Record. " + str(e),
                "data": data
            }
        ), 406
    
# Function and Route to Delete a Membership Record by ID
@app.route("/membershiprecord/<int:id>", methods=['DELETE'])
def deleteMembershipRecord(id: int):
    try:
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=id).first()
        if membershipRecord:
            db.session.delete(membershipRecord)
            db.session.commit()
            return jsonify(
                    "Membership Record with ID: " + str(id) + " has been deleted."
            ), 200
        return jsonify(
            {
                "code": 406,
                "error": False,
                "message": "There are no such membership record with ID: " + str(id)
            }
        ), 406
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while deleting the Membership Record. " + str(e)
            }
        ), 406
    
# Function and Route to create a new Membership Log
@app.route("/membershiplog", methods=['POST'])
def createMembershipLog():
    """
    Sample PAUSE Request
    {
        "Date": "2023-01-01",
        "ActionType": "Pause",
        "Description": "Paused Membership as User is going overseas for 3 months.",
        "MembershipRecordId": 1
    }
    Sample RESUME Request
    {
        "Date": "2023-05-01",
        "ActionType": "Resume",
        "Description": "Resumed Membership as User has returned from overseas trip.",
        "MembershipRecordId": 1
    }
    Sample TERMINATE Request
    {
        "Date": "2023-06-01",
        "ActionType": "Terminate",
        "Description": "Terminated Membership as User has left the gym.",
        "MembershipRecordId": 1
    }
    """
    data = request.get_json()
    try:
        # Check if the MembershipRecordId exists first
        SelectedMembershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=data["MembershipRecordId"]).first()
        if not SelectedMembershipRecord:
            return jsonify(
                {
                    "code": 406,
                    "error": True,
                    "message": "Membership Record with ID: " + str(data["MembershipRecordId"]) + " does not exist."
                }
            ), 406
        # Check for Action Type. If it is "Pause", then check if there is an existing "Pause" Membership Log
        if data["ActionType"] == "Pause":
            ExistingPauseLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Pause").first()
            if ExistingPauseLog:
                return jsonify(
                    {
                        "code": 409,
                        "error": True,
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Pause Log."
                    }
                ), 409
            # If there is no existing "Pause" Membership Log, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to Paused
            SelectedMembershipRecord.ActiveStatus = 'Paused'
            db.session.commit()
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)
            db.session.add(membershipLog)
            db.session.commit()
            return jsonify(
                    "Membership with ID: " + str(data["MembershipRecordId"]) + " has been paused."
            ), 200
        # Check for Action Type. If it is "Resume", then check if there is an existing "Resume" Membership Log
        elif data["ActionType"] == "Resume":
            ExistingResumeLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Resume").first()
            if ExistingResumeLog:
                return jsonify(
                    {
                        "code": 409,
                        "error": True,
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Resume Log."
                    }
                ), 409
            # If there is no existing "Resume" Membership Log, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to 'Active'. Once done, use the given Date and check for the previous log's Pause Date. If the given Date is after the Pause Date, then compute the difference and update the MembershipRecord's EndDate accordingly. If the given Date is before the Pause Date, then return an error.
            SelectedMembershipRecord.ActiveStatus = 'Active'
            db.session.commit()
            # Get the previous Pause Log
            PreviousPauseLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Pause").first()
            #  If there is no previous Pause Log, return an error and rollback, specifying the reason that there was no previous Pause Log to compute the difference in dates from.
            if not PreviousPauseLog:
                db.session.rollback()
                return jsonify(
                    {
                        "code": 411,
                        "error": True,
                        "message": "There is no previous Pause Log to compute the difference in dates from."
                    }
                ), 411
            # If there is a previous Pause Log, then check if the given Date is after the Pause Date. If it is, then compute the difference in dates and update the MembershipRecord's EndDate accordingly. If it is not, then return an error and rollback, specifying the reason that the given Date is before the Pause Date.
            
            date_string = data["Date"]
            date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
            
            if date_object > PreviousPauseLog.Date:
                difference = date_object - PreviousPauseLog.Date
                SelectedMembershipRecord.EndDate = SelectedMembershipRecord.EndDate + difference
                db.session.commit()
            else:
                db.session.rollback()
                return jsonify(
                    {
                        "code": 412,
                        "error": True,
                        "message": "The given Date is before the Pause Date."
                    }
                ), 412
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)
            db.session.add(membershipLog)
            db.session.commit()
            return jsonify(
                    "Membership with ID: " + str(data["MembershipRecordId"]) + " has been resumed."
            ), 200
        # Check for Action Type. If it is "Terminate", then check if there is an existing "Terminate" Membership Log. If not, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to Terminated. Once done, use the given Date and replace the SelectedMembershipRecord's EndDate with the given Date to show that Membership has been terminated.
        elif data["ActionType"] == "Terminate":
            ExistingTerminateLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Terminate").first()
            if ExistingTerminateLog:
                return jsonify(
                    {
                        "code": 409,
                        "error": True,
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Terminate Log."
                    }
                ), 409
            SelectedMembershipRecord.ActiveStatus = 'Terminated'
            SelectedMembershipRecord.EndDate = data["Date"]
            db.session.commit()
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)
            db.session.add(membershipLog)
            db.session.commit()
            return jsonify(
                "Membership with ID: " + str(data["MembershipRecordId"]) + " has been terminated."
            ), 200
        # If the Action Type is not "Pause", "Resume" or "Terminate", then return an error and rollback, specifying the reason that the Action Type is invalid.
        else:
            db.session.rollback()
            return jsonify(
                {
                    "code": 413,
                    "error": True,
                    "message": "Invalid Action Type."
                }
            ), 413
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 410,
                "error": True,
                "message": "An error occurred while creating the new Membership Log. " + str(e),
                "data": data
            }
        ), 410
    
# Function and Route to get all Membership Logs by Membership Record ID
@app.route("/membershiplog/<int:id>")
def getMembershipLogsByMembershipRecordID(id: int):
    membershipLogList = MembershipLog.query.filter_by(MembershipRecordId=id).all()
    if len(membershipLogList):
        return jsonify(
            [membershipLog.json() for membershipLog in membershipLogList]
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existing membership logs with Membership Record ID: " + str(id),
            "data": []
        }
    ), 406

# Function and Route to get a specific Membership Log by MembershipLogId
@app.route("/membershiplog/log/<int:id>")
def getMembershipLogByLogID(id: int):
    membershipLog = MembershipLog.query.filter_by(MembershipLogId=id).first()
    if membershipLog:
        return jsonify(
            membershipLog.json()
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no such membership log with ID: " + str(id),
            "data": []
        }
    ), 406

# Function and Route to Delete a specific Membership Log by MembershipLogId
@app.route("/membershiplog/<int:id>", methods=['DELETE'])
def deleteMembershipLog(id: int):
    try:
        membershipLog = MembershipLog.query.filter_by(MembershipLogId=id).first()
        if membershipLog:
            db.session.delete(membershipLog)
            db.session.commit()
            return jsonify(
                "Membership Log with ID: " + str(id) + " has been deleted."
            ), 200
        return jsonify(
            {
                "code": 406,
                "error": False,
                "message": "There are no such membership log with ID: " + str(id)
            }
        ), 406
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while deleting the Membership Log. " + str(e)
            }
        ), 406
        