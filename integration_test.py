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