def display_message():
    print ("I am learning about functions in Python.")
display_message()

#Exercise 2: Favorite Book
def favorite_book(title):
    print(f"One of my favorite books is {title}.")
favorite_book("Alice in Wonderland")

#Exercise 3: Geography
def describe_city(city, country="Unknown"):
    print(f"{city} is in {country}.")
describe_city("Paris")
describe_city("Reykjavik", "Iceland")

#Exercise 4: Random
import random
def compare_numbers(num):
    random_num = random.randint(1, 100)
    print(f"Your number: {num}")
    print(f"Random number: {random_num}")
    if num == random_num:
        print("The numbers are the same!")
    else:
        print("Your number is different from the random number.")

compare_numbers(42)

#Exercise 5: Personalized Tshirts
def make_shirt(size="Large", text="I love Python"):
    print(f"The shirt size is {size} and it has the text '{text}' printed on it.")
make_shirt()
make_shirt(size="Medium")
make_shirt(size="Small", text="I like trains!")
make_shirt(size="Small", text="Elephants are awesome!")

#Exercise 6: Magicians
magician_names=['Harry Houdini', 'David Blaine', 'Criss Angel']
def show_magicians(magicians):
    for magician in magicians:
        print(magician)
show_magicians(magician_names)

def make_great(magicians):
    for i in range(len(magicians)):
        magicians[i] = "The Great " + magicians[i]
make_great(magician_names)
show_magicians(magician_names)

#Exercise 7: Temperature Advice
def get_random_temp():
    return random.uniform(-10, 40)
def main():
    temp=get_random_temp()
    print(f"The temperature right now is {temp} degrees Celsius.")
    if temp < 0:
        print("Brrr, that's freezing! Wear some extra layers today.")
    elif temp < 16:
        print("Quite chilly! Don't forget your coat.")
    elif temp < 23:
        print("Nice weather")
    elif temp < 32:
        print("A bit warm,stay hydrated.")
    elif temp <= 40:
        print("It’s really hot! Stay cool.")
    #Season
    season=input("Enter the month (1-12):  ")
    if season in ['12', '1', '2']:
        print("It's winter! Time for hot chocolate.")
    elif season in ['3', '4', '5']:
        print("It's spring! Flowers are blooming.")
    elif season in ['6', '7', '8']:
        print("It's summer! Time for the beach.")
    elif season in ['9', '10', '11']:
        print("It's autumn! Leaves are falling.")

main()
 

    
