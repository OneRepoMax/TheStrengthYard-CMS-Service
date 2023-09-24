from app import app, db
from flask import jsonify, request
from app.user import User
from datetime import datetime, timedelta
import requests, json
from os import environ

client_id = environ.get('PAYPAL_CLIENT_ID')
client_secret = environ.get('PAYPAL_CLIENT_SECRET')

def get_access_token():
    auth_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'  # Use the sandbox URL for testing
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    data = {
        'grant_type': 'client_credentials'
    }
    auth = (client_id, client_secret)

    response = requests.post(auth_url, headers=headers, data=data, auth=auth)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        access_token = response_data['access_token']
        return access_token
    else:
        raise Exception('Failed to obtain access token')