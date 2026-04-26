import requests
import json
import random
categories=requests.get("https://api.chucknorris.io/jokes/categories").json()
print(categories)

random_category=random.choice(categories)
print(f"Random category: {random_category}")
joke=requests.get(f"https://api.chucknorris.io/jokes/random?category={random_category}").json()
print(f"Joke: {joke['value']}")