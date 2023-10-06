from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import json
from app.auth import get_access_token
from app.models import MembershipRecord, MembershipLog, Memberships, Payment, Points

# Function and Route to get all Payments
@app.route('/payments')
def getPayments():
    paymentList = Payment.query.all()
    if len(paymentList):
        return jsonify(
            [
                payment.json() for payment in paymentList
            ]
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments.",
            "error": True
        }
    ), 404

# Function and Route to get a Payment by PaymentId
@app.route('/payments/<int:PaymentId>')
def getPaymentById(PaymentId):
    payment = Payment.query.filter_by(PaymentId=PaymentId).first()
    if payment:
        return jsonify(payment.json()), 200
    return jsonify(
        {
            "code": 404,
            "message": "Payment with id {} was not found.".format(PaymentId),
            "error": True
        }
    ), 404

# Function and Route to get all Payments by MembershipRecordId
@app.route('/payments/membershiprecord/<int:MembershipRecordId>')
def getPaymentsByMembershipRecordId(MembershipRecordId):
    paymentList = Payment.query.filter_by(MembershipRecordId=MembershipRecordId).all()
    if len(paymentList):
        return jsonify(
            [
                payment.json() for payment in paymentList
            ]
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments for MembershipRecordId {}.".format(MembershipRecordId),
            "error": True
        }
    ), 404

# Function and Route to refresh the ActiveStatus of all Membership Records by checking the Payment Date and Membership Record End Date
@app.route("/membershiprecord/refresh")
def refreshMembershipRecords():
    # First, get a list of all Membership Records
    membershipRecordList = MembershipRecord.query.all()

    # Save the current date
    currentDate = datetime.now().date()

    # Using this membershipRecordList, for each Membership Record, check if the membership record has expired by using the current date and the Membership Record's End Date. 
    for membershipRecord in membershipRecordList:
        # IF Membership Record's End Date is more than 3 days before the current date, then first check the latest Payment made for this Membership Record. 
        # !!!(This is used when the user have not made payment even after the 3 days grace period)!!! 
        if membershipRecord.EndDate < currentDate - timedelta(days=3):
            latestPayment = Payment.query.filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).order_by(Payment.TransactionDate.desc()).first()
            # Change the MembershipRecord's ActiveStatus to "Expired" and StatusRemarks to "Payment Overdue - Membership Expired on dd/mm/yyyy" if the latest Payment's Transaction Date is more than 3 days before the Membership Record's End Date
            if latestPayment.TransactionDate < membershipRecord.EndDate - timedelta(days=3):
                membershipRecord.ActiveStatus = "Expired"
                membershipRecord.StatusRemarks = "Payment Overdue - Membership Expired on {}".format(membershipRecord.EndDate.strftime("%d/%m/%Y"))
                db.session.commit()
                # Create a new Membership Log with "Expired - Payment Overdue" status, and a description of "Membership record expired on dd/mm/yyyy - payment overdue" where dd/mm/yyyy is the Membership Record's End Date
                membershipLog = MembershipLog(
                    Date=currentDate,
                    Description="Membership record expired on {} - payment overdue".format(membershipRecord.EndDate.strftime("%d/%m/%Y")),
                    ActionType="Expired - Payment Overdue",
                    MembershipRecordId=membershipRecord.MembershipRecordId
                )
                db.session.add(membershipLog)
                db.session.commit()
        # Else if the Membership Record's End Date is the same or before the current date, update the MembershipRecord's ActiveStatus to "Expired", and StatusRemarks to "Pending Payment - Please make payment by dd/mm/yyyy to renew" where dd/mm/yyyy is 3 days after the Membership Record's End Date 
        # !!!(This is used to give the user a 3 day grace period to make payment)!!!
        elif membershipRecord.EndDate <= currentDate:
            membershipRecord.ActiveStatus = "Expired"
            membershipRecord.StatusRemarks = "Pending Payment - Please make payment by {} to renew".format((membershipRecord.EndDate + timedelta(days=3)).strftime("%d/%m/%Y"))

            db.session.commit()

        # Else if the Membership Record is about to expire in 7 days (by using the current date and the Membership Record's End Date), update the MembershipRecord's StatusRemarks to "Membership Expiring - Please make payment by dd/mm/yyyy to renew" where dd/mm/yyyy is the Membership Record's End Date
        # !!!(This is used to give the user an early reminder to make payment before membership expires)!!!
        elif membershipRecord.EndDate <= currentDate + timedelta(days=7):
            membershipRecord.StatusRemarks = "Membership Expiring - Please make payment by {} to renew".format(membershipRecord.EndDate.strftime("%d/%m/%Y"))
            db.session.commit()

        
    # Return a success message
    return (
        "Membership Records have been refreshed."
    ), 200

