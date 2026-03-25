'''
Reverse the Sentence
Write a program to reverse the sentence wordwise.

Input:
You have entered a wrong domain
Output:
domain wrong a entered have You'''
initial_sentence = input("Please enter a sentence: ")
reversed_sentence = ' '.join(initial_sentence.split()[::-1])
print(reversed_sentence)
