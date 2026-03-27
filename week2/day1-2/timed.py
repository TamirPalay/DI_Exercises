def count_letters(sentence, char):
    count = 0
    for letter in sentence:
        if letter == char:
            count += 1
    return count
sentence = input("Please enter a sentence: ")
char = input("Please enter a character to count: ")
letter_count = count_letters(sentence, char)
print(f"The character '{char}' appears {letter_count} times in the sentence.")