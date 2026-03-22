'''
Exercise 4 : How many characters in a sentence ?
Instructions
Use python to find out how many characters are in the following text, use a single line of code (beyond the establishment of your my_text variable).
'''
my_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
print(len(my_text))

'''
Exercise 5: Longest word without a specific character
Instructions
Keep asking the user to input the longest sentence they can without the character “A”.
Each time a user successfully sets a new longest sentence, print a congratulations message.
'''
current_longest = ""
while True:
    sentence = input("Please enter a sentence without the character 'A': ")
    if 'A' in sentence or 'a' in sentence:
        print("Sorry, your sentence contains the character 'A'. Please try again.")
        break
    elif len(sentence) > len(current_longest):
        current_longest = sentence
        print("Congratulations! You have set a new longest sentence without the character 'A'!")
    else:
        print("Your sentence is valid but not longer than the current longest. Try again!")