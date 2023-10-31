from app import app, db
from flask import jsonify, request, url_for, render_template
from datetime import datetime, timedelta
import requests, json
from app.models import MembershipRecord, Class, ClassSlot, Booking, User, Points, Memberships, MembershipClassMapping
from app.email import send_email
from app.user import verifyEmail
from app.token import token_required

# Function and Route to Create a new Class
@app.route("/class", methods=['POST'])
@token_required
def createClass(current_user):
    """
    Sample Request
    {
        "ClassName": "Yoga Class",
        "Description": "Learn the art of Yoga",
        "MaximumCapacity": 10
    }
    """
    data = request.get_json()
    className = data.get("ClassName")
    description = data.get("Description")
    maximumCapacity = data.get("MaximumCapacity")

    # Check className, description and maximumCapacity are not empty
    if not className or not description or not maximumCapacity:
        return "Invalid class details", 400
    
    # Create new class
    newClass = Class(
        ClassName=className,
        Description=description,
        MaximumCapacity=maximumCapacity
    )

    # Add new class to database
    db.session.add(newClass)
    db.session.commit()

    return jsonify(
        newClass.json()
        ), 201

# Function and Route to get all Classes
@app.route("/class")
@token_required
def getAllClass(current_user):
    classList = Class.query.all()
    return jsonify([c.json() for c in classList]), 200

# Function and Route to get a Class by ID
@app.route("/class/<int:id>")
@token_required
def getClassByID(current_user, id: int):
    classList = Class.query.filter_by(ClassId=id).all()
    if len(classList):
        return jsonify(
            [c.json() for c in classList]
        ), 200
    return "There are no such class with ID: " + str(id), 406

# Function and Route to update a Class by ID
@app.route("/class/<int:id>", methods=['PUT'])
@token_required
def updateClassByID(current_user, id: int):
    """
    Sample Request
    {
        "ClassName": "Flying Class",
        "Description": "Learn the art of Flying",
        "MaximumCapacity": 50
    }
    """
    data = request.get_json()
    className = data.get("ClassName")
    description = data.get("Description")
    maximumCapacity = data.get("MaximumCapacity")

    # Check className, description and maximumCapacity are not empty
    if not className or not description or not maximumCapacity:
        return "Invalid class details", 400

    # Check if class exists
    classExists = Class.query.filter_by(ClassId=id).first()
    if not classExists:
        return "There are no such class with ID: " + str(id), 406

    # Update class
    classExists.ClassName = className
    classExists.Description = description
    classExists.MaximumCapacity = maximumCapacity

    # Add updated class to database
    db.session.add(classExists)
    db.session.commit()

    return jsonify(
        classExists.json()
        ), 200

# Function and Route to update a Class Slot by ID
@app.route("/classSlot/<int:id>", methods=['PUT'])
@token_required
def updateClassSlotByID(current_user, id: int):
    """
    Sample Request
    {
        "Day": "Sunday",
        "StartTime": "09:00:00",
        "EndTime": "10:00:00",
    }
    """
    data = request.get_json()
    day = data.get("Day")
    startTime = data.get("StartTime")
    endTime = data.get("EndTime")

    # Check className, description and maximumCapacity are not empty
    if not day or not startTime or not endTime:
        return "Invalid class details", 400

    # Check if class exists
    classExists = ClassSlot.query.filter_by(ClassSlotId=id).first()
    if not classExists:
        return "There are no such class with ID: " + str(id), 406

    # Update class
    classExists.Day = day
    classExists.StartTime = startTime
    classExists.EndTime = endTime

    # Add updated class to database
    db.session.add(classExists)
    db.session.commit()

    return jsonify(
        classExists.json()
        ), 200

# Function and Route to delete a Class by ID
@app.route("/class/<int:id>", methods=['DELETE'])
@token_required
def deleteClassByID(current_user, id: int):
    # Check if class exists
    classExists = Class.query.filter_by(ClassId=id).first()
    if not classExists:
        return "There are no such class with ID: " + str(id), 406

    # Delete class
    db.session.delete(classExists)
    db.session.commit()

    return "Class with ID: " + str(id) + " has been deleted.", 200

