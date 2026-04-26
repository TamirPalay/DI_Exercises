import json
import random


with open("week3\\day5-6\\classexercise\\file.json", 'r') as file:
    family = json.load(file)
    for child in family["children"]:
        print(f"{child['firstName']} is {child['age']} years old.")
        child["favorite_color"] = random.choice(["red", "blue", "green", "yellow",      "purple"])  

with open("week3\\day5-6\\classexercise\\file.json", 'w') as file:
    json.dump(family, file, indent=2)