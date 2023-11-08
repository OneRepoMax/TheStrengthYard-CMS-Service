from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import text
import requests, json
from os import environ
from app.auth import get_access_token
from app.models import Memberships, MembershipRecord, MembershipLog, User, MembershipClassMapping, Class, Booking, ClassSlot
from app.token import admin_protected

# ANALYTICS ROUTES START HERE

# Function and Route to get total count of users in TSY DB
@app.route("/analytics/totalusers", methods=['GET'])
@admin_protected
def getTotalUsers(current_user):
    try:
        totalUsers = User.query.count()
        return jsonify(totalUsers), 200
    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of users. " + str(e)
        ), 404
    
# Function and Route to get total number of users in TSY DB with different classifications
@app.route("/analytics/userbreakdown", methods=['GET'])
@admin_protected
def getTotalUsersWithMembership(current_user):
    # The final outcome should be a list of dictionaries, with each dictionary containing the following, e.g.:
    # ["Total Users in DB": 33, "Total Users with an Active Membership Record": 22, "Total Users without any Membership Record": 11, "Total Users with 'Pending Payment' Membership Records": 2, "Total Users with 'Expired' Membership Records": 3, "Total Users with 'Terminated' Membership Records": 17]

    try:
        totalUsers = User.query.count()
        
        # Get total number of users with an active membership record
        totalUsersWithMembership = User.query.join(MembershipRecord).filter(MembershipRecord.ActiveStatus == "Active").count()

        # Get the total number of Membership Records in DB
        totalMembershipRecords = MembershipRecord.query.count()

        # Get total number of users without any membership record
        totalUsersWithoutMembership = User.query.filter(User.UserId.notin_(db.session.query(MembershipRecord.UserId))).count()

        # Get total number of users with a pending payment membership record
        totalUsersWithPendingPayment = User.query.join(MembershipRecord).filter(MembershipRecord.ActiveStatus == "Pending Payment").count()

        # Get total number of users with an expired membership record
        totalUsersWithExpiredMembership = User.query.join(MembershipRecord).filter(MembershipRecord.ActiveStatus == "Expired").count()

        # Get total number of users with an Paused membership record
        totalUsersWithPausedMembership = User.query.join(MembershipRecord).filter(MembershipRecord.ActiveStatus == "Paused").count()

        # Get total number of users with a terminated membership record
        totalUsersWithTerminatedMembership = User.query.join(MembershipRecord).filter(MembershipRecord.ActiveStatus == "Terminated").count()

        return jsonify(
            {
                "Total Users in DB": totalUsers,
                "Total Number of Membership Records in DB": totalMembershipRecords,
                "Total Users with an 'Active' Membership Record": totalUsersWithMembership,
                "Total Users without any Membership Record": totalUsersWithoutMembership,
                "Total Users with 'Pending Payment' Membership Records": totalUsersWithPendingPayment,
                "Total Users with 'Paused' Membership Records": totalUsersWithPausedMembership,
                "Total Users with 'Expired' Membership Records": totalUsersWithExpiredMembership,
                "Total Users with 'Terminated' Membership Records": totalUsersWithTerminatedMembership
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "error": True,
                "message": "An error occurred while retrieving the total number of users with a membership. " + str(e)
            }
        ), 404

# Function and Route to get total number of new Membership Records created in this current month
@app.route("/analytics/newmemberships/thismonth", methods=['GET'])
@admin_protected
def getTotalNewMembershipsThisMonth(current_user):
    try:
        # Get the current month
        currentMonth = datetime.now().month

        # Get the current year
        currentYear = datetime.now().year

        # Get the total number of new Membership Records created in this current month
        totalNewMembershipsThisMonth = MembershipRecord.query.filter(db.func.month(MembershipRecord.StartDate) == currentMonth, db.func.year(MembershipRecord.StartDate) == currentYear).count()

        return jsonify(totalNewMembershipsThisMonth), 200
    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of new Membership Records created in this current month. " + str(e)
        ), 404

