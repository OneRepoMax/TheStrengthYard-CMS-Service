import os
from app import app
from dotenv import load_dotenv
import pytest
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# class TestApp(flask_testing.TestCase):
    
#     DB_HOSTNAME = environ.get('DB_HOSTNAME')
#     DB_USERNAME = environ.get('DB_USERNAME')
#     DB_PASSWORD = environ.get('DB_PASSWORD')
#     DB_PORT = environ.get("DB_PORT")
#     DB_NAME = environ.get('DB_NAME')

#     app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOSTNAME + ":" + DB_PORT + "/" + DB_NAME + "_test"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['TESTING'] = True

#     def create_app(self):
#         return app

@pytest.fixture(autouse=True)
def initialise_db():
    db_host = os.environ.get("DB_HOSTNAME")
    db_port = os.environ.get("DB_PORT")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}_test"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global db
    db = SQLAlchemy(app)
    global sql_file
    sql_file = open('TSY_DB_TEST.sql', 'r')
    return db, sql_file


# Fixture to reset database before each test is run
@pytest.fixture(autouse=True)
def reset():
    # Before test commands
    print('\nResetting test database')
    sql_command = ''
    for line in sql_file:
        # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):
            # Append line to the command string
            sql_command += line.strip('\n')

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statement and commit it
                try:
                    db.session.execute(text(sql_command))
                    db.session.commit()
                # Assert in case of error
                except Exception as e:
                    print(e)

                # Finally, clear command string
                finally:
                    sql_command = ''
    # This is where the testing happens
    yield


## Test cases for user.py
def test_login():
    with app.test_client() as test_client:
        loginForm = {
            'EmailAddress': 'testuser@tsy.com',
            'Password': '12345678'
        }
        response = test_client.post("/login",
                                    content_type='application/json',
                                    data=json.dumps(loginForm))

        assert response.status_code == 200

def test_login_invalid():
    with app.test_client() as test_client:
        loginForm = {
            'EmailAddress': 'lousy@gmail.com',
            'Password': 'badpassword'
        }
        response = test_client.post("/login",
                                    content_type='application/json',
                                    data=json.dumps(loginForm))

        assert response.status_code == 401

def test_getAllUser():
    with app.test_client() as test_client:
        response = test_client.get("/user")

        assert response.status_code == 200
        all_users = response.get_json()
        assert len(all_users) > 0

def test_getUserByID():
    with app.test_client() as test_client:
        response = test_client.get("/user/1")

        assert response.status_code == 200
        user = response.get_json()
        assert len(user) > 0

def test_getUserByID_Not_Found():
    with app.test_client() as test_client:
        response = test_client.get("/user/9000")

        assert response.status_code == 406

def test_CreateUser():
    with app.test_client() as test_client:
        newUser = {
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
            "Verified": False
        }
        response = test_client.post("/user",
                                    content_type='application/json',
                                    data=json.dumps(newUser))

        assert response.status_code == 200

def test_CreateUser_User_Already_Exists():
    with app.test_client() as test_client:
        newUser = {
            "EmailAddress": "testuser@tsy.com",
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
            "Verified": False
        }
        response = test_client.post("/user",
                                    content_type='application/json',
                                    data=json.dumps(newUser))

        assert response.status_code == 409

def test_updateUser():
    with app.test_client() as test_client:
        updatedInfo = {
            "HomeAddress": "New Fake Address",
            "PostalCode": 654321,
            "ContactNo": "99991234"
        }
        response = test_client.put("/user/1",
                                    content_type='application/json',
                                    data=json.dumps(updatedInfo))

        assert response.status_code == 200

def test_updateUser_User_Does_Not_Exist():
    with app.test_client() as test_client:
        updatedInfo = {
            "HomeAddress": "New Fake Address",
            "PostalCode": 654321,
            "ContactNo": "99991234"
        }
        response = test_client.put("/user/9000",
                                    content_type='application/json',
                                    data=json.dumps(updatedInfo))

        assert response.status_code == 404

def test_deleteUser():
    with app.test_client() as test_client:
        response = test_client.delete("/user/1")

        assert response.status_code == 200

def test_deleteUser_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.delete("/user/9000")

        assert response.status_code == 404

