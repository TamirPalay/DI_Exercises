import datetime

def getTodayDate():
    today = datetime.datetime.today()
    return today
today=getTodayDate()
print("Today's date:", today)
newYears = datetime.datetime(2027, 1, 1)

daysToNewYears = newYears - today
print("Days to New Year's:", daysToNewYears.days)

def calculateMinutesAlive(birthdate):
    today=getTodayDate()
    age = today - birthdate
    return age.total_seconds() / 60

birthdate = datetime.datetime(2001, 12, 2)
minutesAlive = calculateMinutesAlive(birthdate)
print("Minutes alive:", minutesAlive)