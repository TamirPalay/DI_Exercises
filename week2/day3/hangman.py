'''
Instructions
The computer choose a random word and mark stars for each letter of each word.
Then the player will guess a letter.
If that letter is in the word(s) then the computer fills the letter in all the correct positions of the word.
If the letter isn’t in the word(s) then add a body part to the gallows (head, body, left arm, right arm, left leg, right leg).
The player will continue guessing letters until they can either solve the word(s) (or phrase) or all six body parts are on the gallows.
The player can’t guess the same letter twice.
'''
import random

wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']
word = random.choice(wordslist) 

guesses=0
word_filled=False
display_word = ['*' if char != ' ' else ' ' for char in word]
print("Welcome to Hangman! Your word has ", len(word), "letters.")
print(display_word)

while not word_filled and guesses < 6:
    guess = input("Please guess a letter: ")
    if guess in display_word:
        print("You already guessed that letter. Try again.")
        continue
    if guess in word:
        for i, char in enumerate(word):
            if char == guess:
                display_word[i] = guess
        print("Correct! Current word:", ''.join(display_word))
    else:
        guesses += 1
        print(f"Wrong! You have {6 - guesses} guesses left.")
    if '*' not in display_word:
        word_filled = True

if word_filled:
    print("Congratulations! You've guessed the word:", word)
else:
    print("Game over! The word was:", word)