## Test Cases for registration.py
def test_register():
    with app.test_client() as test_client:
        newUser = {
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
            "Verified": False,
            "FeedbackDiscover": "Search Engine, Friend's Recommendation, Walking Pass, Google Maps, Facebook Adverts, Google Adverts, Other",
            "MedicalHistory": "Heart Problems, Pain in Chest when exercising/not exercising, Low Blood Pressure/High Blood Pressure, Any breathing difficulties or asthma, Diabetes, Fainting spells, Joint problems, Epilepsy, Currently on medication, Significant illness/Operations, None, Other",
            "MedicalRemarks": "I had a heart operation back in 2008 and my knees are very weak. I am also on medication for my heart. I also have fainting spells once in a while.",
            "AcknowledgementTnC": True,
            "AcknowledgementOpenGymRules": True
        }
        response = test_client.post("/register",
                                    content_type='application/json',
                                    data=json.dumps(newUser))

        assert response.status_code == 200

def test_register_user_exists():
    with app.test_client() as test_client:
        newUser = {
            "EmailAddress": "admin@tsy.com",
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
            "Verified": False,
            "FeedbackDiscover": "Search Engine, Friend's Recommendation, Walking Pass, Google Maps, Facebook Adverts, Google Adverts, Other",
            "MedicalHistory": "Heart Problems, Pain in Chest when exercising/not exercising, Low Blood Pressure/High Blood Pressure, Any breathing difficulties or asthma, Diabetes, Fainting spells, Joint problems, Epilepsy, Currently on medication, Significant illness/Operations, None, Other",
            "MedicalRemarks": "I had a heart operation back in 2008 and my knees are very weak. I am also on medication for my heart. I also have fainting spells once in a while.",
            "AcknowledgementTnC": True,
            "AcknowledgementOpenGymRules": True
        }
        response = test_client.post("/register",
                                    content_type='application/json',
                                    data=json.dumps(newUser))

        assert response.status_code == 409

# def test_getIndemnityForm():
#     with app.test_client() as test_client:
#         response = test_client.get("/indemnityform/1")

#         assert response.status_code == 200

def test_getIndemnityForm_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/indemnityform/9000")

        assert response.status_code == 404

def test_resetPassword():
    with app.test_client() as test_client:
        User = {
            "EmailAddress": "admin@tsy.com"
        }
        response = test_client.post("/resetpassword",
                                    content_type='application/json',
                                    data=json.dumps(User))

        assert response.status_code == 200

def test_resetPassword_User_Does_Not_Exist():
    with app.test_client() as test_client:
        User = {
            "EmailAddress": "emailthatdont@exist.com"
        }
        response = test_client.post("/resetpassword",
                                    content_type='application/json',
                                    data=json.dumps(User))

        assert response.status_code == 404

## Test Cases for membership.py
def test_getAllMemberships():
    with app.test_client() as test_client:
        response = test_client.get("/memberships")

        assert response.status_code == 200
        all_memberships = response.get_json()
        assert len(all_memberships) > 0

def test_getMembershipByID():
    with app.test_client() as test_client:
        response = test_client.get("/memberships/1")

        assert response.status_code == 200

def test_getMembershipByID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/memberships/9000")

        assert response.status_code == 406

def test_createMembership():
    with app.test_client() as test_client:
        newMembership = {
            "Type": "Monthly",
            "BaseFee": 100,
            "Description": "New Monthly Training Membership",
            "Title": "New Title",
            "Picture": "picture.jpg"
        }
        response = test_client.post("/memberships",
                                    content_type='application/json',
                                    data=json.dumps(newMembership))

        assert response.status_code == 200

def test_updateMembership():
    with app.test_client() as test_client:
        updateMembership = {
            "Type": "Yearly",
            "BaseFee": 1200,
            "Description": "New 2024 Open Gym Membership"
        }
        response = test_client.put("/memberships/2",
                                    content_type='application/json',
                                    data=json.dumps(updateMembership))

        assert response.status_code == 200

def test_updateMembership_Membership_Does_Not_Exist():
    with app.test_client() as test_client:
        updateMembership = {
            "Type": "Yearly",
            "BaseFee": 1200,
            "Description": "New 2024 Open Gym Membership"
        }
        response = test_client.put("/memberships/9000",
                                    content_type='application/json',
                                    data=json.dumps(updateMembership))

        assert response.status_code == 406

def test_deleteMembership():
    with app.test_client() as test_client:
        response = test_client.delete("/memberships/8")
        ## Does not delete if there is a fk dependency
        assert response.status_code == 200

def test_deleteMembership_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.delete("/memberships/9000")

        assert response.status_code == 406

def test_getAllMembershipRecords():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord")

        assert response.status_code == 200
        all_memberships = response.get_json()
        assert len(all_memberships) > 0

def test_getMembershipRecordsByID():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/100")

        assert response.status_code == 200

def test_getMembershipByRecordsID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/9000")

        assert response.status_code == 406

def test_getMembershipRecordsByMembershipID():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/membership/1")

        assert response.status_code == 200

