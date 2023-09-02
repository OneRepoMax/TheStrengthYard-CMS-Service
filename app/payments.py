from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.membership import MembershipRecord, MembershipLog, Memberships


class Payment(db.Model):
    __tablename__ = 'Payment'

    PaymentId = db.Column(db.Integer, primary_key=True)
    PayPalId = db.Column(db.String(255))
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))
    TransactionDate = db.Column(db.Date, nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    Discount = db.Column(db.Float, nullable=False)
    PaymentMode = db.Column(db.String(255), nullable=False)

    def json(self):
        return {
            'PaymentId': self.PaymentId,
            'PayPalId': self.PayPalId,
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

# Functioon and Route to make a monthly Payment for a MembershipRecord
@app.route('/payments/membershiprecord/<int:MembershipRecordId>', methods=['POST'])
def makePayment(MembershipRecordId):
    """
    Sample Request (if any other mode than PayPal is used)
    {
        "PayPalId": null,
        "Amount": 250,
        "Discount": 0,
        "PaymentMode": "PayNow"
    }
    Sample Request (if PayPal is used)
    {
        "PayPalId": "1234567890",
        "Amount": 250,
        "Discount": 0,
        "PaymentMode": "PayPal"
    }
    """
    data = request.get_json()
    payment = Payment(
        PayPalId = data['PayPalId'],
        MembershipRecordId = MembershipRecordId,
        TransactionDate = datetime.now(),
        Amount = data['Amount'],
        Discount = data['Discount'],
        PaymentMode = data['PaymentMode']
    )
    try:
        db.session.add(payment)
        db.session.commit()

        # Update the MembershipRecord by extending the End Date by 1 month, but keeping the same day e.g. from 2021-01-15 to 2021-02-15. And if the MembershipRecord's is anything but "Active", change it to "Active"
        membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=MembershipRecordId).first()
        membershipRecord.EndDate = membershipRecord.EndDate + relativedelta(months=1)
        if membershipRecord.ActiveStatus != "Active":
            membershipRecord.ActiveStatus = "Active"
        db.session.commit()

        # Create a new Membership Log entry to record the extension of the membership
        membershipLog = MembershipLog(
            Date=datetime.now().date(),
            Description="Membership extended by 1 month",
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
    
# Function and Route to refresh the ActiveStatus of all Membership Records by checking the Payment Date and Membership Record End Date
@app.route("/membershiprecord/refresh")
def refreshMembershipRecords():
    # First, get a list of all Membership Types that are Monthly
    monthlyMembershipList = Memberships.query.filter_by(Type="Monthly").all()

    # Save the current date
    currentDate = datetime.now().date()

    # Then, using the Membership Type ID of this monthlyMembershipList, get a list of all Membership Records that are Monthly
    monthlyMembershipRecordList = MembershipRecord.query.filter(MembershipRecord.MembershipTypeId.in_([membership.MembershipTypeId for membership in monthlyMembershipList])).all()

    # Using this monthlyMembershipRecordList, for each Membership Record, check if the membership record has expired by using the current date and the Membership Record's End Date. 
    for membershipRecord in monthlyMembershipRecordList:
        # IF Membership Record's End Date is before or the same as the current date, then first check the latest Payment made for this Membership Record.  
        if membershipRecord.EndDate <= currentDate:
            latestPayment = Payment.query.filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).order_by(Payment.TransactionDate.desc()).first()
            # IF the latest Payment Date is more than 3 days before the current date, then update the Membership Record's ActiveStatus to "Expired - Payment Overdue"
            if latestPayment.TransactionDate < currentDate - timedelta(days=3):
                membershipRecord.ActiveStatus = "Expired - Payment Overdue"
                db.session.commit()
                # Create a new Membership Log with "Expired - Payment Overdue" status
                membershipLog = MembershipLog(
                    Date=currentDate,
                    Description="Membership record expired - payment overdue",
                    ActionType="Expired - Payment Overdue",
                    MembershipRecordId=membershipRecord.MembershipRecordId
                )
                db.session.add(membershipLog)
                db.session.commit()
    
    # Return a success message
    return jsonify(
        {
            "code": 200,
            "error": False,
            "message": "Membership Records have been refreshed."
        }
    ), 200