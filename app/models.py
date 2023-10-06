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
    
    def jsonMinInfo(self):
        return {
            "UserId": self.UserId,
            "EmailAddress": self.EmailAddress,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Gender": self.Gender,
            "UserType": self.UserType,
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
    
class Class(db.Model):
    __tablename__ = 'Class'

    ClassId = db.Column(db.Integer, primary_key=True)
    ClassName = db.Column(db.String)
    Description = db.Column(db.String)
    MaximumCapacity = db.Column(db.Integer)

    def json(self):
        return {
            "ClassId": self.ClassId,
            "ClassName": self.ClassName,
            "Description": self.Description,
            "MaximumCapacity": self.MaximumCapacity
        }
    
class ClassSlot(db.Model):
    __tablename__ = 'ClassSlot'

    ClassSlotId = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.String)
    StartTime = db.Column(db.DateTime)
    EndTime = db.Column(db.DateTime)
    Duration = db.Column(db.Integer)
    CurrentCapacity = db.Column(db.Integer)
    ClassId = db.Column(db.Integer, db.ForeignKey('Class.ClassId'))
    Class = db.relationship('Class', backref=db.backref('Class', cascade='all, delete-orphan'))

    def json(self):
        return {
            "ClassSlotId": self.ClassSlotId,
            "Day": self.Day,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
            "Duration": self.Duration,
            "CurrentCapacity": self.CurrentCapacity,
            "ClassId": self.ClassId
        }
    
    def jsonWithClass(self):
        return {
            "ClassSlotId": self.ClassSlotId,
            "Day": self.Day,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
            "Duration": self.Duration,
            "CurrentCapacity": self.CurrentCapacity,
            "ClassId": self.ClassId,
            "Class": self.Class.json()
        }
    
class Booking(db.Model):
    __tablename__ = 'Booking'

    BookingId = db.Column(db.Integer, primary_key=True)
    BookingDateTime = db.Column(db.DateTime)
    Status = db.Column(db.String)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    ClassSlotId = db.Column(db.Integer, db.ForeignKey('ClassSlot.ClassSlotId'))
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))
    User = db.relationship('User', backref=db.backref('Booking', cascade='all, delete-orphan'))
    ClassSlot = db.relationship('ClassSlot', backref=db.backref('Booking', cascade='all, delete-orphan'))
    MembershipRecord = db.relationship('MembershipRecord', backref=db.backref('Booking', cascade='all, delete-orphan'))

    def json(self):
        return {
            "BookingId": self.BookingId,
            "BookingDateTime": self.BookingDateTime,
            "Status": self.Status,
            "UserId": self.UserId,
            "ClassSlotId": self.ClassSlotId,
            "MembershipRecordId": self.MembershipRecordId
        }
    
    def jsonWithUserAndClassSlot(self):
        return {
            "BookingId": self.BookingId,
            "BookingDateTime": self.BookingDateTime,
            "Status": self.Status,
            "UserId": self.UserId,
            "ClassSlotId": self.ClassSlotId,
            "User": self.User.json(),
            "MembershipRecordId": self.MembershipRecordId,
            "ClassSlot": self.ClassSlot.json()
        }
    
class Points(db.Model):
    __tablename__ = 'Points'

    PointsId = db.Column(db.Integer, primary_key=True)
    MembershipRecordId = db.Column(db.Integer, db.ForeignKey('MembershipRecord.MembershipRecordId'))
    PointsStartDate = db.Column(db.Date)
    PointsEndDate = db.Column(db.Date)
    Balance = db.Column(db.Integer)
    Status = db.Column(db.String)
    MembershipRecord = db.relationship('MembershipRecord', backref=db.backref('Points', cascade='all, delete-orphan'))

    def json(self):
        return {
            "PointsId": self.PointsId,
            "MembershipRecordId": self.MembershipRecordId,
            "PointsStartDate": self.PointsStartDate,
            "PointsEndDate": self.PointsEndDate,
            "Balance": self.Balance,
            "Status": self.Status
        }
    
    def jsonWithMembershipRecord(self):
        return {
            "PointsId": self.PointsId,
            "MembershipRecordId": self.MembershipRecordId,
            "PointsStartDate": self.PointsStartDate,
            "PointsEndDate": self.PointsEndDate,
            "Balance": self.Balance,
            "Status": self.Status,
            "MembershipRecord": self.MembershipRecord.json()
        }


class Schedule(db.Model):
    __tablename__ = 'Schedule'

    ScheduleId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    PublishDate = db.Column(db.Date)
    Title = db.Column(db.String)
    Description = db.Column(db.String)
    ImgUrl = db.Column(db.String)

    User = db.relationship('User', backref=db.backref('Schedule', cascade='all, delete-orphan'))

    def json(self):
        return {
            "ScheduleId": self.ScheduleId,
            "UserId": self.UserId,
            "PublishDate": self.PublishDate,
            "Title": self.Title,
            "Description": self.Description,
            "ImgUrl": self.ImgUrl
        }
    
    def jsonWithUser(self):
        return {
            "ScheduleId": self.ScheduleId,
            "PublishDate": self.PublishDate,
            "Title": self.Title,
            "Description": self.Description,
            "ImgUrl": self.ImgUrl,
            "User": self.User.jsonMinInfo()
        }
    

    
