import pytz

def local_to_utc(dt, tz_name):
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    return local_dt.astimezone(pytz.UTC)