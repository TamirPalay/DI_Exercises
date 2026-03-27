'''
Instructions
Here is a python code that generates a list of 20000 random numbers, called list_of_numbers, and a target number.

import random

list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]

target_number   = 3728


Copy this code, and create a program that finds, within list_of_numbers all the pairs of number that sum to the target number

For example

1000 and 2728 sums to the target_number 3728
1864 and 1864 sums to the target_number 3728'''
import random


list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]
print("Numbers generated")
target_number   = 3728
pairs = []
print("Finding pairs that sum to the target number...")
for i in range(len(list_of_numbers)):
    for j in range(i + 1, len(list_of_numbers)):
        if list_of_numbers[i] + list_of_numbers[j] == target_number:
            pairs.append((list_of_numbers[i], list_of_numbers[j]))

print(f"Found {len(pairs)} pairs that sum to {target_number}:")
if pairs:
    for pair in pairs:
        print(f"{pair[0]} and {pair[1]} sums to the target_number {target_number}")
