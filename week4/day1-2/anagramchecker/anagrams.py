import anagram_checker
def show_user_menu():
    while True:
        print("1. Input a word and find its anagrams")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            word = input("Enter a word: ")
            word=word.upper()
            if validate_word(word):
                ac = anagram_checker.AnagramChecker()
                if ac.is_valid_word(word):
                    print(f"{word} is a valid word.")
                    anagrams = ac.get_anagrams(word)
                    print(f"Anagrams for '{word}': {anagrams}\n")

        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again. Enter 1 to find anagrams or 2 to exit\n.")

def validate_word(word):
    word = word.strip()
    if ' ' in word:
        print("Error: Only a single word is allowed.\n")
        return False
    if not word.isalpha():
        print("Error: Only alphabetic characters are allowed.\n")
        return False
    return True


show_user_menu()