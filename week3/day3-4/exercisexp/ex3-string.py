import random
import string

allLetters = string.ascii_letters
print(allLetters)

newWord=''
for i in range(5):
    newWord += random.choice(allLetters)
print(newWord)