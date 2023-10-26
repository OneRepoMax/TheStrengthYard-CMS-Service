from app import app, db
from flask import jsonify, request, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.passwordchecker import is_strong_password, generate_strong_password
from app.token import confirm_token, generate_token
from app.email import send_email
from app.user import verifyEmail
from app.models import User, IndemnityForm
from app.token import token_required

# Function and Route to Register a new User with completed Indemnity Form
@app.route("/register", methods=['POST'])
def register():
    """
    Sample Request
    {
        "EmailAddress": "tsy.fyp.2023@gmail.com",
        "FirstName": "OneRepo",
        "LastName": "Max",
        "Gender": "O",
        "DateOfBirth": "1945-01-01",
        "HomeAddress": "Geylang Lorong 23",
        "PostalCode": 670123,
        "ContactNo": "91234567",
        "Password": "TSY@FYPi2023",
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
                    "error": True,
                    "message": "An error occured while creating a new User. User with ID " + str(userExists.UserId) + " already exists. Check that email address is unique."
                }
            ), 409
        
        # Check if password is strong
        # if not is_strong_password(data.get("Password")):
        #     return jsonify(
        #         {
        #             "error": True,
        #             "message": "An error occured while creating a new User. Password is not strong enough or does not meet the requirements."
        #         }
        #     ), 400
        
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

        token = generate_token(newUser.EmailAddress)
        confirm_url = url_for("verifyEmail", token=token, _external=True)
        html = render_template("/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(newUser.EmailAddress, subject, html)

        return jsonify(
            newUser.json()       
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "error": True,
                "message": "An error occurred while creating the new User. " + str(e)
            }
        ), 406

# Function and Route to get Indemnity Form details by UserId
@app.route("/indemnityform/<int:UserId>", methods=['GET'])
@token_required
def getIndemnityForm(UserId: int):
    try:
        indemnityForm = IndemnityForm.query.filter_by(UserId=UserId).first()
        if indemnityForm:
            return jsonify(indemnityForm.json()), 200
        return jsonify(
            {
                "error": True,
                "message": "Indemnity Form not found",
            }
        ), 404
    except Exception as e:
        return jsonify(
            {
                "error": True,
                "message": "An error occurred while retrieving the Indemnity Form. " + str(e)
            }
        ), 404
    
# Function and Route to Reset Password by EmailAddress Part 1
@app.route("/resetpassword", methods=['POST'])
def resetPassword():
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
            
            # Generate random password
            newPassword = generate_strong_password()
            print("\nThe new password is: " + f"{newPassword}")

            # Hash password
            hashed_password = generate_password_hash(newPassword, method='pbkdf2:sha256', salt_length=8)
            user.Password = hashed_password
            
            # Commit hashed password to database
            db.session.commit()

            # Send email with new password and a link to reset password
            token = generate_token(user.EmailAddress)
            reset_url = url_for("resetPassword2", token=token, _external=True)
            html = render_template("/reset_password.html", reset_url=reset_url, newPassword=newPassword)
            subject = "Reset Your Password"
            send_email(user.EmailAddress, subject, html)
            
            return jsonify(user.jsonMinInfo()), 200
        
        return "User with email address " + data["EmailAddress"] + " not found.", 404
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "error": True,
                "message": "An error occurred while resetting the password. " + str(e)
            }
        ), 404
    
# Function and Route to Reset Password by EmailAddress Part 2
@app.route("/resetpassword/<token>", methods=['GET'])
def resetPassword2(token):
    email = confirm_token(token)
    user = User.query.filter_by(EmailAddress=email).first()
    if user.EmailAddress == email:
        # Route the User to the Reset Password Page
        return render_template("/reset_password.html")
    else:
        return("The confirmation link is invalid or has expired.")
    
    return redirect(url_for("core.home"))