# Function and Route to create new Class Slots by Class ID
@app.route("/class/<int:id>/classSlot", methods=['POST'])
@token_required
def createClassSlotByClassID(current_user, id: int):
    """
    Sample Request
    {
        "Day": "Sunday",
        "StartTime": "09:00:00",
        "EndTime": "10:00:00",
        "StartingFrom": "2023-11-01",
        "RecurringUntil": "2023-12-31"
    }
    """
    data = request.get_json()

    # Get the day, start time, end time and recurring until from the request
    day = data.get("Day")
    startTime = data.get("StartTime")
    endTime = data.get("EndTime")
    recurringUntil = data.get("RecurringUntil")
    startingFrom = data.get("StartingFrom")
    
    # Compute the duration in minutes (integer) by subtracting the given end time with the given start time
    duration = int(endTime[:2]) * 60 + int(endTime[3:5]) - int(startTime[:2]) * 60 - int(startTime[3:5])

    # Create empty list to store the created class slots which is to be returned later
    classSlotList = []

    # Using the given startingFrom date, we create multiple class slots (based on the given day, start time, end time) until the given recurring until date, and add them to the database
    while startingFrom <= recurringUntil:
        # If the given day is the same as the startingFrom date's day, we create a new class slot
        if day == datetime.strptime(startingFrom, "%Y-%m-%d").strftime("%A"):
            # Create new class slot
            newClassSlot = ClassSlot(
                Day=day,
                StartTime=startingFrom + ' ' + startTime,
                EndTime=startingFrom + ' ' + endTime,
                Duration=duration,
                CurrentCapacity=0,
                ClassId=id
            )

            # Add new class slot to database
            db.session.add(newClassSlot)
            db.session.commit()

            # Add new class slot to classSlotList
            classSlotList.append(newClassSlot.json())

        # Increment the startingFrom date by 1 day
        startingFrom = datetime.strptime(startingFrom, "%Y-%m-%d").date() + timedelta(days=1)
        startingFrom = startingFrom.strftime("%Y-%m-%d")

    return jsonify(
        classSlotList
        ), 201

# Function and Route to get all Class Slots by Class ID
@app.route("/class/<int:id>/classSlot")
@token_required
def getAllClassSlotByClassID(current_user, id: int):
    classSlotList = ClassSlot.query.filter_by(ClassId=id).all()
    # Return all class slots with the given class ID, if not found, return 406
    if len(classSlotList):
        return jsonify(
            [c.json() for c in classSlotList]
        ), 200
    return "There are no such class slots with Class ID: " + str(id), 406

# Function and Route to get all Class Slots from TODAY onwards
@app.route("/classSlot")
@token_required
def getAllClassSlot(current_user):
    # Get the current date and time
    now = datetime.now()

    # Get all class slots from today onwards
    classSlotList = ClassSlot.query.filter(ClassSlot.StartTime >= now.strftime("%Y-%m-%d %H:%M:%S")).all()

    # Return all class slots from ascending order of start time
    if len(classSlotList):
        return jsonify(
            [c.jsonWithClass() for c in classSlotList]
        ), 200
    return "There are no class slots from today (" + str(now) + ") onwards", 406

# Function and Route to get a specific Class Slot by Class Slot ID
@app.route("/classSlot/<int:id>")
@token_required
def getClassSlotByID(current_user, id: int):
    classSlot = ClassSlot.query.filter_by(ClassSlotId=id).first()
    # Return the class slot with the given class slot ID, if not found, return 406
    if classSlot:
        return jsonify(
            classSlot.jsonWithClass()
        ), 200
    return "There are no such class slot with Class Slot ID: " + str(id), 406

