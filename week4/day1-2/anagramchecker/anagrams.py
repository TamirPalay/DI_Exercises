import anagram_checker as ac
def show_user_menu(ac):
    while True:
        print("1. Input a word and find its anagrams")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            word = input("Enter a word: ")
            word=word.upper()
            if validate_word(word):
                if ac.is_valid_word(word):
                    print(f"{word} is a valid word.")
                    anagrams = ac.get_anagrams(word)
                    print(f"Anagrams for '{word}': {anagrams}")

        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again. Enter 1 to find anagrams or 2 to exit.")

def validate_word(word):
    word = word.strip()
    if ' ' in word:
        print("Error: Only a single word is allowed.")
        return False
    if not word.isalpha():
        print("Error: Only alphabetic characters are allowed.")
        return False
    return True

ac = ac.AnagramChecker()
show_user_menu(ac)