# Function and Route for PayPal Webhook to record payments
@app.route("/recordPayment", methods=['POST'])
def recordPayment():
        # # Validate Webhook First
        transmission_id = request.headers.get('PAYPAL-TRANSMISSION-ID')
        transmission_time = request.headers.get('PAYPAL-TRANSMISSION-TIME')
        transmission_sig = request.headers.get('PAYPAL-TRANSMISSION-SIG')
        auth_algo = request.headers.get('PAYPAL-AUTH-ALGO')

        data = {
            'auth_algo': auth_algo, 
            'cert_url':request.headers.get('PAYPAL-CERT-URL'),
            'transmission_id': transmission_id,
            'transmission_sig': transmission_sig,
            'transmission_time': transmission_time,
            'webhook_id': '6HJ03451BX462510T',
            'webhook_event': request.get_json()
        }

        access_token = get_access_token()
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        validation = requests.post('https://api-m.sandbox.paypal.com/v1/notifications/verify-webhook-signature',
                            headers=headers, data=json.dumps(data))
        
        verification = validation.json()
        if (verification['verification_status'] == "SUCCESS"):
            data = request.get_json()
            transactionID = data['resource']['id']
            subscriptionID = 0
            transactionDate = datetime.now()
            for i in data['resource']:
                # Subscription
                if i == 'billing_agreement_id':
                    subscriptionID = data['resource']['billing_agreement_id']
                    amount = data['resource']['amount']['total']
                # One Time Payments
                if i =='supplementary_data':
                    transactionID = data['resource']['supplementary_data']['related_ids']['order_id']
                    amount = data['resource']['amount']['value']
            
            # Get the MembershipRecordId based on the PayPalSubscriptionId
            if(subscriptionID != 0):
                # Subscriptions
                paymentList = MembershipRecord.query.filter_by(PayPalSubscriptionId=subscriptionID).first()
            else:
                # One Time Payments
                paymentList = MembershipRecord.query.filter_by(PayPalSubscriptionId=transactionID).first()
            paymentList = paymentList.json()

            newPayment = Payment(
                PayPalTransactionId = transactionID, ## Take the invoice number
                MembershipRecordId = paymentList['MembershipRecordId'],
                TransactionDate = transactionDate,
                Amount = amount,
                Discount = 0,
                PaymentMode = "PayPal"
            )

            # Check if amount is equal to $70, which is the initial setup fee. If it is not, check if this is the very first payment or not by checking the Payment table using this MembershipRecordId. If it is NOT the first payment, run the extendMembershipRecordDates function to extend the membership by 1 month or 1 year depending on the membership type. Else if it is the first payment, do not extend the membership.
            if amount != "70.00":
                payment = Payment.query.filter_by(MembershipRecordId=paymentList['MembershipRecordId']).first()
                if payment:
                    extendMembershipRecordDates(paymentList['MembershipRecordId'])
                
            db.session.add(newPayment)
            db.session.commit()

            # Disburse Points to the User's Membership Record after successful payment
            disbursePoints(paymentList['MembershipRecordId'])

            return ("Payment Successfully Recorded"), 201

# Function to extend the membership after successful payment
def extendMembershipRecordDates(MembershipRecordId):
    # First, get the MembershipRecord based on the MembershipRecordId
    membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()

    # Then, get the Membership based on the MembershipId to check if it is a monthly or yearly membership
    membership = Memberships.query.filter_by(MembershipTypeId=membershipRecord.MembershipTypeId).first()

    # If it is a monthly membership, extend the membership by 1 month
    if membership.Type == "Monthly":
        # Update the MembershipRecord by extending the End Date by 1 month, but keeping the same day e.g. from 2021-01-15 to 2021-02-15. Similarly, update the MembershipRecord Start Date to the old End Date to reflect the validity of the new membership. And if the current date is less than the MembershipRecord's new End Date, we change the MembershipRecord's ActiveStatus to "Active"
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()
        membershipRecord.EndDate = membershipRecord.EndDate + relativedelta(months=1)
        membershipRecord.StartDate = membershipRecord.EndDate - relativedelta(months=1)
        if datetime.now().date() < membershipRecord.EndDate:
            membershipRecord.ActiveStatus = "Active"
            # Change the MembershipRecord's StatusRemarks to null to indicate all is well
            # !!!(This is used to remove any previous remarks that may have been set)!!!
            membershipRecord.StatusRemarks = None
        db.session.commit()

        # Create a new Membership Log entry to record the extension of the membership
        membershipLog = MembershipLog(
            Date=datetime.now().date(),
            Description="Membership extended by 1 month to {}".format(membershipRecord.EndDate.strftime("%d/%m/%Y")),
            ActionType="Membership Extended",
            MembershipRecordId=MembershipRecordId
        )
        db.session.add(membershipLog)
        db.session.commit()

    # Else if it is a yearly membership, extend the membership by 1 year
    elif membership.Type == "Yearly":
        # Update the MembershipRecord by extending the End Date by 1 year, but keeping the same day e.g. from 2021-01-15 to 2022-01-15. Similarly, update the MembershipRecord Start Date to the old End Date to reflect the validity of the new membership. And if the current date is less than the MembershipRecord's new End Date, we change the MembershipRecord's ActiveStatus to "Active"
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()
        membershipRecord.EndDate = membershipRecord.EndDate + relativedelta(years=1)
        membershipRecord.StartDate = membershipRecord.EndDate - relativedelta(years=1)
        if datetime.now().date() < membershipRecord.EndDate:
            membershipRecord.ActiveStatus = "Active"
            # Change the MembershipRecord's StatusRemarks to null to indicate all is well
            # !!!(This is used to remove any previous remarks that may have been set)!!!
            membershipRecord.StatusRemarks = None 
        db.session.commit()

        # Create a new Membership Log entry to record the extension of the membership
        membershipLog = MembershipLog(
            Date=datetime.now().date(),
            Description="Membership extended by 1 year to {}".format(membershipRecord.EndDate.strftime("%d/%m/%Y")),
            ActionType="Membership Extended",
            MembershipRecordId=MembershipRecordId
        )
        db.session.add(membershipLog)
        db.session.commit()

