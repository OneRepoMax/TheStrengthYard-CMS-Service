from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.membership import MembershipRecord, MembershipLog, Memberships
import requests
import json
from app.auth import get_access_token


class Payment(db.Model):
    __tablename__ = 'Payment'

    PaymentId = db.Column(db.Integer, primary_key=True)
    PayPalTransactionId = db.Column(db.String(255))
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))
    TransactionDate = db.Column(db.Date, nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    Discount = db.Column(db.Float, nullable=False)
    PaymentMode = db.Column(db.String(255), nullable=False)

    def json(self):
        return {
            'PaymentId': self.PaymentId,
            'PayPalTransactionId': self.PayPalTransactionId,
            'MembershipRecordId': self.MembershipRecordId,
            'TransactionDate': self.TransactionDate,
            'Amount': self.Amount,
            'Discount': self.Discount,
            'PaymentMode': self.PaymentMode
        }
    
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

# Function and Route to make a monthly Payment for a MembershipRecord
@app.route('/payments/membershiprecord/<int:MembershipRecordId>', methods=['POST'])
def makePayment(MembershipRecordId):
    """
    Sample Request (if any other mode than PayPal is used)
    {
        "PayPalTransactionId": null,
        "Amount": 250,
        "Discount": 0,
        "PaymentMode": "PayNow"
    }
    Sample Request (if PayPal is used)
    {
        "PayPalTransactionId": "1234567890",
        "Amount": 250,
        "Discount": 0,
        "PaymentMode": "PayPal"
    }
    """
    data = request.get_json()
    payment = Payment(
        PayPalTransactionId = data['PayPalTransactionId'],
        MembershipRecordId = MembershipRecordId,
        TransactionDate = datetime.now(),
        Amount = data['Amount'],
        Discount = data['Discount'],
        PaymentMode = data['PaymentMode']
    )
    try:
        db.session.add(payment)
        db.session.commit()

        # Update the MembershipRecord by extending the End Date by 1 month, but keeping the same day e.g. from 2021-01-15 to 2021-02-15. And if the current date is less than the MembershipRecord's new End Date, we change the MembershipRecord's ActiveStatus to "Active"
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()
        membershipRecord.EndDate = membershipRecord.EndDate + relativedelta(months=1)
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

        return jsonify(
            payment.json()
        ), 201

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the payment.",
                "error": True
            }
        ), 500
    
# Function and Route to make a yearly Payment for a MembershipRecord
@app.route('/payments/yearly/membershiprecord/<int:MembershipRecordId>', methods=['POST'])
def makeYearlyPayment(MembershipRecordId):
    """
    Sample Request (if any other mode than PayPal is used)
    {
        "PayPalTransactionId": null,
        "Amount": 2400,
        "Discount": 0,
        "PaymentMode": "PayNow"
    }
    Sample Request (if PayPal is used)
    {
        "PayPalTransactionId": "1234567890",
        "Amount": 2400,
        "Discount": 0,
        "PaymentMode": "PayPal"
    }
    """
    data = request.get_json()
    payment = Payment(
        PayPalTransactionId = data['PayPalTransactionId'],
        MembershipRecordId = MembershipRecordId,
        TransactionDate = datetime.now(),
        Amount = data['Amount'],
        Discount = data['Discount'],
        PaymentMode = data['PaymentMode']
    )
    try:
        db.session.add(payment)
        db.session.commit()

        # Update the MembershipRecord by extending the End Date by 1 year, but keeping the same day e.g. from 2021-01-15 to 2022-01-15. And if the current date is less than the MembershipRecord's new End Date, we change the MembershipRecord's ActiveStatus to "Active"
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()
        membershipRecord.EndDate = membershipRecord.EndDate + relativedelta(years=1)
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

        return jsonify(
            payment.json()
        ), 201

    except:
        return jsonify(
            {
                "code": 400,
                "message": "An error occurred creating the payment.",
                "error": True
            }
        ), 400
    
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

@app.route("/recordPayment", methods=['POST'])
def recordPayment():

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
        
        print(validation.text)
        

        data = request.get_json()
        transactionID = data['resource']['id']
        transactionDate = datetime.now()
        # subscriptionID = data['resource']['billing_agreement_id']
        amount = data['resource']['amount']['total']
        newPayment = Payment(
            PayPalTransactionId = transactionID, ## Take the invoice number
            MembershipRecordId = 1,
            TransactionDate = transactionDate,
            Amount = amount,
            Discount = 0,
            PaymentMode = "PayPal"
        )

        db.session.add(newPayment)
        db.session.commit()

        return ("Success"), 200
    # else:
    #     return ("Recieved"), 200