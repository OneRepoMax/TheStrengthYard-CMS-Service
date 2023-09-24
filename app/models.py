from app import app, db

class User(db.Model):
    __tablename__ = 'User'

    UserId = db.Column(db.Integer, primary_key=True)
    EmailAddress = db.Column(db.String)
    FirstName = db.Column(db.String)
    LastName = db.Column(db.String)
    Gender = db.Column(db.String)
    DateOfBirth = db.Column(db.Date)
    HomeAddress = db.Column(db.String)
    PostalCode = db.Column(db.Integer)
    ContactNo = db.Column(db.String)
    Password = db.Column(db.String)
    UserType = db.Column(db.String)
    AccountCreationDate = db.Column(db.Date)
    DisplayPicture = db.Column(db.String)
    Verified = db.Column(db.String)

    def json(self):
        return {
            "UserId": self.UserId,
            "EmailAddress": self.EmailAddress,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Gender": self.Gender,
            "DateOfBirth": self.DateOfBirth,
            "HomeAddress": self.HomeAddress,
            "PostalCode": self.PostalCode,
            "ContactNo": self.ContactNo,
            "Password": self.Password,
            "UserType": self.UserType,
            "AccountCreationDate": self.AccountCreationDate,
            "DisplayPicture": self.DisplayPicture,
            "Verified": self.Verified
        }

class IndemnityForm(db.Model):
    __tablename__ = 'IndemnityForm'

    IndemnityFormId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'),primary_key=True)
    FeedbackDiscover = db.Column(db.String)
    MedicalHistory = db.Column(db.String)
    MedicalRemarks = db.Column(db.String)
    AcknowledgementTnC = db.Column(db.Boolean, default=True)
    AcknowledgementOpenGymRules = db.Column(db.Boolean, default=True)

    def json(self):
        return {
            "IndemnityFormId": self.IndemnityFormId,
            "UserId": self.UserId,
            "FeedbackDiscover": self.FeedbackDiscover,
            "MedicalHistory": self.MedicalHistory,
            "MedicalRemarks": self.MedicalRemarks,
            "AcknowledgementTnC": self.AcknowledgementTnC,
            "AcknowledgementOpenGymRules": self.AcknowledgementOpenGymRules
        }
    
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
    
class Memberships(db.Model):
    __tablename__ = 'Memberships'

    MembershipTypeId = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String)
    Visibility = db.Column(db.String)
    BaseFee = db.Column(db.Float)
    Title = db.Column(db.String)
    Description = db.Column(db.String)
    Picture = db.Column(db.String)
    PayPalPlanId = db.Column(db.String)
    SetupFee = db.Column(db.Float)

    def json(self):
        return {
            "MembershipTypeId": self.MembershipTypeId,
            "Type": self.Type,
            "Visibility": self.Visibility,
            "BaseFee": self.BaseFee,
            "Title": self.Title,
            "Description": self.Description,
            "Picture": self.Picture,
            "PayPalPlanId": self.PayPalPlanId,
            "SetupFee": self.SetupFee
        }
    
    def jsonWithUser(self):
        return {
            "MembershipTypeId": self.MembershipTypeId,
            "Type": self.Type,
            "Visibility": self.Visibility,
            "BaseFee": self.BaseFee,
            "Title": self.Title,
            "Description": self.Description,
            "Picture": self.Picture,
            "PayPalPlanId": self.PayPalPlanId,
            "SetupFee": self.SetupFee,
            "User": [user.json() for user in self.User]
        }
    
class MembershipRecord(db.Model):
    __tablename__ = 'MembershipRecord'

    MembershipRecordId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PayPalSubscriptionId = db.Column(db.String)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), primary_key=True)
    MembershipTypeId = db.Column(db.Integer, db.ForeignKey('Memberships.MembershipTypeId'), primary_key=True)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    ActiveStatus = db.Column(db.String, default='Active')
    StatusRemarks = db.Column(db.String)
    User = db.relationship('User', backref=db.backref('Memberships', cascade='all, delete-orphan'))
    Membership = db.relationship('Memberships', backref=db.backref('Memberships', cascade='all, delete-orphan'))

    def json(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "PayPalSubscriptionId": self.PayPalSubscriptionId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "ActiveStatus": self.ActiveStatus,
            "StatusRemarks": self.StatusRemarks
        }

    def jsonWithUserAndMembership(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "PayPalSubscriptionId": self.PayPalSubscriptionId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "ActiveStatus": self.ActiveStatus,
            "StatusRemarks": self.StatusRemarks,
            "User": self.User.json(),
            "Membership": self.Membership.json()
        }
    
    def jsonWithMembership(self):
        return {
            "MembershipRecordId": self.MembershipRecordId,
            "PayPalSubscriptionId": self.PayPalSubscriptionId,
            "UserId": self.UserId,
            "MembershipTypeId": self.MembershipTypeId,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "ActiveStatus": self.ActiveStatus,
            "StatusRemarks": self.StatusRemarks,
            "Membership": self.Membership.json()
        }
    
class MembershipLog(db.Model):
    __tablename__ = 'MembershipLog'

    MembershipLogId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    ActionType = db.Column(db.String)
    Description = db.Column(db.String)
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))
    MembershipRecord = db.relationship('MembershipRecord', backref=db.backref('MembershipRecord', cascade='all, delete-orphan'))

    def json(self):
        return {
            "MembershipLogId": self.MembershipLogId,
            "Date": self.Date,
            "ActionType": self.ActionType,
            "Description": self.Description,
            "MembershipRecordId": self.MembershipRecordId
        }

    def jsonWithMembershipRecord(self):
        return {
            "MembershipLogId": self.MembershipLogId,
            "Date": self.Date,
            "ActionType": self.ActionType,
            "Description": self.Description,
            "MembershipRecordId": self.MembershipRecordId,
            "MembershipRecord": self.MembershipRecord.json()
        }