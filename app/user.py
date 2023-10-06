from app import app, db
from flask import jsonify, request, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.token import confirm_token, generate_token
from app.email import send_email
from app.models import User, IndemnityForm, MembershipRecord, Payment, MembershipLog

@app.route("/user/test")
def testUser():
    return "user route is working"

# Function and Route for user login
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("EmailAddress")
    password = data.get("Password")

    if not email or not password:
        return "Invalid user credentials", 400

    user = User.query.filter_by(EmailAddress=email).first()

    if user and check_password_hash(user.Password, password):
        return jsonify(user.jsonMinInfo())
    else:
        return "Invalid user credentials", 401

# Function and Route for getting All Users in the DB
@app.route("/user")
def getAllUser():
    userList = User.query.all()
    
    return jsonify([user.json() for user in userList]), 200
    

# Function and Route for getting a User by ID
@app.route("/user/<int:id>")
def getUserByID(id: int):
    userList = User.query.filter_by(UserId=id).all()
    if len(userList):
        return jsonify(
            [user.json() for user in userList]
        ), 200
    return "There are no such user with ID: " + str(id), 406

# Function and Route to Create a new User (USE THIS FOR STAFF 1RATION that does not need indemnity form)
@app.route("/user", methods=['POST'])
def createUser():
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
        "AccountCreationDate": "2023-01-01",
        "Verified": false
    }
    """
    data = request.get_json()
    try:
        userExists = User.query.filter_by(
            EmailAddress=data["EmailAddress"]).first()
        if userExists:
            return "An error occured while creating new user: User already exists. Check by email address", 409
        
        # Hash password
        if data.get("Password") is not None:
            hashed_password = generate_password_hash(data.get("Password"), method='pbkdf2:sha256', salt_length=8)
            data["Password"] = hashed_password

        user = User(**data)

        db.session.add(user)
        db.session.commit()

        token = generate_token(user.EmailAddress)
        confirm_url = url_for("verifyEmail", token=token, _external=True)
        html = render_template("/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.EmailAddress, subject, html)

        return jsonify(user.json()), 200
    except Exception as e:
        db.session.rollback()
        return "An error occurred while creating the new User. " + str(e), 406

# Function that verifies the user when they click on the verification link
@app.route("/verify/<token>", methods=['GET'])
def verifyEmail(token):
    email = confirm_token(token)
    user = User.query.filter_by(EmailAddress=email).first()
    if user.EmailAddress == email:
        user.Verified = 1
        db.session.add(user)
        db.session.commit()
        return("You have confirmed your account. Thanks!")
    else:
        return("The confirmation link is invalid or has expired.")
    
    return redirect(url_for("core.home"))

# Function to Resend Verification Email after it expires
@app.route("/verify/resend", methods=['POST'])
def resendVerifyEmail():
    """
    Sample Request
    {
        "EmailAddress": "tsy.fyp.2023@gmail.com"
    }
    """
    data = request.get_json()

    try:
        user = User.query.filter_by(EmailAddress=data["EmailAddress"]).first()
        if user:
            token = generate_token(user.EmailAddress)
            confirm_url = url_for("verifyEmail", token=token, _external=True)
            html = render_template("/confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.EmailAddress, subject, html)
            
            return("Verification Email Successfully Sent"), 200
        
        return "User with email address " + data["EmailAddress"] + " not found.", 404
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "error": True,
                "message": "An error occurred while sending verification email. " + str(e)
            }
        ), 404
    
# Function and Route to Update a User by ID
@app.route("/user/<int:id>", methods=['PUT'])
def updateUser(id: int):
    """
    Sample Request
    {
        "HomeAddress": "New Fake Address",
        "PostalCode": 654321,
        "ContactNo": "99991234"
    }
    """
    UserId=id
    data = request.get_json()

    # Hash password
    if data.get("Password") is not None:
        hashed_password = generate_password_hash(data.get("Password"), method='pbkdf2:sha256', salt_length=8)
        data["Password"] = hashed_password


    try:
        user = User.query.filter_by(UserId=UserId).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return jsonify(user.json()), 200
        return "User not found", 404
    except Exception as e:
        db.session.rollback()
        return "An error occurred while updating the User. " + str(e), 406
    
#Function and Route to Delete a User by ID
@app.route("/user/<int:id>", methods=['DELETE'])
def deleteUser(id: int):
    try:
        user = User.query.filter_by(UserId=id).first()
        if user:
            # Check if user has any Indemnity Form, and if he/she has, delete it
            indemnityForm = IndemnityForm.query.filter_by(UserId=id).first()
            if indemnityForm:
                db.session.delete(indemnityForm)

            # Check if user has any Membership Record, and retrieve all of them
            membershipRecordList = MembershipRecord.query.filter_by(UserId=id).all()

            # For each membershipRecord, check if there are any Payments, MembershipLogs, and delete all of them
            for membershipRecord in membershipRecordList:
                # Delete all Payments tied to the Membership Record
                paymentList = Payment.query.filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).all()
                for payment in paymentList:
                    db.session.delete(payment)

                # Delete all Membership Logs tied to the Membership Record
                membershipLogList = MembershipLog.query.filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).all()
                for membershipLog in membershipLogList:
                    db.session.delete(membershipLog)
                
                # Delete the Membership Record
                db.session.delete(membershipRecord)
                
            # Delete the User
            db.session.delete(user)
            db.session.commit()
            return "User Deleted Successfully of ID: " + str(id) + ".", 200
        
        return "User not found", 404
    except Exception as e:
        db.session.rollback()
        return "An error occurred while deleting the User. " + str(e), 406
