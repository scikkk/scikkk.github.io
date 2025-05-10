import datetime

def convert_timestamp_to_datetime(timestamp):
    timestamp_in_seconds = timestamp / 1000.0
    dt = datetime.datetime.fromtimestamp(timestamp_in_seconds)
    return dt