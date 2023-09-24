from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
import requests, json
from os import environ
from app.auth import get_access_token
from app.models import Memberships, MembershipRecord, MembershipLog, User

client_id = environ.get('PAYPAL_CLIENT_ID')
client_secret = environ.get('PAYPAL_CLIENT_SECRET')

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

# Function and Route to get all Memberships that are 'Public' under Visibility attribute (For Users to see)
@app.route("/memberships/public")
def getAllPublicMemberships():
    membershipList = Memberships.query.filter_by(Visibility="Public").all()
    if len(membershipList):
        return jsonify(
                [membership.json() for membership in membershipList]
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no public memberships.",
            "data": []
        }
    ), 406

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

# Function and Route to Create a new Membership (With PayPal Integration)
@app.route("/memberships", methods=['POST'])
def createMembership():
    """
    Sample Request
    {
        "Type": "Monthly",
        "Visibility": "Public",
        "BaseFee": 100,
        "Description": "Monthly Training Membership",
        "Title": "Monthly Training",
        "Picture": "https://example.com/picture.jpg",
        "SetupFee": 70
    }
    """
    data = request.get_json()

    # Use the access token to make the API call
    access_token = get_access_token()

    # Check that data["Type"] is not One-Time:
    if data["Type"] != "One-Time":

        # Create headers for request to PayPal API to create a new Product
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Prefer': 'return=representation',
        }

        # Create the request body to send to PayPal API to create a new Product
        paypalproductdata = '{"name": "' + data["Title"] + '","description": "' + data["Description"] + '","type": "SERVICE","category": "EXERCISE_AND_FITNESS","image_url": "' + data["Picture"] + '","home_url": "' + data["Picture"] + '"}'
    
        productresponse = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, data=paypalproductdata)

        # Create request body to send to PayPal API to create a new Plan
        # NEED TO EDIT TO CHANGE OTHER VARIABLES OF THE PLAN E.G. CYCLE, SETUP FEE, ETC.
        if data["Type"] == "Monthly":
            paypalplandata = '{"product_id": "' + productresponse.json()["id"] + '","name": "' + data["Title"] + ' (Monthly Plan)","description": "' + data["Description"] + '","billing_cycles": [{"frequency": {"interval_unit": "MONTH","interval_count": 1},"tenure_type": "REGULAR","sequence": 1,"total_cycles": 0,"pricing_scheme": {"fixed_price": {"value": ' + str(data["BaseFee"]) + ',"currency_code": "SGD"}}}],"payment_preferences": {"auto_bill_outstanding": true,"setup_fee": {"value": ' + str(data["SetupFee"]) + ',"currency_code": "SGD"},"setup_fee_failure_action": "CONTINUE","payment_failure_threshold": 1}}'
        elif data["Type"] == "Yearly":
            paypalplandata = '{"product_id": "' + productresponse.json()["id"] + '","name": "' + data["Title"] + ' (Yearly Plan)","description": "' + data["Description"] + '","billing_cycles": [{"frequency": {"interval_unit": "YEAR","interval_count": 1},"tenure_type": "REGULAR","sequence": 1,"total_cycles": 0,"pricing_scheme": {"fixed_price": {"value": ' + str(data["BaseFee"]) + ',"currency_code": "SGD"}}}],"payment_preferences": {"auto_bill_outstanding": true,"setup_fee": {"value": ' + str(data["SetupFee"]) + ',"currency_code": "SGD"},"setup_fee_failure_action": "CONTINUE","payment_failure_threshold": 1}}'

        planresponse = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers, data=paypalplandata)

        # If the both responses are successful, print the response then create the new Membership in the DB
        if productresponse.status_code == 201 and planresponse.status_code == 201:
            print(productresponse.json())
            print(planresponse.json())
            try:
                # Create a new Membership together with the PayPal Plan ID
                membership = Memberships(**data, PayPalPlanId=planresponse.json()["id"])
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
        else:
            return jsonify(
                {
                    "code": 407,
                    "error": True,
                    "message": "An error occurred while creating the new Membership in PayPal. " + str(productresponse.json()) + str(planresponse.json()),
                }
            ), 407
    # Else if data["Type"] is One-Time, since it is not a recurring purchase, we create a simple checkout in PayPal instead
    else:
        # Create headers for request to PayPal API to create a new checkout Order
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Prefer": "return=representation",
        }

        # Create request body to send to PayPal API to create a new Order
        paypalorderdata = '{"intent": "CAPTURE", "purchase_units": [{"items": [{"name": "' + data["Title"] + '", "description": "' + data["Description"] + '", "quantity": "1","unit_amount": {"currency_code": "SGD","value": "' + str(data["BaseFee"]) + '"}}],"amount": {"currency_code": "SGD","value": "' + str(data["BaseFee"]) + '","breakdown": {"item_total": {"currency_code": "SGD","value": "' + str(data["BaseFee"]) + '"}}}}],"application_context": {"return_url": "https://example.com/return","cancel_url": "https://example.com/cancel"}}'

        orderresponse = requests.post(
            "https://api-m.sandbox.paypal.com/v2/checkout/orders",
            headers=headers,
            data=paypalorderdata,
        )

        print(orderresponse.json())
        # If the both responses are successful, print the response then create the new Membership in the DB
        if orderresponse.status_code == 201:
            try:
                # Create a new Membership together with the PayPal Plan ID
                membership = Memberships(**data, PayPalPlanId=orderresponse.json()["id"])
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
        else:
            return jsonify(
                {
                    "code": 407,
                    "error": True,
                    "message": "An error occurred while creating the new Membership in PayPal. " + str(orderresponse.json()),
                }
            ), 407
    

