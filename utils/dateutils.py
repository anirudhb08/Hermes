from datetime import datetime, timedelta
import pytz
ist = pytz.timezone("Asia/Kolkata")

def get_days_close_timestamp(no_of_days):
    d = datetime.now(ist) - timedelta(days = no_of_days)
    d = d.replace(hour = 15, minute = 30, second = 0, microsecond = 0)
    return int(d.timestamp())

def get_days_open_timestamp(no_of_days):
    d = datetime.now(ist) - timedelta(days = no_of_days)
    d = d.replace(hour = 9, minute = 15, second = 0, microsecond = 0)
    return int(d.timestamp())


def get_minutes_timestamp(no_of_minutes):
    d = datetime.now(ist).replace(hour = 10, minute = 38)
    start = d.replace(hour = 9, minute = 15, second = 0, microsecond = 0)
    end = d.replace(hour = 15, minute = 30, second = 0, microsecond = 0)
    
    if int(d.timestamp()) > int(end.timestamp()):
        ans = start + timedelta(days = 1)
        return int(ans.timestamp())
    elif int(d.timestamp()) < int(start.timestamp()):
        return int(start.timestamp())
    else:
        diff = int(d.timestamp()) - int(start.timestamp())
        diff = diff % (no_of_minutes * 60)
        return int(d.timestamp()) - diff