# Function and Route to check for each Class, the total number of bookings made for each Class in this current month
@app.route("/analytics/totalbookings", methods=['GET'])
@admin_protected
def getTotalNumberOfBookingsForEachClassInCurrentMonth(current_user):
    try:
        # Get the current month
        currentMonth = datetime.now().month

        # Get the current year
        currentYear = datetime.now().year

        # Get all the Classes
        allClasses = Class.query.all()

        # Create a list to store the total number of bookings for each Class.
        # Final outcome in this list should be a list of dictionaries, with each dictionary containing the following, e.g.:
        # ["Progressive Strength Class": 22, "Olympic Barbell Class": 11, "Open Gym": 2, "Gymnastics Class": 3, "Conditioning Class": 17, "Total": 55]"]
        totalNumberOfBookingsForEachClass = []

        # Loop through each Class
        for selectedClass in allClasses:
            # Get the total number of bookings for this Class
            classAndTotalNumberOfBookings = getTotalNumberOfBookingsForClass(selectedClass.ClassId, currentMonth, currentYear)

            # Append the total number of bookings for this Class into the list
            totalNumberOfBookingsForEachClass.append(classAndTotalNumberOfBookings)

        # Create a dictionary to store the total number of bookings for all Classes
        totalNumberOfBookingsForAllClasses = {
            "Total": 0
        }

        # Loop through each Class, and add the total number of bookings for each Class into the totalNumberOfBookingsForAllClasses dictionary
        for selectedClass in totalNumberOfBookingsForEachClass:
            for className, totalNumberOfBookings in selectedClass.items():
                totalNumberOfBookingsForAllClasses["Total"] += totalNumberOfBookings
                totalNumberOfBookingsForAllClasses[className] = totalNumberOfBookings

        return jsonify(totalNumberOfBookingsForAllClasses), 200
    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of bookings for each Class. " + str(e)
        ), 404
            

# Helper function to get the total number of bookings for each Class
# Input: ClassId, currentMonth, currentYear
# Output: "ClassName": totalNumberOfBookingsForClass
def getTotalNumberOfBookingsForClass(ClassId: int, currentMonth: int, currentYear: int):
    try:
        # Get all the ClassSlots for this given ClassId that are in this current month and year
        allClassSlotsForThisClass = ClassSlot.query.filter(ClassSlot.ClassId == ClassId, db.func.month(ClassSlot.StartTime) == currentMonth, db.func.year(ClassSlot.StartTime) == currentYear).all()

        # Create a variable to store the total number of bookings for each ClassSlot
        totalNumberOfBookingsForClass = 0

        # Loop through each ClassSlot, and check the total number of bookings for each ClassSlot. The Booking 'Status' must also be 'Confirmed'. Add them to the totalNumberOfBookingsForClass variable
        for selectedClassSlot in allClassSlotsForThisClass:
            totalNumberOfBookingsForClass += Booking.query.filter(Booking.ClassSlotId == selectedClassSlot.ClassSlotId, Booking.Status == "Confirmed").count()

        # Get the Class Name
        className = Class.query.filter(Class.ClassId == ClassId).first().ClassName

        # Create a dictionary to store the Class Name and the total number of bookings for this Class
        classAndTotalNumberOfBookings = {
            className: totalNumberOfBookingsForClass
        }

        return classAndTotalNumberOfBookings
    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of bookings for this Class. " + str(e)
        ), 404

