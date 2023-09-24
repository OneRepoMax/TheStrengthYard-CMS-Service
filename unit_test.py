import unittest
from app.user import User, IndemnityForm
from app.membership import Memberships, MembershipRecord, MembershipLog

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(
            UserId = 101,
            EmailAddress = "tanahkao@gmail.com",
            FirstName = "Ah Kao",
            LastName = "Tan",
            Gender = "F",
            DateOfBirth = "1945-01-01", 
            HomeAddress = "Geylang Lorong 23",
            PostalCode = 670123,
            ContactNo = "91234567",
            Password = "iactuallylovecats",
            UserType = "C",
            AccountCreationDate = "2023-01-01",
            DisplayPicture = "sample.jpg",
            Verified = 0
        )

    def tearDown(self):
        self.user = None

    def test_json(self):
        self.assertEqual(self.user.json(), {
            "UserId": 101,
            "EmailAddress": "tanahkao@gmail.com",
            "FirstName": "Ah Kao",
            "LastName": "Tan",
            "Gender": "F",
            "DateOfBirth": "1945-01-01",
            "HomeAddress": "Geylang Lorong 23",
            "PostalCode": 670123,
            "ContactNo": "91234567",
            "Password": "iactuallylovecats",
            "UserType": "C",
            "AccountCreationDate": "2023-01-01",
            "DisplayPicture": "sample.jpg",
            "Verified": 0
        })

class TestIndemnityForm(unittest.TestCase):
    def setUp(self):
        self.IndemnityForm = IndemnityForm(
            IndemnityFormId = 1,
            UserId = 1,
            FeedbackDiscover = "Instagram",
            MedicalHistory = "Asthma",
            MedicalRemarks = "",
            AcknowledgementTnC = True,
            AcknowledgementOpenGymRules = True
        )

    def tearDown(self):
        self.IndemnityForm = None

    def test_json(self):
        self.assertEqual(self.IndemnityForm.json(), {
            "IndemnityFormId": 1,
            "UserId": 1,
            "FeedbackDiscover": "Instagram",
            "MedicalHistory": "Asthma",
            "MedicalRemarks": "",
            "AcknowledgementTnC" : True,
            "AcknowledgementOpenGymRules" : True
        })

class TestMembership(unittest.TestCase):
    def setUp(self):
        self.membership = Memberships(
            MembershipTypeId = 1,
            Type = "Monthly",
            BaseFee = 250,
            Title = "Progressive Strength Class Membership (Standard)",
            Description = "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.",
            Picture = "sample.jpg"
        )

    def tearDown(self):
        self.membership = None

    def test_json(self):
        self.assertEqual(self.membership.json(), {
            "MembershipTypeId": 1,
            "Type": "Monthly",
            "BaseFee": 250,
            "Title": "Progressive Strength Class Membership (Standard)",
            "Description": "Get access to our Progressive Strength Class and enjoy a well-rounded fitness experience. This membership includes monthly sessions to help you build strength and improve your overall fitness.",
            "Picture": "sample.jpg"
        })

class TestMembershipLog(unittest.TestCase):
    def setUp(self):
        self.membershipLog = MembershipLog(
            MembershipLogId = 900,
            Date = "2023-01-01",
            ActionType = "Membership record created",
            Description = "Created",
            MembershipRecordId = 1
        )

    def tearDown(self):
        self.membershipLog = None

    def test_json(self):
        self.assertEqual(self.membershipLog.json(), {
            "MembershipLogId": 900,
            "Date": "2023-01-01",
            "ActionType": "Membership record created",
            "Description": "Created",
            "MembershipRecordId": 1
        })

class TestMembershipRecord(unittest.TestCase):
    def setUp(self):
        self.membershipRecord = MembershipRecord(
            MembershipRecordId = 1,
            MembershipTypeId = 100,
            UserId = 5,
            StartDate = "2023-01-01",
            EndDate = "2023-05-01",
            ActiveStatus = "Active",
            StatusRemarks = "Status Text"
        )

    def tearDown(self):
        self.membershipRecord = None

    def test_json(self):
        self.assertEqual(self.membershipRecord.json(), {
            "MembershipRecordId": 1,
            "MembershipTypeId": 100,
            "UserId": 5,
            "StartDate": "2023-01-01",
            "EndDate": "2023-05-01",
            "ActiveStatus": "Active",
            "StatusRemarks": "Status Text"
        })

if __name__ == "__main__":
    unittest.main()