from app import app, db
from flask import jsonify, request
from datetime import datetime, timedelta
import requests, json
from app.models import MembershipRecord, Class, ClassSlot, Booking, User, Points

# Function and Route to Create a new Class
@app.route("/class", methods=['POST'])
def createClass():
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
def getAllClass():
    classList = Class.query.all()
    return jsonify([c.json() for c in classList]), 200

# Function and Route to get a Class by ID
@app.route("/class/<int:id>")
def getClassByID(id: int):
    classList = Class.query.filter_by(ClassId=id).all()
    if len(classList):
        return jsonify(
            [c.json() for c in classList]
        ), 200
    return "There are no such class with ID: " + str(id), 406

# Function and Route to update a Class by ID
@app.route("/class/<int:id>", methods=['PUT'])
def updateClassByID(id: int):
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

# Function and Route to delete a Class by ID
@app.route("/class/<int:id>", methods=['DELETE'])
def deleteClassByID(id: int):
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
def createClassSlotByClassID(id: int):
    """
    Sample Request
    {
        "Day": "Sunday",
        "StartTime": "09:00:00",
        "EndTime": "10:00:00",
        "RecurringUntil": "2023-12-31"
    }
    """
    data = request.get_json()
    # Get the current date and time
    now = datetime.now()

    # Get the day, start time, end time and recurring until from the request
    day = data.get("Day")
    startTime = data.get("StartTime")
    endTime = data.get("EndTime")
    recurringUntil = data.get("RecurringUntil")
    
    # Compute the duration in minutes (integer) by subtracting the given end time with the given start time
    duration = int(endTime[:2]) * 60 + int(endTime[3:5]) - int(startTime[:2]) * 60 - int(startTime[3:5])

    


    