def test_getMembershipRecordsByMembershipID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/membership/9000")

        assert response.status_code == 406

def test_getMembershipRecordByRecordID():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/record/1")

        assert response.status_code == 200

def test_getMembershipRecordByRecordID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/membershiprecord/record/9000")

        assert response.status_code == 406

def test_createMembershipRecord():
    with app.test_client() as test_client:
        newMembershipRecord = {
            "UserId": 100,
            "MembershipTypeId": 4,
            "StartDate": "2023-01-01",
            "EndDate": "2023-12-31"
        }
        response = test_client.post("/membershiprecord",
                                    content_type='application/json',
                                    data=json.dumps(newMembershipRecord))

        assert response.status_code == 200

def test_createMembershipRecord_User_Does_Not_Exist():
    with app.test_client() as test_client:
        newMembershipRecord = {
            "UserId": 9000,
            "MembershipTypeId": 4,
            "StartDate": "2021-01-01",
            "EndDate": "2021-12-31"
        }
        response = test_client.post("/membershiprecord",
                                    content_type='application/json',
                                    data=json.dumps(newMembershipRecord))

        assert response.status_code == 406

def test_createMembershipRecord_Membership_Does_Not_Exist():
    with app.test_client() as test_client:
        newMembershipRecord = {
            "UserId": 100,
            "MembershipTypeId": 9000,
            "StartDate": "2021-01-01",
            "EndDate": "2021-12-31"
        }
        response = test_client.post("/membershiprecord",
                                    content_type='application/json',
                                    data=json.dumps(newMembershipRecord))

        assert response.status_code == 407

def test_createMembershipRecord_Membership_Already_Exists():
    with app.test_client() as test_client:
        newMembershipRecord = {
            "UserId": 100,
            "MembershipTypeId": 5,
            "StartDate": "2021-01-01",
            "EndDate": "2021-12-31"
        }
        response = test_client.post("/membershiprecord",
                                    content_type='application/json',
                                    data=json.dumps(newMembershipRecord))

        assert response.status_code == 408

## Still Broken
def test_updateMembershipRecord():
    with app.test_client() as test_client:
        updateMembershipRecord = {
            "MembershipRecordId": 1,
            "StartDate": "2021-01-01",
            "EndDate": "2023-12-31",
            "ActiveStatus": "Active",
            "StatusRemarks": None
            
        }
        response = test_client.put("/membershiprecord/1",
                                    content_type='application/json',
                                    data=json.dumps(updateMembershipRecord))

        assert response.get_json()['message'] == 200

def test_updateMembershipRecord_Does_Not_Exist():
    with app.test_client() as test_client:
        updateMembershipRecord = {
            "MembershipRecordId": 9000,
            "StartDate": "2021-01-01",
            "EndDate": "2023-12-31"
        }
        response = test_client.put("/membershiprecord/1",
                                    content_type='application/json',
                                    data=json.dumps(updateMembershipRecord))

        assert response.status_code == 406

# def test_deleteMembershipRecord():
#     with app.test_client() as test_client:
#         response = test_client.delete("/membershiprecord/2")
#         foreign key issue
#         assert response.status_code == 200

def test_deleteMembershipRecord_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.delete("/membershiprecord/9000")

        assert response.status_code == 406

## Still Broken
def test_createMembershipLog():
    with app.test_client() as test_client:
        newMembershipLog = {
            "Date": "2023-01-01",
            "ActionType": "Pause",
            "Description": "Paused Membership as User is going overseas for 3 months.",
            "MembershipRecordId": 1
        }
        response = test_client.post("/membershiplog",
                                    content_type='application/json',
                                    data=json.dumps(newMembershipLog))

        assert response.status_code == 200

def test_getMembershipLogsByMembershipRecordID():
    with app.test_client() as test_client:
        response = test_client.get("/membershiplog/1")

        assert response.status_code == 200

def test_getMembershipLogsByMembershipRecordID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/membershiplog/9000")

        assert response.status_code == 406

def test_getMembershipLogByLogID():
    with app.test_client() as test_client:
        response = test_client.get("/membershiplog/log/901")

        assert response.status_code == 200

def test_getMembershipLogByLogID_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.get("/membershiplog/log/9000")

        assert response.status_code == 406

def test_deleteMembershipLog():
    with app.test_client() as test_client:
        response = test_client.delete("/membershiplog/901")

        assert response.status_code == 200

def test_deleteMembershipLog_Does_Not_Exist():
    with app.test_client() as test_client:
        response = test_client.delete("/membershiplog/9000")

        assert response.status_code == 406