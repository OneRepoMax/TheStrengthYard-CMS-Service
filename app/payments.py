from app import app, db
from flask import jsonify, request
from datetime import datetime

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
