'''
🌟 Exercise 1: Favorite Numbers
Key Python Topics:
Sets
Adding/removing items in a set
Set concatenation (using union)
Instructions:
Create a set called my_fav_numbers and populate it with your favorite numbers.
Add two new numbers to the set.
Remove the last number you added to the set.
Create another set called friend_fav_numbers and populate it with your friend’s favorite numbers.
Concatenate my_fav_numbers and friend_fav_numbers to create a new set called our_fav_numbers.
Note: Sets are unordered collections, so ensure no duplicate numbers are added.
'''
myfav_numbers = {3, 7, 9}
myfav_numbers.add(11)
myfav_numbers.add(13)
myfav_numbers.remove(13)
friend_fav_numbers = {2, 4, 6}
our_fav_numbers = myfav_numbers.union(friend_fav_numbers)
'''
🌟 Exercise 2: Tuple
Key Python Topics:
Tuples (immutability)
Instructions:
Given a tuple of integers, try to add more integers to the tuple.
Hint: Tuples are immutable, meaning they cannot be changed after creation. Think about why you can’t add more integers to a tuple.
'''
my_tuple = (1, 2, 3)
# my_tuple.append(4)  # This will raise an AttributeError because tuples do not have an append method.
'''
🌟 Exercise 3: List Manipulation
Key Python Topics:
Lists
List methods: append, remove, insert, count, clear
Instructions:
You have a list: basket = ["Banana", "Apples", "Oranges", "Blueberries"]
Remove "Banana" from the list.
Remove "Blueberries" from the list.
Add "Kiwi" to the end of the list.
Add "Apples" to the beginning of the list.
Count how many times "Apples" appear in the list.
Empty the list.
Print the final state of the list.
'''
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")
apples_count = basket.count("Apples")
basket.clear()
print(basket)
'''

🌟 Exercise 4: Floats
Key Python Topics:
Lists
Floats and integers
Range generation
Instructions:
Recap: What is a float? What’s the difference between a float and an integer?
Create a list containing the following sequence of mixed types: floats and integers:
1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.
Avoid hard-coding each number manually.
Think: Can you generate this sequence using a loop or another method?
'''
my_list = [1.5 + 0.5 * i for i in range(8)]
print(my_list)
'''
🌟 Exercise 5: For Loop
Key Python Topics:
Loops (for)
Range and indexing
Instructions:
Write a for loop to print all numbers from 1 to 20, inclusive.
Write another for loop that prints every number from 1 to 20 where the index is even.
'''
for i in range(1, 21):
    print(i)
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
'''
🌟 Exercise 6: While Loop
Key Python Topics:
Loops (while)
Conditionals
Instructions:
Use an input to ask the user to enter their name.
Using a while True loop, check if the user gave a proper name (not digits and at least 3 letters long)
hint: check for the method isdigit()
if the input is incorrect, keep asking for the correct input until it is correct
if the input is correct print “thank you” and break the loop
Example:
Alt text
'''
while True:
    name = input("Please enter your name: ")
    if any(char.isdigit() for char in name) or len(name) < 3:
        print("Invalid input. Please enter a proper name.")
    else:
        print("Thank you!")
        break
'''
🌟 Exercise 7: Favorite Fruits
Key Python Topics:
Input/output
Strings and lists
Conditionals
Instructions:
Ask the user to input their favorite fruits (they can input several fruits, separated by spaces).
Store these fruits in a list.
Ask the user to input the name of any fruit.
If the fruit is in their list of favorite fruits, print:
"You chose one of your favorite fruits! Enjoy!"
If not, print:
"You chose a new fruit. I hope you enjoy it!"
'''
favorite_fruits = input("Please enter your favorite fruits, separated by spaces: ").split()
fruit= input("Please enter the name of any fruit: ")
if fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")
'''
🌟 Exercise 8: Pizza Toppings
Key Python Topics:
Loops
Lists
String formatting
Instructions:
Write a loop that asks the user to enter pizza toppings one by one.
Stop the loop when the user types 'quit'.
For each topping entered, print:
"Adding [topping] to your pizza."
After exiting the loop, print all the toppings and the total cost of the pizza.
The base price is $10, and each topping adds $2.50.
'''
toppings = []
while True:
    topping = input("Enter a pizza topping (or 'quit' to finish): ")
    if topping == 'quit':
        break
    print(f"Adding {topping} to your pizza.")
    toppings.append(topping)

print("Your pizza toppings:")
for t in toppings:
    print(f"- {t}")

total_cost = 10 + len(toppings) * 2.50
print(f"Total cost: ${total_cost:.2f}")

'''

🌟 Exercise 9: Cinemax Tickets
Key Python Topics:
Conditionals
Lists
Loops
Instructions:
Ask for the age of each person in a family who wants to buy a movie ticket.
Calculate the total cost based on the following rules:
Free for people under 3.
$10 for people aged 3 to 12.
$15 for anyone over 12.
Print the total ticket cost.
'''
total_cost = 0
while True:
    age_input = input("Enter the age of a family member (or 'done' to finish): ")
    if age_input.lower() == 'done':
        break
    try:
        age = int(age_input)
        if age < 3:
            cost = 0
        elif 3 <= age <= 12:
            cost = 10
        else:
            cost = 15
        total_cost += cost
    except ValueError:
        print("Please enter a valid age or 'done' to finish.")
print(f"Total ticket cost: ${total_cost}")

'''
Bonus:

Imagine a group of teenagers wants to see a restricted movie (only for ages 16–21).
Write a program to:
Ask for each person’s age.
Remove anyone who isn’t allowed to watch.
Print the final list of attendees.'''
while True:
    age_input = input("Enter the age of a teenager (or 'done' to finish): ")
    if age_input.lower() == 'done':
        break
    try:
        age = int(age_input)
        if 16 <= age <= 21:
            print("This person can attend the movie.")
        else:
            print("This person cannot attend the movie.")
    except ValueError:
        print("Please enter a valid age or 'done' to finish.")
    
