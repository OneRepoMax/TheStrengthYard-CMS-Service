import pytz

# Format the dates in GMT+8 (Asia/Singapore) time zone
def sg_tz_dateformat(date):
    singapore_timezone = pytz.timezone('Asia/Singapore')
    return date.astimezone(singapore_timezone).strftime("%a, %d %b %Y %H:%M:%S %Z")