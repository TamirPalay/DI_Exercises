'''
Instructions
Ask the user for their birthdate (specify the format, for example: DD/MM/YYYY).
Display a little cake as seen below:
       ___iiiii___
      |:H:a:p:p:y:|
    __|___________|__
   |^^^^^^^^^^^^^^^^^|
   |:B:i:r:t:h:d:a:y:|
   |                 |
   ~~~~~~~~~~~~~~~~~~~

The number of candles on the cake should be the last number of the users age, if they are 53, then add 3 candles.

Bonus : If they were born on a leap year, display two cakes !'''
birthdate = input("Please enter your birthdate (DD/MM/YYYY): ")
day, month, year = map(int, birthdate.split('/'))
from datetime import datetime
current_year = datetime.now().year  
age = current_year - year
candles = age % 10
cake = f"       ___{'i' * candles}___\n      |:H:a:p:p:y:|\n    __|___________|__\n   |^^^^^^^^^^^^^^^^^|\n   |:B:i:r:t:h:d:a:y:|\n   |                 |\n   ~~~~~~~~~~~~~~~~~~~"
print(cake)
if (year % 4 == 0 and year % 100 != 0) or(year % 400 == 0):
    print("\nIt's a leap year! Here's another cake for you:\n")
    print(cake)

