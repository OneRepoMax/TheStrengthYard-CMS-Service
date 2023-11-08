from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask import request, jsonify
import jwt

from app import app


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False

## Token based authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authHeader = request.headers.get('Authorization').split(" ")
        token = authHeader[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def admin_protected(f):
    @wraps(f)
    def admindecorated(*args, **kwargs):
        authHeader = request.headers.get('Authorization').split(" ")
        token = authHeader[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = data['email']
            userType = data['userType']
            if userType != "A":
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return admindecorated

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': 'This is a protected route', 'email': current_user}), 200

@app.route('/adminprotected', methods=['GET'])
@admin_protected
def adminprotected(current_user):
    return jsonify({'message': 'This is a admin protected route', 'email': current_user}), 200