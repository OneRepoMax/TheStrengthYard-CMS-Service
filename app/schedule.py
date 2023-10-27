from app import app, db
from flask import jsonify, request, url_for, render_template
from datetime import datetime
from app.models import Schedule
from app.token import token_required

# Function and Route for getting All Schedule in the DB
@app.route("/schedule")
@token_required
def getAllSchedule(current_user):
    scheduleList = Schedule.query.all()
    
    return jsonify([schedule.jsonWithUser() for schedule in scheduleList]), 200
    

# Function and Route for getting a Schedule by ID
@app.route("/schedule/<int:id>")
@token_required
def getScheduleByID(current_user, id: int):
    scheduleList = Schedule.query.filter_by(ScheduleId=id).all()
    if len(scheduleList):
        return jsonify([schedule.jsonWithUser() for schedule in scheduleList]), 200

    return "There are no such schedule with ID: " + str(id), 406

# Function and Route to create a new schedule
@app.route("/schedule", methods=['POST'])
@token_required
def createSchedule(current_user):
    """
    Sample Request
    {
        "UserId": 2,
        "Description": "Updated Schedule for Progressive Strength Class August 2023",
        "ImgUrl": "sample.jpg"
    }
    """
    
    data = request.get_json()

    try:

        # Add Published Date to data and set to now
        data["PublishDate"] = datetime.now()
        
        schedule = Schedule(**data)

        db.session.add(schedule)
        db.session.commit()

        return jsonify(schedule.jsonWithUser()), 200

    except Exception as e:
        db.session.rollback()
        return "An error occurred while creating the new User. " + str(e), 406

#Function and Route to update a schedule
@app.route("/schedule/<int:id>", methods=['PUT'])
@token_required
def updateSchedule(current_user):
     
    """
    Sample Request
    {
        "ScheduleID": 1,
        "UserId": 2,
        "PublishDate": "1945-01-01",
        "Description": "Updated Schedule for Progressive Strength Class August 2023",
        "ImgUrl": "sample.jpg"
    }
    """
     
    data = request.get_json()

    try:
        
        schedule = Schedule.query.filter_by(ScheduleId=data["ScheduleId"]).first()
        if schedule:
            schedule.UserId = data["UserId"]
            schedule.PublishDate = data["PublishDate"]
            schedule.Description = data["Description"]
            schedule.ImgUrl = data["ImgUrl"]
            
            db.session.add(schedule)
            db.session.commit()

            return jsonify(schedule.jsonWithUser()), 200

        return "Schedule with ID: " + str(data["ScheduleId"]) + " not found.", 404
    
    except Exception as e:
        db.session.rollback()
        return "An error occurred while updating the Schedule. " + str(e), 406
    
# Function and Route to delete a schedule
@app.route("/schedule/<int:id>", methods=['DELETE'])
@token_required
def deleteSchedule(current_user, id: int):
    schedule = Schedule.query.filter_by(ScheduleId=id).first()
    if schedule:
        db.session.delete(schedule)
        db.session.commit()

        return "Schedule with ID: " + str(id) + " was deleted.", 200

    return "Schedule with ID: " + str(id) + " not found.", 404


        