# Function and Route to Get all Memberships (Products) in PayPal
@app.route("/memberships/paypal")
def getAllMembershipsPayPal():
    # Use the access token to make the API call
    access_token = get_access_token()

    # Create headers for request to PayPal API to get all Products
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # params
    params = {
        'page_size': 20,
        'page': 1,
        'total_required': 'true'
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, params=params)

    # If the response is successful, return the response
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(
            {
                "code": 407,
                "error": True,
                "message": "An error occurred while retrieving the Memberships from PayPal. " + str(response.json()),
            }
        ), 407
    
# Function and Route to list all Plans (Memberships) in PayPal
@app.route("/memberships/paypal/plans")
def getAllPlansPayPal():
    # Use the access token to make the API call
    access_token = get_access_token()

    # Create headers for request to PayPal API to get all Plans
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Prefer': 'return=representation',
    }

    # params
    params = {
        'sort_order': 'DESC',
        'sort_by': 'create_time',
        'page_size': 20,
        'page': 1,
        'total_required': 'true'
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers, params=params)

    # If the response is successful, return the response
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(
            {
                "code": 407,
                "error": True,
                "message": "An error occurred while retrieving the Plans from PayPal. " + str(response.json()),
            }
        ), 407

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
        print(membership.json())
        if membership:
            
            if membership.Type != "One-Time":
                # Use the access token to make the API call
                access_token = get_access_token()

                # Create headers for request to PayPal API to deactivate a Plan
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }

                print(membership.PayPalPlanId)
                response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans/' + membership.PayPalPlanId + '/deactivate', headers=headers)

                # If the response is successful, print the response
                if response.status_code == 204:
                    # Print a Message to say that PayPal plan has been deactivated
                    print("PayPal Plan with ID " + membership.PayPalPlanId + " has been deactivated.")
                else:
                    return jsonify(
                        {
                            "code": 407,
                            "error": True,
                            "message": "An error occurred while deactivating the Membership (Plan) in PayPal. " + str(response.json()),
                        }
                    ), 407
            
            db.session.delete(membership)
            db.session.commit()
            return jsonify(
                    "Membership with ID: " + str(id) + " has been deleted. Plan has been deactivated in PayPal."
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
                [membershipRecord.jsonWithUserAndMembership() for membershipRecord in membershipRecordList]
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
                    [membershipRecord.jsonWithMembership() for membershipRecord in membershipRecordList]
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existings memberships with User ID: " + str(id),
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
                membershipRecord.jsonWithUserAndMembership()
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
        "PayPalSubscriptionId": "I-1234567890",
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

        # Create a membership log with "Created" status
        membershipLog = MembershipLog(
            Date=membershipRecord.StartDate,
            Description="Membership record created on " + str(membershipRecord.StartDate) + ".",
            ActionType="Created",
            MembershipRecordId=membershipRecord.MembershipRecordId
        )
        db.session.add(membershipLog)
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
        "EndDate": "2023-12-31",
        "ActiveStatus": "Active",
        "StatusRemarks": null
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
        # Check if the Membership Record exists first
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=id).first()
        
        if membershipRecord:
            # Use the access token to make the API call
            access_token = get_access_token()

            # Create headers for request to PayPal API to cancel a Subscription
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }

            # If the Membership Record has a PayPal Subscription ID, then cancel the Subscription in PayPal
            if membershipRecord.PayPalSubscriptionId:
                # Include data in the request body to state reason for cancellation
                data = '{"reason": "User has terminated their membership on ' + str(datetime.now()) + '"}'

                # Make the API call to cancel the Subscription
                response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/' + membershipRecord.PayPalSubscriptionId + '/cancel', headers=headers, data=data)

                # If the response is successful, print the response
                if response.status_code == 204:
                    # Print a Message to say that PayPal Subscription has been cancelled
                    print("PayPal Subscription with ID " + membershipRecord.PayPalSubscriptionId + " has been cancelled.")
                else:
                    return jsonify(
                        {
                            "code": 407,
                            "error": True,
                            "message": "An error occurred while cancelling the Membership (Subscription) in PayPal. " + str(response.json()),
                        }
                    ), 407
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
                    "message": "Membership Record with ID: " + str(data["MembershipRecordId"]) + " does not exist."
                }
            ), 406
        # Check for Action Type. If it is "Pause", pull the latest Membership Log and check if it is a "Pause" Log. If it is, then return an error and rollback, specifying the reason that the Membership Record already has an existing Pause Log.
        if data["ActionType"] == "Pause":
            LatestMembershipLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"]).order_by(MembershipLog.MembershipLogId.desc()).first()

            if LatestMembershipLog.ActionType == "Pause":
                return jsonify(
                    {
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Pause Log."
                    }
                ), 409
            # If there is no existing "Pause" Membership Log, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to Paused
            SelectedMembershipRecord.ActiveStatus = 'Paused'

            # Check the MembershipRecord if the PayPalSubscriptionId is not null, if it is not null, then pause the Subscription in PayPal
            if SelectedMembershipRecord.PayPalSubscriptionId:
                # Use the access token to make the API call
                access_token = get_access_token()

                # Create headers for request to PayPal API to suspend a Subscription
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }

                # Include data in the request body to state reason for suspension
                reasondata = '{"reason": "User has paused their membership on ' + str(datetime.now()) + '"}'

                # Make the API call to suspend the Subscription
                response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/' + SelectedMembershipRecord.PayPalSubscriptionId + '/suspend', headers=headers, data=reasondata)

                # If the response is successful, print the response
                if response.status_code == 204:
                    # Print a Message to say that PayPal Subscription has been suspended
                    print("PayPal Subscription with ID " + SelectedMembershipRecord.PayPalSubscriptionId + " has been suspended.")
                else:
                    return jsonify(
                        {
                            "code": 407,
                            "error": True,
                            "message": "An error occurred while suspending the Membership (Subscription) in PayPal. " + str(response.json()),
                        }
                    ), 407
            db.session.commit()
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)
            db.session.add(membershipLog)
            db.session.commit()
            return jsonify(
                    membershipLog.json()
            ), 200
        # Check for Action Type. If it is "Resume", pull the latest Membership Log and check if it is a "Resume" Log. If it is, then return an error and rollback, specifying the reason that the Membership Record already has an existing Resume Log.
        elif data["ActionType"] == "Resume":
            LatestMembershipLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"]).order_by(MembershipLog.MembershipLogId.desc()).first()

            if LatestMembershipLog.ActionType == "Resume":
                return jsonify(
                    {
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Resume Log."
                    }
                ), 409
            # If there is no existing "Resume" Membership Log, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to 'Active'. Once done, use the given Date and check for the previous log's Pause Date. If the given Date is after the Pause Date, then compute the difference and update the MembershipRecord's EndDate accordingly. If the given Date is before the Pause Date, then return an error.
            SelectedMembershipRecord.ActiveStatus = 'Active'

            # Check the MembershipRecord if the PayPalSubscriptionId is not null, if it is not null, then resume the Subscription in PayPal
            if SelectedMembershipRecord.PayPalSubscriptionId:
                # Use the access token to make the API call
                access_token = get_access_token()

                # Create headers for request to PayPal API to reactivate a Subscription
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }

                # Include data in the request body to state reason for reactivation
                reasondata = '{"reason": "User has resumed their membership on ' + str(datetime.now()) + '"}'

                # Make the API call to reactivate the Subscription
                response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/' + SelectedMembershipRecord.PayPalSubscriptionId + '/activate', headers=headers, data=reasondata)

                # If the response is successful, print the response
                if response.status_code == 204:
                    # Print a Message to say that PayPal Subscription has been reactivated
                    print("PayPal Subscription with ID " + SelectedMembershipRecord.PayPalSubscriptionId + " has been reactivated.")
                else:
                    return jsonify(
                        {
                            "code": 407,
                            "error": True,
                            "message": "An error occurred while reactivating the Membership (Subscription) in PayPal. " + str(response.json()),
                        }
                    ), 407
            db.session.commit()
            # Get the latest Pause Log
            PreviousPauseLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Pause").order_by(MembershipLog.MembershipLogId.desc()).first()
            #  If there is no previous Pause Log, return an error and rollback, specifying the reason that there was no previous Pause Log to compute the difference in dates from.
            if not PreviousPauseLog:
                db.session.rollback()
                return jsonify(
                    {
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
                        "message": "The given Date is before the Pause Date."
                    }
                ), 412
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)

            # Add to the existing MembershipLog's description to include the number of additional days that we extended the Membership for (and how we computed it in brackets e.g. Paused Date - End Date in dd/mm/yyyy), as well as the new Membership End Date.
            membershipLog.Description = membershipLog.Description + "\nExtended the Membership by " + str(difference.days) + " days to " + str(SelectedMembershipRecord.EndDate) + "." + "(Paused Date: " + str(PreviousPauseLog.Date) + ", Resumed Date: " + date_string + ")"

            db.session.add(membershipLog)
            db.session.commit()
            return jsonify(membershipLog.json()), 200
        # Check for Action Type. If it is "Terminate", then check if there is an existing "Terminate" Membership Log. If not, then using the SelectedMembershipRecord, update it and change the ActiveStatus column to Terminated. Once done, use the given Date and replace the SelectedMembershipRecord's EndDate with the given Date to show that Membership has been terminated.
        elif data["ActionType"] == "Terminate":
            ExistingTerminateLog = MembershipLog.query.filter_by(MembershipRecordId=data["MembershipRecordId"], ActionType="Terminate").first()
            if ExistingTerminateLog:
                return jsonify(
                    {
                        "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " already has an existing Terminate Log."
                    }
                ), 409
            SelectedMembershipRecord.ActiveStatus = 'Terminated'
            SelectedMembershipRecord.EndDate = data["Date"]
            # Check if the MembershipRecord if the PayPalSubscriptionId is not null, if it is not null, then cancel the Subscription in PayPal
            if SelectedMembershipRecord.PayPalSubscriptionId:
                # Use the access token to make the API call
                access_token = get_access_token()

                # Create headers for request to PayPal API to cancel a Subscription
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }

                # Include data in the request body to state reason for cancellation
                reasondata = '{"reason": "User has terminated their membership on ' + data["Date"] + '"}'

                # Make the API call to cancel the Subscription
                response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/' + SelectedMembershipRecord.PayPalSubscriptionId + '/cancel', headers=headers, data=reasondata)

                # If the response is successful, print the response
                if response.status_code == 204:
                    # Print a Message to say that PayPal Subscription has been cancelled
                    print("PayPal Subscription with ID " + SelectedMembershipRecord.PayPalSubscriptionId + " has been cancelled.")
                else:
                    return jsonify(
                        {
                            "code": 407,
                            "error": True,
                            "message": "An error occurred while cancelling the Membership (Subscription) in PayPal. " + str(response.json()),
                        }
                    ), 407
            db.session.commit()
            # Create the new Membership Log and add into the DB
            membershipLog = MembershipLog(**data)
            db.session.add(membershipLog)
            db.session.commit()
            return jsonify({
                "message": "Membership with ID: " + str(data["MembershipRecordId"]) + " has been terminated.",
                "log": membershipLog.json()
            }), 200
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
            [membershipLog.jsonWithMembershipRecord() for membershipLog in membershipLogList]
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

