'''
Exercise 1: Formula
Instructions
Write a program that calculates and prints a value according to this given formula:
Q = Square root of [(2 * C * D)/H]
Following are the fixed values of C and H:
C is 50.
H is 30.
Ask the user for a comma-separated string of numbers, use each number from the user as D in the formula and return all the results
For example, if the user inputs: 100,150,180
The output should be:

18,22,24
'''
import math
C = 50
H = 30
user_input = input("Please enter a comma-separated string of numbers: ")
D_values = user_input.split(',')
results = []
for D in D_values:
    D = int(D)
    Q = math.sqrt((2 * C * D) / H)
    results.append(str(int(Q)))
print(','.join(results))
'''

Exercise 2 : List of integers
Instructions
Given a list of 10 integers to analyze. For example:

    [3, 47, 99, -80, 22, 97, 54, -23, 5, 7] 
    [44, 91, 8, 24, -6, 0, 56, 8, 100, 2] 
    [3, 21, 76, 53, 9, -82, -3, 49, 1, 76] 
    [18, 19, 2, 56, 33, 17, 41, -63, -82, 1]


1. Store the list of numbers in a variable.

2. Print the following information:
a. The list of numbers – printed in a single line
b. The list of numbers – sorted in descending order (largest to smallest)
c. The sum of all the numbers

3. A list containing the first and the last numbers.

4. A list of all the numbers greater than 50.

5. A list of all the numbers smaller than 10.

6. A list of all the numbers squared – eg. for [1, 2, 3] you would print “1 4 9”.

7. The numbers without any duplicates – also print how many numbers are in the new list.

8. The average of all the numbers.

9. The largest number.

10.The smallest number.

11. Bonus: Find the sum, average, largest and smallest number without using built in functions.

12. Bonus: Instead of using pre-defined lists of numbers, ask the user for 10 numbers between -100 and 100. Ask the user for an integer between -100 and 100 – repeat this question 10 times. Each number should be added into a variable that you created earlier.

13. Bonus: Instead of asking the user for 10 integers, generate 10 random integers yourself. Make sure that these random integers are between -100 and 100.

14. Bonus: Instead of always generating 10 integers, let the amount of integers also be random! Generate a random positive integer no smaller than 50.

15. Bonus: Will the code work when the number of random numbers is not equal to 10?
'''
numbers = [3, 47, 99, -80, 22, 97, 54, -23, 5, 7]
print("Original list:", numbers)
print("Sorted list (descending):", sorted(numbers, reverse=True))
print("Sum of numbers:", sum(numbers))
print("First and last numbers:", [numbers[0], numbers[-1]])
print("Numbers greater than 50:", [num for num in numbers if num > 50])
print("Numbers smaller than 10:", [num for num in numbers if num < 10])
print("Numbers squared:", [num ** 2 for num in numbers])
print("Unique numbers:", set(numbers), "Count:", len(set(numbers)))
print("Average:", sum(numbers) / len(numbers))
print("Largest number:", max(numbers))
print("Smallest number:", min(numbers))
'''


Exercise 3: Working on a paragraph
Find an interesting paragraph of text online. (Please keep it appropriate to the social context of our class.)
Paste it to your code, and store it in a variable.
Let’s analyze the paragraph. Print out a nicely formatted message saying:
How many characters it contains (this one is easy…).
How many sentences it contains.
How many words it contains.
How many unique words it contains.
Bonus: How many non-whitespace characters it contains.
Bonus: The average amount of words per sentence in the paragraph.
Bonus: the amount of non-unique words in the paragraph.
'''
paragraph = """Your interesting paragraph goes here. It can be about anything you like, as long as it's appropriate for our class. You can analyze the number of characters, sentences, words, and unique words in this paragraph."""
num_characters = len(paragraph)
num_sentences = paragraph.count('.') + paragraph.count('!') + paragraph.count('?')
num_words = len(paragraph.split())  
num_unique_words = len(set(paragraph.split()))
num_non_whitespace_characters = len(paragraph.replace(" ", ""))

print(f"Number of characters: {num_characters}")
print(f"Number of sentences: {num_sentences}")
print(f"Number of words: {num_words}")
print(f"Number of unique words: {num_unique_words}")
print(f"Number of non-whitespace characters: {num_non_whitespace_characters}")
average_words_per_sentence = num_words / num_sentences if num_sentences > 0 else 0
print(f"Average words per sentence: {average_words_per_sentence}")
num_non_unique_words = num_words - num_unique_words
print(f"Number of non-unique words: {num_non_unique_words}")
'''
Exercise 4 : Frequency Of The Words
Instructions
Write a program that prints the frequency of the words from the input.

Suppose the following input is supplied to the program:
New to Python or choosing between Python 2 and Python 3? Read Python 2 or Python 3.

Then, the output should be:

    2:2
    3.:1
    3?:1
    New:1
    Python:5
    Read:1
    and:1
    between:1
    choosing:1
    or:2
    to:1'''
sentence=input("Please enter a sentence: ")
word_list = sentence.split()
word_freq = {}
for word in word_list:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1
for word, freq in word_freq.items():
    print(f"{word}:{freq}")
