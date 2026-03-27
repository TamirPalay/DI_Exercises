'''
Exercise 1 : When will I retire ?
Instructions
The point of the exercise is to check if a person can retire depending on their age and their gender.
Note : Let’s say retirement age is 67 for men, and 62 for women (born after April, 1947).

Create a function get_age(year, month, day)
Hard-code the current year and month in your code (there are better ways of doing this, but for now it will be enough.)
After calculating the age of a person, the function should return the age (the age is an integer).
Create a function can_retire(gender, date_of_birth).
It should call the get_age function (with what arguments?) in order to receive an age.
Now it has all the information it needs in order to determine if the person with the given gender and date of birth is able to retire or not.
Calculate. You may need to do a little more hard-coding here.
Return True if the person can retire, and False if he/she can’t.
Some Hints

Ask for the user’s gender as “m” or “f”.
Ask for the user’s date of birth in the form of “yyyy/mm/dd”, eg. “1993/09/21”.
Call can_retire to get a definite value for whether the person can or can’t retire.
Display a message informing the user whether they can retire or not.
As always, test your code to ensure it works.'''
gender=input("Please enter your gender (m/f): ").strip().lower()
date_of_birth = input("Please enter your date of birth (yyyy/mm/dd): ").strip()
def get_age(year, month, day):
    # Hard-code the current year and month
    year_current = 2026
    month_current = 3
    age = year_current - year
    if month_current < month or (month_current == month and 1 < day):
        age -= 1
    return age
def can_retire(gender, date_of_birth):
    year, month, day = map(int, date_of_birth.split('/'))
    age = get_age(year, month, day)
    if gender == 'm':
        return age >= 67
    elif gender == 'f':
        return age >= 62
    else:
        return False
if can_retire(gender, date_of_birth):
    print("You can retire! You deserve it!")
else:
    print("You cannot retire yet. Keep working!")    
