import time





def get_current_time_stamp():
    return int(time.time() * 1000)

def time_stamp2str(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts / 1000))

def time_str2stamp(time_str):
    return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")) * 1000)

# time_stamp = get_current_time_stamp()
# print("Current time stamp:", time_stamp)
time_stamp = time_str2stamp("2025-05-18 12:17:26")
print("Current time stamp:", time_stamp)
time_str = time_stamp2str(time_stamp)
print("Time stamp to string:", time_str)