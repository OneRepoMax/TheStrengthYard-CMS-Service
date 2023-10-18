from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

user = environ.get('user') or "placeholderuser"
password = environ.get('password') or "placeholderpassword"

DB_HOSTNAME = environ.get('DB_HOSTNAME')
DB_USERNAME = environ.get('DB_USERNAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_PORT = environ.get("DB_PORT")
DB_NAME = environ.get('DB_NAME')

app = Flask(__name__)

@app.route("/")
def index():
    return "TSY-IABS Backend Service API has been succesfully connected!"

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOSTNAME + ":" + DB_PORT + "/" + DB_NAME
# print
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
db = SQLAlchemy(app)

app.config['MAIL_DEFAULT_SENDER'] = "noreply@flask.com"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = environ.get("EMAIL_PASSWORD")
mail = Mail(app)

app.config['SECURITY_PASSWORD_SALT'] = environ.get("SECURITY_PASSWORD_SALT", default="very-important")
app.config['SECRET_KEY'] = 'fdkjshfhjsdfdskfdsfdcbsjdkfdsdf'

from .user import User
from .membership import Memberships
from .registration import IndemnityForm
from .payments import Payment
from .booking import Booking
from .schedule import Schedule