# Function and Route to get Class Slots by Date
@app.route("/classSlot/slots/<string:date>")
@token_required
def getClassSlotByDate(current_user, date: str):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # If given date is more than 2 weeks from today, return 406
    if date > (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"):
        return "You can only view class slots up to 2 weeks from today", 406

    # Get the current DateTime
    now = datetime.now()
    print(now)

    # Get all Class Slots from DB that match the given date, and is after the current date and time (now)
    classSlotList = ClassSlot.query.filter(ClassSlot.StartTime.between(date + ' 00:00:00', date + ' 23:59:59')).filter(ClassSlot.StartTime >= now.strftime("%Y-%m-%d %H:%M:%S")).order_by(ClassSlot.StartTime).all()

    if len(classSlotList):
        return jsonify(
            [c.jsonWithClass() for c in classSlotList]
        ), 200
    return "There are no class slots on this date", 406

# Function and Route to CANCEL a ClassSlot by ID, and send email notifications to all users who have booked the class slot, and refund their points
@app.route("/classSlot/<int:id>", methods=['DELETE'])
@token_required
def deleteClassSlotByID(current_user, id: int):
    # Check if class exists
    classExists = ClassSlot.query.filter_by(ClassSlotId=id).first()
    if not classExists:
        return "There are no such class with ID: " + str(id), 406

    # Get all Bookings with the given ClassSlotId
    bookingList = Booking.query.filter_by(ClassSlotId=id).all()

    # If there are bookings, we need to refund the user's points and send them an email notification
    if len(bookingList):
        # For each booking, we need to refund the user's points and send them an email notification
        for booking in bookingList:
            # If the status of this booking is "Confirmed", we proceed with the function
            if booking.Status == "Confirmed":
                # Update the booking status to "Cancelled"
                booking.Status = "Cancelled"

                # Add updated booking to database
                db.session.add(booking)
                db.session.commit()

                # Get the MembershipRecordId from the booking
                membershipRecordId = booking.MembershipRecordId

                # Using the selectedClassSlot's StartTime, we retrive the corresponding Points row from the Points table in which the selectedClassSlot's StartTime is between the PointsStartDate and PointsEndDate. The Points row should also match the MembershipRecordId being used above
                selectedPoints = Points.query.filter(Points.PointsStartDate <= classExists.StartTime).filter(Points.PointsEndDate >= classExists.StartTime).filter_by(MembershipRecordId=membershipRecordId).first()

                # If the selectedPoints is not found, return 406
                if not selectedPoints:
                    return "There are no valid points record for the selected class slot to refund the points", 406

                # If selectedPoints is found, update the selectedPoints Balance by adding 1
                selectedPoints.Balance += 1

                # Add updated selectedPoints to database
                db.session.add(selectedPoints)
                db.session.commit()

                # Send an email notification to the user and gym owner about the booking cancellation.
                user = User.query.filter_by(UserId=booking.UserId).first()
                gymOwner = "tsy.fyp.2023@gmail.com"

                emailMessage = "Our apologies, we had to cancel this class due to unforeseen circumstances, thus your booking has been cancelled. You have been refunded 1 point. Your current points balance is " + str(selectedPoints.Balance) + "."

                html = render_template("/cancel_booking.html", user_first_name=user.FirstName, user_last_name=user.LastName, booking_id=booking.BookingId, booking_date_time=booking.BookingDateTime, class_name=classExists.Class.ClassName, class_start_time=classExists.StartTime, class_day= classExists.Day, duration=classExists.Duration, message=emailMessage, points_refunded=1, points_balance=selectedPoints.Balance)

                subject = "[NOTICE] Class Has Been Cancelled!"

                send_email(gymOwner, subject, html)
                send_email(user.EmailAddress, subject, html)

    # Delete class slot
    db.session.delete(classExists)
    db.session.commit()

    return "Class Slot with ID: " + str(id) + " has been deleted. All users who had an existing booking for this Class Slot has been notified by email and points has been refunded to them.", 200

# Function and Route to delete a given list of ClassSlots
@app.route("/classSlot/delete", methods=['POST'])
@token_required
def deleteClassSlots(current_user):
    """
    Sample Request
    {
        "ClassSlotIdList": [5002, 5003, 5004, 5005, 5006]
        }
    """
    data = request.get_json()
    classSlotIdList = data.get("ClassSlotIdList")

    # Check if class slot ID list is empty
    if not classSlotIdList:
        return "Invalid class slot ID list", 400

    # Delete all class slots with the given class slot ID list
    for classSlotId in classSlotIdList:
        # Check if class slot exists
        classSlotExists = ClassSlot.query.filter_by(ClassSlotId=classSlotId).first()
        if not classSlotExists:
            return "There are no such class slot with ID: " + str(classSlotId), 406

        # Delete class slot
        db.session.delete(classSlotExists)
        db.session.commit()

    return "Class slots with ID: " + str(classSlotIdList) + " have been deleted.", 200

# Function and Route to create a new Booking
@app.route("/booking", methods=['POST'])
@token_required
def createNewBooking(current_user):
    """
    Sample Request
    {
        "MembershipRecordId": 1,
        "UserId": 1,
        "ClassSlotId": 5002,
        }
    """
    data = request.get_json()
    membershipRecordId = data.get("MembershipRecordId")
    userId = data.get("UserId")
    classSlotId = data.get("ClassSlotId")

    # First, check if the user has an active membership record
    membershipRecord = MembershipRecord.query.filter_by(MembershipRecordId=membershipRecordId).first()
    
    if not membershipRecord:
        return "There are no such membership record with ID: " + str(membershipRecordId), 406
    
    # Then, using the MembershipTypeId in Membership Record, get the Membership. If the Membership's hasClasses is False, return 406
    membership = Memberships.query.filter_by(MembershipTypeId=membershipRecord.MembershipTypeId).first()
    
    if not membership.hasClasses:
        return "You do not have a membership that allows you to book classes", 406
    
    # Get the Class using the ClassSlotId
    classSlot = ClassSlot.query.filter_by(ClassSlotId=classSlotId).first()
    selectedClass = Class.query.filter_by(ClassId=classSlot.ClassId).first()

    # Use MembershipClassMapping to check if the user's membership type allows the user to book the selected class
    membershipClassMapping = MembershipClassMapping.query.filter_by(MembershipTypeId=membershipRecord.MembershipTypeId).filter_by(ClassId=selectedClass.ClassId).first()

    if not membershipClassMapping:
        return "Your membership does not allow you to book this class", 406
    
    # Then, check if the user has an active OR "pending payment" membership record
    if membershipRecord.ActiveStatus != "Active" and membershipRecord.ActiveStatus != "Pending Payment":
        return "The selected membership record is not active. The status is " + membershipRecord.ActiveStatus, 406

    # Then, check if the user already has an existing active booking for the selected class slot. We use the MembershipRecordId and ClassSlotId to check for this
    existingBooking = Booking.query.filter_by(MembershipRecordId=membershipRecordId).filter_by(ClassSlotId=classSlotId).filter_by(Status="Confirmed").first()

    if existingBooking:
        return "You already have an existing active booking for the selected class slot", 406

    # Retrieve the class slot with the given class slot ID
    selectedClassSlot = ClassSlot.query.filter_by(ClassSlotId=classSlotId).first()

    # Check if the class slot's current capacity is less than the class's maximum capacity
    selectedClass = Class.query.filter_by(ClassId=selectedClassSlot.ClassId).first()

    if selectedClassSlot.CurrentCapacity < selectedClass.MaximumCapacity:
        # Using the selectedClassSlot's StartTime, we retrive the corresponding Points row from the Points table in which the selectedClassSlot's StartTime is between the PointsStartDate and PointsEndDate
        selectedPoints = Points.query.filter(Points.PointsStartDate <= selectedClassSlot.StartTime).filter(Points.PointsEndDate >= selectedClassSlot.StartTime).first()

        # If the selectedPoints is not found, return 406
        if not selectedPoints:
            return "There are no valid points record for the selected class slot to make the booking", 406
        
        # If selectedPoints is found, check that the Balance is more than 0. If it is, we can proceed to create the booking and deduct one point from this selectedPoints Balance
        if selectedPoints.Balance > 0:
            # Create new booking
            newBooking = Booking(
                BookingDateTime = datetime.now(),
                Status = "Confirmed", # Default status is "Confirmed"
                UserId=userId,
                ClassSlotId=classSlotId,
                MembershipRecordId=membershipRecordId
            )

            # Add new booking to database
            db.session.add(newBooking)
            db.session.commit()

            # Update the selectedPoints Balance by deducting 1
            selectedPoints.Balance -= 1

            # Add updated selectedPoints to database
            db.session.add(selectedPoints)
            db.session.commit()

            # Update the selectedClassSlot CurrentCapacity by adding 1
            selectedClassSlot.CurrentCapacity += 1

            # Add updated selectedClassSlot to database
            db.session.add(selectedClassSlot)
            db.session.commit()

            # Send an email notification to the user and gym owner
            user = User.query.filter_by(UserId=userId).first()
            gymOwner = "tsy.fyp.2023@gmail.com"

            # Use new_booking.html template to generate the email content, with the following variables:
            # user_first_name, user_last_name, booking_id, booking_date_time, class_name, class_start_time, points_balance, duration, confirm_url
            html = render_template("/new_booking.html", user_first_name=user.FirstName, user_last_name=user.LastName, booking_id=newBooking.BookingId, booking_date_time=newBooking.BookingDateTime, class_name=selectedClass.ClassName, class_start_time=selectedClassSlot.StartTime, points_balance=selectedPoints.Balance, duration=selectedClassSlot.Duration, class_day=selectedClassSlot.Day)

            subject = "New Booking Confirmation - " + user.FirstName + " " + user.LastName
            send_email(gymOwner, subject, html)
            send_email(user.EmailAddress, subject, html)

            return jsonify(
                newBooking.json()
                ), 201
        else:
            return "You do not have enough points to make the booking", 406  
    else:
        return "The class is full", 406

# Function and Route to get ALL Bookings
@app.route("/booking")
@token_required
def getAllBookings(current_user):
    bookingList = Booking.query.all()
    return jsonify([b.jsonWithUserAndClassSlot() for b in bookingList]), 200

# Function and Route to get all upcoming Bookings by User ID
@app.route("/booking/user/<int:id>")
@token_required
def getAllBookingsByUserID(current_user, id: int):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Get all of the User's bookings from today onwards by using the given user ID
    bookingList = Booking.query.filter_by(UserId=id).filter(Booking.BookingDateTime >= today + ' 00:00:00').all()

    # If there are no bookings, return 406
    if not len(bookingList):
        return "There are no upcoming bookings for User ID: " + str(id), 406
    else:
        # Sort the booking list by Class Slot Start Time in descending order, so that the latest booking will be at the top
        bookingList.sort(key=lambda x: x.ClassSlot.StartTime, reverse=True)
        return jsonify(
            [b.jsonWithUserAndClassSlot() for b in bookingList]
        ), 200

# Function and Route to get all PAST Bookings by User ID
@app.route("/booking/user/past/<int:id>")
@token_required
def getAllPastBookingsByUserID(current_user, id: int):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Get all of the User's bookings from today onwards by using the given user ID. The Status of the Booking must be "Confirmed"
    bookingList = Booking.query.filter_by(UserId=id).filter(Booking.BookingDateTime < today + ' 00:00:00').filter_by(Status="Confirmed").all()

    # If there are no bookings, return 406
    if not len(bookingList):
        return "There are past no bookings for User ID: " + str(id), 406
    else:
        # Sort the booking list by Class Slot Start Time in descending order, so that the latest booking will be at the top
        bookingList.sort(key=lambda x: x.ClassSlot.StartTime, reverse=True)
        return jsonify(
            [b.jsonWithUserAndClassSlot() for b in bookingList]
        ), 200
    
# Function and Route to get all CANCELLED Bookings by User ID
@app.route("/booking/user/cancelled/<int:id>")
@token_required
def getAllCancelledBookingsByUserID(current_user, id: int):
    # Get all of the User's bookings that has status "Cancelled" by using the given user ID
    bookingList = Booking.query.filter_by(UserId=id).filter_by(Status="Cancelled").all()

    # If there are no bookings, return 406
    if not len(bookingList):
        return "There are no cancelled bookings for User ID: " + str(id), 406
    else:
        # Sort the booking list by Class Slot Start Time in descending order, so that the latest booking will be at the top
        bookingList.sort(key=lambda x: x.ClassSlot.StartTime, reverse=True)
        return jsonify(
            [b.jsonWithUserAndClassSlot() for b in bookingList]
        ), 200
    

# Function and Route to get a specific Booking by Booking ID
@app.route("/booking/<int:id>")
@token_required
def getBookingByID(current_user, id: int):
    booking = Booking.query.filter_by(BookingId=id).first()
    # Return the booking with the given booking ID, if not found, return 406
    if booking:
        return jsonify(
            booking.jsonWithUserAndClassSlot()
        ), 200
    return "There are no such booking with Booking ID: " + str(id), 406

# Function and Route to get all Bookings by Class Slot ID
@app.route("/booking/classSlot/<int:id>")
@token_required
def getAllBookingsByClassSlotID(current_user, id: int):
    bookingList = Booking.query.filter_by(ClassSlotId=id).all()
    # Return all bookings with the given class slot ID, if not found, return 406
    if len(bookingList):
        return jsonify(
            [b.jsonWithUserAndClassAndClassSlot() for b in bookingList]
        ), 200
    return "There are no such bookings with Class Slot ID: " + str(id), 406
    
# Function and Route to cancel a Booking by Booking ID
@app.route("/booking/cancel/<int:id>")
@token_required
def cancelBookingByID(current_user, id: int):
    # Check if booking exists
    bookingExists = Booking.query.filter_by(BookingId=id).first()
    if not bookingExists:
        return "There are no such booking with Booking ID: " + str(id), 406

    # Check if booking status is "Confirmed"
    if bookingExists.Status == "Confirmed":
        # Update booking status to "Cancelled"
        bookingExists.Status = "Cancelled"

        # Add updated booking to database
        db.session.add(bookingExists)
        db.session.commit()

        # Retrieve the class slot with the given class slot ID
        selectedClassSlot = ClassSlot.query.filter_by(ClassSlotId=bookingExists.ClassSlotId).first()

        # Update the selectedClassSlot CurrentCapacity by minusing 1
        selectedClassSlot.CurrentCapacity -= 1

        # Add updated selectedClassSlot to database
        db.session.add(selectedClassSlot)
        db.session.commit()

        # Get the MembershipRecordId from the bookingExists
        membershipRecordId = bookingExists.MembershipRecordId

        # Using the selectedClassSlot's StartTime, we retrive the corresponding Points row from the Points table in which the selectedClassSlot's StartTime is between the PointsStartDate and PointsEndDate. The Points row should also match the MembershipRecordId being used above
        selectedPoints = Points.query.filter(Points.PointsStartDate <= selectedClassSlot.StartTime).filter(Points.PointsEndDate >= selectedClassSlot.StartTime).filter_by(MembershipRecordId=membershipRecordId).first()

        # If the selectedPoints is not found, return 406
        if not selectedPoints:
            return "There are no valid points record for the selected class slot to refund the points", 406

        # Since there is a 12 hour cancellation policy, we check the current date time and the class slot's start time to see if it is more than 12 hours apart. 
        # Get the current date time
        now = datetime.now()

        # Get the class slot's start time
        classSlotStartTime = selectedClassSlot.StartTime

        # Compute the difference between the current date time and the class slot's start time
        difference = classSlotStartTime - now

        # Check if the difference is less than 12 hours. If it is, we do not refund the user's points. If it is not, we refund the user's points.
        user = User.query.filter_by(UserId=bookingExists.UserId).first()
        gymOwner = "tsy.fyp.2023@gmail.com"
        if difference < timedelta(hours=12):
            # Send an email notification to the user and gym owner about the booking cancellation. 
            emailMessage = "Your booking has been cancelled. Since the cancellation is not more than 12 hours before the class, you will not be refunded any points. Your current points balance from  is " + str(selectedPoints.Balance) + "."

            html = render_template("/cancel_booking.html", user_first_name=user.FirstName, user_last_name=user.LastName, booking_id=bookingExists.BookingId, booking_date_time=bookingExists.BookingDateTime, class_name=selectedClassSlot.Class.ClassName, class_start_time=selectedClassSlot.StartTime, class_day= selectedClassSlot.Day, duration=selectedClassSlot.Duration, message=emailMessage, points_refunded=0, points_balance=selectedPoints.Balance)

            subject = "Booking Cancellation - " + user.FirstName + " " + user.LastName
            send_email(gymOwner, subject, html)
            send_email(user.EmailAddress, subject, html)

            return "Your booking has been cancelled. You will not be refunded any points.", 200
        else:
            # If selectedPoints is found, update the selectedPoints Balance by adding 1
            selectedPoints.Balance += 1

            # Add updated selectedPoints to database
            db.session.add(selectedPoints)
            db.session.commit()

            # Send an email notification to the user and gym owner about the booking cancellation.
            emailMessage = "Your booking has been cancelled. You have been refunded 1 point. Your current points balance is " + str(selectedPoints.Balance) + "."

            html = render_template("/cancel_booking.html", user_first_name=user.FirstName, user_last_name=user.LastName, booking_id=bookingExists.BookingId, booking_date_time=bookingExists.BookingDateTime, class_name=selectedClassSlot.Class.ClassName, class_start_time=selectedClassSlot.StartTime, class_day= selectedClassSlot.Day, duration=selectedClassSlot.Duration, message=emailMessage, points_refunded=1, points_balance=selectedPoints.Balance)

            subject = "Booking Cancellation - " + user.FirstName + " " + user.LastName

            send_email(gymOwner, subject, html)
            send_email(user.EmailAddress, subject, html)

            return "Your booking has been cancelled. You have been refunded 1 point.", 200

# Function and Route to create a new Booking 2
@app.route("/booking2", methods=['POST'])
@token_required
def createNewBooking2(current_user):
    """
    Sample Request
    {
        "UserId": 1,
        "ClassSlotId": 5002
        }
    """
    data = request.get_json()
    userId = data.get("UserId")
    classSlotId = data.get("ClassSlotId")

    # First, get the Class using the ClassSlotId
    selectedClassSlot = ClassSlot.query.filter_by(ClassSlotId=classSlotId).first()
    selectedClass = Class.query.filter_by(ClassId=selectedClassSlot.ClassId).first()
    
    # Next, using the selectedClass, search the MembershipClassMapping table to get a list of MembershipTypeId that allows the user to book the selected class
    membershipClassMappingList = MembershipClassMapping.query.filter_by(ClassId=selectedClass.ClassId).all()

    print(f"\nThe MembershipClassMapping List is: {membershipClassMappingList}\n")

    # Extract all of the MembershipTypeIds from the membershipClassMappingList
    membershipTypeIdList = [m.MembershipTypeId for m in membershipClassMappingList]

    # Next, using the userId, get the MembershipRecord that belongs to the user using these search criterias:
    # ActiveStatus must be "Active" or "Pending Payment"
    # MembershipTypeId must be in the list of MembershipTypeId (membershipTypeIdList) that allows the user to book the selected class
    membershipRecord = MembershipRecord.query.filter_by(UserId=userId).filter(MembershipRecord.ActiveStatus.in_(["Active", "Pending Payment"])).filter(MembershipRecord.MembershipTypeId.in_(membershipTypeIdList)).first()

    # If there are no such membership records, return 406
    if not membershipRecord:
        return "You do not have an active membership that allows you to book this class", 406
    else:
        print(f"\nThe MembershipRecord is: {membershipRecord.json()}\n")

    # Get the MembershipRecordId from the membershipRecord
    membershipRecordId = membershipRecord.MembershipRecordId
    print(f"\nThe MembershipRecordId is: {membershipRecordId}\n")

    # Then, check if the user already has an existing active booking for the selected class slot. We use the MembershipRecordId and ClassSlotId to check for this
    existingBooking = Booking.query.filter_by(UserId=userId).filter_by(ClassSlotId=classSlotId).filter_by(Status="Confirmed").first()

    if existingBooking:
        return "You already have an existing active booking for the selected class slot", 406

    # Check if the class slot's current capacity is less than the class's maximum capacity
    if selectedClassSlot.CurrentCapacity < selectedClass.MaximumCapacity:
        # Using the selectedClassSlot's StartTime, we retrive the corresponding Points row from the Points table in which the selectedClassSlot's StartTime is between the PointsStartDate and PointsEndDate. The Points row should also match the MembershipRecordId being used above
        selectedPoints = Points.query.filter(Points.PointsStartDate <= selectedClassSlot.StartTime).filter(Points.PointsEndDate >= selectedClassSlot.StartTime).filter_by(MembershipRecordId=membershipRecordId).first()

        # If the selectedPoints is not found, return 406
        if not selectedPoints:
            return "There are no valid points record for the selected class slot to make the booking", 406
        
        # If selectedPoints is found, check that the Balance is more than 0. If it is, we can proceed to create the booking and deduct one point from this selectedPoints Balance
        if selectedPoints.Balance > 0:
            # Create new booking
            newBooking = Booking(
                BookingDateTime = datetime.now(),
                Status = "Confirmed", # Default status is "Confirmed"
                UserId=userId,
                ClassSlotId=classSlotId,
                MembershipRecordId=membershipRecordId
            )

            # Add new booking to database
            db.session.add(newBooking)
            db.session.commit()

            # Update the selectedPoints Balance by deducting 1
            selectedPoints.Balance -= 1

            # Add updated selectedPoints to database
            db.session.add(selectedPoints)
            db.session.commit()

            # Update the selectedClassSlot CurrentCapacity by adding 1
            selectedClassSlot.CurrentCapacity += 1

            # Add updated selectedClassSlot to database
            db.session.add(selectedClassSlot)
            db.session.commit()

            # Send an email notification to the user and gym owner
            user = User.query.filter_by(UserId=userId).first()
            gymOwner = "tsy.fyp.2023@gmail.com"

            # Use new_booking.html template to generate the email content, with the following variables:
            # user_first_name, user_last_name, booking_id, booking_date_time, class_name, class_start_time, points_balance, duration, confirm_url
            html = render_template("/new_booking.html", user_first_name=user.FirstName, user_last_name=user.LastName, booking_id=newBooking.BookingId, booking_date_time=newBooking.BookingDateTime, class_name=selectedClass.ClassName, class_start_time=selectedClassSlot.StartTime, points_balance=selectedPoints.Balance, duration=selectedClassSlot.Duration, class_day=selectedClassSlot.Day)

            subject = "New Booking Confirmation - " + user.FirstName + " " + user.LastName
            send_email(gymOwner, subject, html)
            send_email(user.EmailAddress, subject, html)

            return jsonify(
                newBooking.json()
                ), 201
        else:
            return "You do not have enough points to make the booking", 406  
    else:
        return "The class is full", 406
    
# Function and Route to get Points history by Membership Record ID (For Staff view)
@app.route("/pointsHistory/<int:id>")
@token_required
def getPointsHistoryByMembershipRecordID(current_user, id: int):
    pointsHistoryList = Points.query.filter_by(MembershipRecordId=id).all()
    # Return all points history with the given membership record ID, if not found, return 406
    if len(pointsHistoryList):
        return jsonify(
            [p.json() for p in pointsHistoryList]
        ), 200
    return "There are no such points history with Membership Record ID: " + str(id), 406

# Function and Route to get Points history by Membership Record ID (For User view)
@app.route("/pointsHistory/user/<int:id>")
@token_required
def getPointsHistoryByMembershipRecordIDForUser(current_user, id: int):
    # Get Points list using MembershipRecordId, but Status must be "Paid"
    pointsHistoryList = Points.query.filter_by(MembershipRecordId=id).filter_by(Status="Paid").all()
    # Return all points history with the given membership record ID, if not found, return 406
    if len(pointsHistoryList):
        return jsonify(
            [p.json() for p in pointsHistoryList]
        ), 200
    return "There are no such points history with Membership Record ID: " + str(id), 406


# Helper Function that takes in a list of ClassSlot objects and the User Id. It will return a list of ClassSlot objects that are available (not full) and that User has a valid membership for. If not, it will return the ClassSlot with new attributes e.g. "Status": "Unavailable", "Message": "You do not have a valid membership for this class". OR "Status": "Unavailable", "Message": "The class is full". If valid, it will return the ClassSlot with new attributes e.g. "Status": "Available", "Message": "".
def checkClassSlotAvailability(classSlotList: list, userId: int):
    # Master List to store the ClassSlot objects with the new attributes, which will be returned at the end of the function
    masterList = []

    # Loop through the list of class slots
    for classSlot in classSlotList:
        # Create a new dictionary to store the new attributes
        newDict = {}

        # Check if the class slot's current capacity is less than the class's maximum capacity
        selectedClass = Class.query.filter_by(ClassId=classSlot.ClassId).first()

        if classSlot.CurrentCapacity < selectedClass.MaximumCapacity:
            # Check if the User has a valid membership for the selected class
            # First, using the selectedClass, search the MembershipClassMapping table to get a list of MembershipTypeId that allows the user to book the selected class
            membershipClassMappingList = MembershipClassMapping.query.filter_by(ClassId=selectedClass.ClassId).all()

            # Extract all of the MembershipTypeIds from the membershipClassMappingList
            membershipTypeIdList = [m.MembershipTypeId for m in membershipClassMappingList]

            # Next, using the userId, get the MembershipRecord that belongs to the user using these search criterias:
            # ActiveStatus must be "Active" or "Pending Payment"
            # MembershipTypeId must be in the list of MembershipTypeId (membershipTypeIdList) that allows the user to book the selected class

            membershipRecord = MembershipRecord.query.filter_by(UserId=userId).filter(MembershipRecord.ActiveStatus.in_(["Active", "Pending Payment"])).filter(MembershipRecord.MembershipTypeId.in_(membershipTypeIdList)).first()

            # If there are no such membership records, save the Status and Message in the newDict and append the newDict to the masterList
            if not membershipRecord:
                newDict["Status"] = "Unavailable"
                newDict["Message"] = "You do not have a valid membership for this class"
                newDict["ClassSlot"] = classSlot.jsonWithClass()
                masterList.append(newDict)
            else:
                # If there is a valid membership record, check if the User already has an existing active booking for the selected class slot. We use the MembershipRecordId and ClassSlotId to check for this
                existingBooking = Booking.query.filter_by(UserId=userId).filter_by(ClassSlotId=classSlot.ClassSlotId).filter_by(Status="Confirmed").first()

                if existingBooking:
                    newDict["Status"] = "Unavailable"
                    newDict["Message"] = "You already have an existing active booking for the selected class slot"
                    newDict["ClassSlot"] = classSlot.jsonWithClass()
                    masterList.append(newDict)
                else:
                    # If there is no existing booking, check if the User has enough points to make a booking for this Class Slot
                    # Using the class slot's StartTime, we retrive the corresponding Points row from the Points table in which the class slot's StartTime is between the PointsStartDate and PointsEndDate. The Points row should also match the MembershipRecordId being used above
                    selectedPoints = Points.query.filter(Points.PointsStartDate <= classSlot.StartTime).filter(Points.PointsEndDate >= classSlot.StartTime).filter_by(MembershipRecordId=membershipRecord.MembershipRecordId).first()

                    # If the selectedPoints is not found, return 406
                    if not selectedPoints:
                        newDict["Status"] = "Unavailable"
                        newDict["Message"] = "There are no valid points record for the selected class slot to make the booking"
                        newDict["ClassSlot"] = classSlot.jsonWithClass()
                        masterList.append(newDict)
                    else:
                        # If selectedPoints is found, check that the Balance is more than 0. If it is, we can proceed to create the booking and deduct one point from this selectedPoints Balance
                        if selectedPoints.Balance > 0:
                            newDict["Status"] = "Available"
                            newDict["Message"] = ""
                            newDict["ClassSlot"] = classSlot.jsonWithClass()
                            masterList.append(newDict)
                        else:
                            newDict["Status"] = "Unavailable"
                            newDict["Message"] = "You do not have enough points to make the booking"
                            newDict["ClassSlot"] = classSlot.jsonWithClass()
                            masterList.append(newDict)
        else:
            newDict["Status"] = "Unavailable"
            newDict["Message"] = "The class is full"
            newDict["ClassSlot"] = classSlot.jsonWithClass()
            masterList.append(newDict)

    return masterList

# Function and Route to get Class Slots by Date and User ID
@app.route("/classSlot/slots/<string:date>/user/<int:id>")
def getClassSlotByDateAndUserID(date: str, id: int):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # If given date is more than 2 weeks from today, return 406
    if date > (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"):
        return "You can only view class slots up to 2 weeks from today", 406

    # Get the current DateTime
    now = datetime.now()
    print(now)

    # Get all Class Slots from DB that match the given date, and is after the current date and time (now)
    classSlotList = ClassSlot.query.filter(ClassSlot.StartTime.between(date + ' 00:00:00', date + ' 23:59:59')).filter(ClassSlot.StartTime >= now.strftime("%Y-%m-%d %H:%M:%S")).order_by(ClassSlot.StartTime).all()

    if len(classSlotList):
        # Call the checkClassSlotAvailability function to get the list of class slots with the new attributes
        masterList = checkClassSlotAvailability(classSlotList, id)
        
        return jsonify(
            masterList
        ), 200
    return "There are no class slots on this date", 406
