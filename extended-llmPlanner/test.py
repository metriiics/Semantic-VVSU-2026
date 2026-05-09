import datetime

tz = datetime.datetime.now().astimezone().tzinfo

print(tz)