from app import app, db
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.user import User
from app.passwordchecker import is_strong_password

class IndemnityForm(db.Model):
    __tablename__ = 'IndemnityForm'

    IndemnityFormId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'),primary_key=True)
    FeedbackDiscover = db.Column(db.String)
    MedicalHistory = db.Column(db.String)
    MedicalRemarks = db.Column(db.String)
    AcknowledgementTnC = db.Column(db.Boolean, default=True)
    AcknowledgementOpenGymRules = db.Column(db.Boolean, default=True)

    def json(self):
        return {
            "IndemnityFormId": self.IndemnityFormId,
            "UserId": self.UserId,
            "FeedbackDiscover": self.FeedbackDiscover,
            "MedicalHistory": self.MedicalHistory,
            "MedicalRemarks": self.MedicalRemarks,
            "AcknowledgementTnC": self.AcknowledgementTnC,
            "AcknowledgementOpenGymRules": self.AcknowledgementOpenGymRules
        }
    
# Function and Route to Register a new User with completed Indemnity Form
@app.route("/register", methods=['POST'])
def register():
    """
    Sample Request
    {
        "EmailAddress": "tanahkao@gmail.com",
        "FirstName": "Ah Kao",
        "LastName": "Tan",
        "Gender": "F",
        "DateOfBirth": "1945-01-01",
        "HomeAddress": "Geylang Lorong 23",
        "PostalCode": 670123,
        "ContactNo": "91234567",
        "Password": "iactuallylovecats",
        "UserType": "C",
        "DisplayPicture": "sample.jpg",
        "Verified": false,
        "FeedbackDiscover": "Search Engine, Friend's Recommendation, Walking Pass, Google Maps, Facebook Adverts, Google Adverts, Other",
        "MedicalHistory": "Heart Problems, Pain in Chest when exercising/not exercising, Low Blood Pressure/High Blood Pressure, Any breathing difficulties or asthma, Diabetes, Fainting spells, Joint problems, Epilepsy, Currently on medication, Significant illness/Operations, None, Other",
        "MedicalRemarks": "I had a heart operation back in 2008 and my knees are very weak. I am also on medication for my heart. I also have fainting spells once in a while.",
        "AcknowledgementTnC": true,
        "AcknowledgementOpenGymRules": true
    }
    """
    data = request.get_json()
    try:
        userExists = User.query.filter_by(
            EmailAddress=data["EmailAddress"]).first()
        if userExists:
            return jsonify(
                {
                    "code": 409,
                    "error": True,
                    "message": "An error occured while creating a new User. User with ID " + str(userExists.UserId) + " already exists. Check that email address is unique."
                }
            ), 409
        
        # Check if password is strong
        if not is_strong_password(data.get("Password")):
            return jsonify(
                {
                    "code": 400,
                    "error": True,
                    "message": "An error occured while creating a new User. Password is not strong enough or does not meet the requirements."
                }
            ), 400
        
        # Hash password
        hashed_password = generate_password_hash(data.get("Password"), method='pbkdf2:sha256', salt_length=8)
        data["Password"] = hashed_password

        # Create new User
        newUser = User()
        newUser.EmailAddress = data.get("EmailAddress")
        newUser.FirstName = data.get("FirstName")
        newUser.LastName = data.get("LastName")
        newUser.Gender = data.get("Gender")
        newUser.DateOfBirth = data.get("DateOfBirth")
        newUser.HomeAddress = data.get("HomeAddress")
        newUser.PostalCode = data.get("PostalCode")
        newUser.ContactNo = data.get("ContactNo")
        newUser.Password = data.get("Password")
        newUser.UserType = data.get("UserType")
        newUser.DisplayPicture = data.get("DisplayPicture")
        newUser.AccountCreationDate = datetime.now()
        newUser.Verified = data.get("Verified")

        # Add newUser into the database, return error if failed
        db.session.add(newUser)
        db.session.commit()

        # Create new Indemnity Form with the newly created UserId
        newIndemnityForm = IndemnityForm()
        newIndemnityForm.FeedbackDiscover = data.get("FeedbackDiscover")
        newIndemnityForm.MedicalHistory = data.get("MedicalHistory")
        newIndemnityForm.MedicalRemarks = data.get("MedicalRemarks")
        newIndemnityForm.AcknowledgementTnC = data.get("AcknowledgementTnC")
        newIndemnityForm.AcknowledgementOpenGymRules = data.get("AcknowledgementOpenGymRules")
        newIndemnityForm.UserId = newUser.UserId

        # Add newIndemnityForm into the database
        db.session.add(newIndemnityForm)
        db.session.commit()

        return jsonify(
            {
                "code": 201,
                "data": [
                    newUser.json()
                    ],
                "message": "User created successfully."
            }
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 406,
                "error": True,
                "message": "An error occurred while creating the new User. " + str(e)
            }
        ), 406

# Function and Route to get Indemnity Form details by UserId
@app.route("/indemnityform/<int:UserId>", methods=['GET'])
def getIndemnityForm(UserId: int):
    try:
        indemnityForm = IndemnityForm.query.filter_by(UserId=UserId).first()
        if indemnityForm:
            return jsonify(
                {
                    "code": 200,
                    "data": [
                        indemnityForm.json()
                        ]
                }
                ), 200
        return jsonify(
            {
                "code": 404,
                "error": True,
                "message": "Indemnity Form not found",
                "data": {}
            }
        ), 404
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "error": True,
                "message": "An error occurred while retrieving the Indemnity Form. " + str(e)
            }
        ), 404