# Function and Route to get all Payments history by MembershipRecordId
@app.route('/payments/history/membershiprecord/<int:MembershipRecordId>')
def getPaymentsHistoryByMembershipRecordId(MembershipRecordId):
    paymentList = Payment.query.filter_by(MembershipRecordId=MembershipRecordId).all()
    if len(paymentList):
        return jsonify(
            [
                payment.json() for payment in paymentList
            ]
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments for MembershipRecordId {}.".format(MembershipRecordId),
            "error": True
        }
    ), 404

# Function to disburse Points to the User's Membership Record after successful payment
def disbursePoints(MembershipRecordId):
    # First, get the Membership Record using the MembershipRecordId
    membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()

    # Then, get the Membership using the MembershipId
    membership = Memberships.query.filter_by(MembershipTypeId=membershipRecord.MembershipTypeId).first()

    # Then, get the complete history of the Membership Record's Points
    pointsList = Points.query.filter_by(MembershipRecordId=MembershipRecordId).all()

    # Check if it is a monthly or yearly membership
    if membership.Type == "Monthly":
        # If it is a monthly membership, check if there are any previous Points history.  
        if len(pointsList):
            latestPoints = Points.query.filter_by(MembershipRecordId=MembershipRecordId).order_by(Points.PointsId.desc()).first()
            # If the latest Points record's PointsStartDate and PointsEndDate is equal to the MembershipRecord's StartDate and EndDate respectively, we change the Status of this Points record to "Paid", and create a new Points record for the next month, with a balance of 12 points and Status of "Not Paid".
            if latestPoints.PointsStartDate == membershipRecord.StartDate and latestPoints.PointsEndDate == membershipRecord.EndDate:
                latestPoints.Status = "Paid"
                newPoints = Points(
                    PointsStartDate=membershipRecord.StartDate + relativedelta(months=1),
                    PointsEndDate=membershipRecord.EndDate + relativedelta(months=1),
                    Balance=12,
                    Status="Not Paid",
                    MembershipRecordId=MembershipRecordId
                )
                db.session.add(newPoints)
                db.session.commit()
        # Else if there are no previous Points history, we create 2 new Points records, one for the current month, and one for the next month, with a balance of 12 points for both. For the current month, we set the Status to "Paid", and for the next month, we set the Status to "Not Paid".
        else:
            newPoints = Points(
                PointsStartDate=membershipRecord.StartDate,
                PointsEndDate=membershipRecord.EndDate,
                Balance=12,
                Status="Paid",
                MembershipRecordId=MembershipRecordId
            )
            db.session.add(newPoints)
            db.session.commit()
            newPoints = Points(
                PointsStartDate=membershipRecord.StartDate + relativedelta(months=1),
                PointsEndDate=membershipRecord.EndDate + relativedelta(months=1),
                Balance=12,
                Status="Not Paid",
                MembershipRecordId=MembershipRecordId
            )
            db.session.add(newPoints)
            db.session.commit()
    elif membership.Type == "Yearly":
        # If it is a yearly membership, we create 12 new Points records to reflect the Membership Record's StartDate and EndDate, one for each month, with a balance of 12 points for each. For each month, we set the Status to "Paid".
        for i in range(12):
            newPoints = Points(
                PointsStartDate=membershipRecord.StartDate + relativedelta(months=i),
                PointsEndDate=membershipRecord.StartDate + relativedelta(months=i+1),
                Balance=12,
                Status="Paid",
                MembershipRecordId=MembershipRecordId
            )
            db.session.add(newPoints)
            db.session.commit()
