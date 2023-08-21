from app import app, db
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'

    UserId = db.Column(db.Integer, primary_key=True)
    EmailAddress = db.Column(db.String)
    FirstName = db.Column(db.String)
    LastName = db.Column(db.String)
    Gender = db.Column(db.String)
    DateOfBirth = db.Column(db.Date)
    HomeAddress = db.Column(db.String)
    PostalCode = db.Column(db.Integer)
    ContactNo = db.Column(db.String)
    Password = db.Column(db.String)
    UserType = db.Column(db.String)
    AccountCreationDate = db.Column(db.Date)
    DisplayPicture = db.Column(db.String)
    Verified = db.Column(db.String)

    def json(self):
        return {
            "UserId": self.UserId,
            "EmailAddress": self.EmailAddress,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Gender": self.Gender,
            "DateOfBirth": self.DateOfBirth,
            "HomeAddress": self.HomeAddress,
            "PostalCode": self.PostalCode,
            "ContactNo": self.ContactNo,
            "Password": self.Password,
            "UserType": self.UserType,
            "AccountCreationDate": self.AccountCreationDate,
            "DisplayPicture": self.DisplayPicture,
            "Verified": self.Verified
        }

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
        return jsonify(user.json()), 200
    else:
        return "Invalid user credentials", 401

# Function and Route for getting All Users in the DB
@app.route("/user")
def getAllUser():
    userList = User.query.all()
    
    return jsonify([user.json() for user in userList],200)
    

# Function and Route for getting a User by ID
@app.route("/user/<int:id>")
def getUserByID(id: int):
    userList = User.query.filter_by(UserId=id).all()
    if len(userList):
        return jsonify(
            [user.json() for user in userList]
        ), 200
    return "There are no such user with ID: " + str(id), 406

# Function and Route to Create a new User
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
        hashed_password = generate_password_hash(data.get("Password"), method='pbkdf2:sha256', salt_length=8)
        data["Password"] = hashed_password

        user = User(**data)

        db.session.add(user)
        db.session.commit()
        return jsonify(user.json()), 200
    except Exception as e:
        db.session.rollback()
        return "An error occurred while creating the new User. " + str(e), 406
    
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
    try:
        user = User.query.filter_by(UserId=UserId).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return jsonify(user.json()), 200
        return jsonify(
            {
                "code": 404,
                "error": True,
                "message": "User not found",
                "data": {}
            }
        ), 404
    except Exception as e:
        db.session.rollback()
        return "An error occurred while updating the User. " + str(e), 406
    
#Function and Route to Delete a User by ID
@app.route("/user/<int:id>", methods=['DELETE'])
def deleteUser(id: int):
    try:
        user = User.query.filter_by(UserId=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User Deleted Successfully of ID: " + str(id) + ".", 200
        return "User not found", 404
    except Exception as e:
        db.session.rollback()
        return "An error occurred while deleting the User. " + str(e), 406