# Function and Route to get User Demographics statistics e.g. Age Group and Gender
@app.route("/analytics/userdemographics", methods=['GET'])
@admin_protected
def getUserDemographics(current_user):
    try:
        # Get all the Users
        allUsers = User.query.all()

        # Create a dictionary with key value pairs to store the total number of users for each Age Group
        totalNumberOfUsersForEachAgeGroup = {
            "17 and below": 0,
            "18-24": 0,
            "25-34": 0,
            "35-44": 0,
            "45-54": 0,
            "55-64": 0,
            "65-74": 0,
            "75+": 0
        }

        # Create a dictionary with key value pairs to store the Gender breakdown
        genderBreakdown = {
            "Male": 0,
            "Female": 0,
            "Others": 0
        }
        
        # Loop through the allUsers list and derive the age from the DateOfBirth for each User. Then, add the count into the respective Age Group. Also, check the Gender and add the count in the respective gender
        for selectedUser in allUsers:
            if selectedUser.DateOfBirth != None:
                # Calculate the age of this User
                userAge = datetime.now().year - selectedUser.DateOfBirth.year

                # Check the age of this User and add the count into the respective Age Group
                if userAge <= 17:
                    totalNumberOfUsersForEachAgeGroup["17 and below"] += 1
                elif userAge >= 18 and userAge <= 24:
                    totalNumberOfUsersForEachAgeGroup["18-24"] += 1
                elif userAge >= 25 and userAge <= 34:
                    totalNumberOfUsersForEachAgeGroup["25-34"] += 1
                elif userAge >= 35 and userAge <= 44:
                    totalNumberOfUsersForEachAgeGroup["35-44"] += 1
                elif userAge >= 45 and userAge <= 54:
                    totalNumberOfUsersForEachAgeGroup["45-54"] += 1
                elif userAge >= 55 and userAge <= 64:
                    totalNumberOfUsersForEachAgeGroup["55-64"] += 1
                elif userAge >= 65 and userAge <= 74:
                    totalNumberOfUsersForEachAgeGroup["65-74"] += 1
                elif userAge >= 75:
                    totalNumberOfUsersForEachAgeGroup["75+"] += 1
            
            if selectedUser.Gender == "M":
                genderBreakdown["Male"] += 1
            elif selectedUser.Gender == "F":
                genderBreakdown["Female"] += 1
            else:
                genderBreakdown["Others"] += 1
        
        print(totalNumberOfUsersForEachAgeGroup)
        print(genderBreakdown)
        return jsonify(
            {
                "Age Demographics": totalNumberOfUsersForEachAgeGroup,
                "Gender Demographics": genderBreakdown
            }
        ), 200
    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the User Demographics. " + str(e)
        ), 404
    
## Returns unique bookings for the current month
@app.route("/analytics/uniquemonthlybookings", methods=['GET'])
@admin_protected
def monthlyBookings(current_user):
    try:
        # Get the current month
        currentMonth = datetime.now().month

        # Get the current year
        currentYear = datetime.now().year

        stmt = text("SELECT count(distinct(UserId)) as 'UniqueClients' FROM tsy_db.Booking where month(BookingDateTime) = :month and year(BookingDateTime) = :year and Status = 'Confirmed';")
        stmt = stmt.bindparams(month=currentMonth, year=currentYear)
        uniqueBookings = db.session.execute(stmt).fetchone()
        db.session.close()
        return jsonify(
            {
                "Unique Bookings this month": uniqueBookings[0]
            }), 200

    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of unique bookings for this month. " + str(e)
        ), 404
        
## Returns unique bookings for the current month
@app.route("/analytics/peakTimings/<int:classId>", methods=['GET'])
@admin_protected
def peakTimings(current_user, classId):
    try:
        # Get the current month
        currentMonth = datetime.now().month

        # Get the current year
        currentYear = datetime.now().year

        stmt = text("SELECT day, hour(StartTime) as 'StartTime', sum(CurrentCapacity) as 'Bookings_This_Month' FROM tsy_db.ClassSlot where month(StartTime) = :month and year(StartTime) = :year and ClassId = :classId group by day, hour(StartTime) order by time(StartTime) desc")
        stmt = stmt.bindparams(month=currentMonth, year=currentYear, classId=classId)
        timeSlots = db.session.execute(stmt).fetchall()
        db.session.close()
        formattedTimeSlots = []
        for row in timeSlots:
            formattedTimeSlots.append({
                "day": row[0],
                "hour": row[1],
                "Bookings_This_Month": row[2]
            })

        return jsonify({"Time Slots": formattedTimeSlots}), 200

    except Exception as e:
        return jsonify(
            "An error occurred while retrieving the total number of unique bookings for this month. " + str(e)
        ), 404


