# Using this python script to schedule run refreshMembershipRecords in payments.py every day at 02:00 AM so that the membership records will be updated daily.

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
from app.payments import refreshMembershipRecords
import atexit

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Add job (return of the function is a json, so it will be printed in the console)
scheduler.add_job(
    func=refreshMembershipRecords,
    trigger=CronTrigger(hour=2, minute=0, second=0),
    id='refreshMembershipRecords',
    name='Refresh membership records every day at 02:00 AM',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Run the app
if __name__ == "__main__":
    app.run()

            