# Function and Route to get Membership Records based on the Active Status filter
@app.route("/membershiprecord/filter", methods=['POST'])
def getMembershipRecordsByFilter():
    """
    SAMPLE REQUEST for "Active" Status
    {
        "ActiveStatus": "Active"
    }
    SAMPLE REQUEST for "Pending Payment" Status
    {
        "ActiveStatus": "Pending Payment"
    }
    SAMPLE REQUEST for "Paused" Status
    {
        "ActiveStatus": "Paused"
    }
    SAMPLE REQUEST for "Expired" Status
    {
        "ActiveStatus": "Expired"
    }
    SAMPLE REQUEST for "Terminated" Status
    {
        "ActiveStatus": "Terminated"
    }
    """
    data = request.get_json()
    membershipRecordList = MembershipRecord.query.filter_by(ActiveStatus=data["ActiveStatus"]).all()
    if len(membershipRecordList):
        return jsonify(
            [membershipRecord.jsonWithUserAndMembership() for membershipRecord in membershipRecordList]
        ), 200
    return jsonify(
        {
            "message": "There are no existing memberships with Active Status: " + data["ActiveStatus"],
        }
    ), 406

# Function and Route to get all Membership Logs across all Membership Records from the User Id
@app.route("/membershiplog/user/<int:id>")
def getMembershipLogsByUserID(id: int):
    # Get all Membership Records of the given User Id
    membershipRecordList = MembershipRecord.query.filter_by(UserId=id).all()
    print(membershipRecordList)
    # Create a new master list to store all of the Membership Records and their related Membership Logs
    MasterMembershipRecordAndLogList = []
    if len(membershipRecordList):
        # Loop through each Membership Record that the user has and pull out all of the related Membership Logs to this Membership Record
        for membershipRecord in membershipRecordList:
            # Create a temporary empty list to store all of the Membership Logs of this Membership Record
            tempMembershipLogList = []
            # Get all of the Membership Logs of that specific Membership Record
            membershipLogList = MembershipLog.query.filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).all()
            # Loop through each Membership Log and append it to the tempMembershipLogList
            for membershipLog in membershipLogList:
                tempMembershipLogList.append(membershipLog.json())
            # Append the Membership Record and its related Membership Logs to the membershipRecordAndLogList
            MasterMembershipRecordAndLogList.append(
                {
                    "MembershipRecord": membershipRecord.jsonWithMembership(),
                    "MembershipLog": tempMembershipLogList
                }
            )
        # Return the MasterMembershipRecordAndLogList and their related Membership Logs
        return jsonify(
            MasterMembershipRecordAndLogList
        ), 200
    return jsonify(
        {
            "code": 406,
            "error": False,
            "message": "There are no existing membership logs with User ID: " + str(id),
            "data": []
        }
    ), 406
        
            

            
            





