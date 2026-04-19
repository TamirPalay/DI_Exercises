#Exercise 1
import datetime
import holidays
from sqlalchemy import values

def getTodayDate():
    today = datetime.date.today()
    return today

today=getTodayDate()
days=holidays.Israel(years=today.year,language="en_US" )
nextholiday=days.get_closest_holiday(today)

print("Next holiday:", nextholiday[1], "on", nextholiday[0])
timeToNextHoliday = nextholiday[0] - today
print("Time to next holiday:", timeToNextHoliday.days, "days")

'''Exercise 2 : How Old Are You On Jupiter?
Instructions
Given an age in seconds, calculate how old someone would be on all those planets :

Earth: orbital period 365.25 Earth days, or 31557600 seconds
Example : if someone is 1,000,000,000 seconds old, the function should output that they are 31.69 Earth-years old.
Mercury: orbital period 0.2408467 Earth years
Venus: orbital period 0.61519726 Earth years
Mars: orbital period 1.8808158 Earth years
Jupiter: orbital period 11.862615 Earth years
Saturn: orbital period 29.447498 Earth years
Uranus: orbital period 84.016846 Earth years
Neptune: orbital period 164.79132 Earth years'''
def age_on_planet(seconds, planet):
    earth_years = seconds / 31557600
    if planet == "Mercury":
        return earth_years / 0.2408467
    elif planet == "Venus":
        return earth_years / 0.61519726
    elif planet == "Mars":
        return earth_years / 1.8808158
    elif planet == "Jupiter":
        return earth_years / 11.862615
    elif planet == "Saturn":
        return earth_years / 29.447498
    elif planet == "Uranus":
        return earth_years / 84.016846
    elif planet == "Neptune":
        return earth_years / 164.79132
    else:
        return None