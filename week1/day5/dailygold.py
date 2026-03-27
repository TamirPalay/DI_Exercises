'''
Create a python program that encrypts and decrypts messages with ceasar cypher.
The user enters the program, and then the program asks him if he wants to encrypt or decrypt, and then execute encryption/decryption on a given message and a given shift.

Check out this tutorial

Hint:

for letter in text:
    cypher_text += chr(ord(letter) + 3)
'''
mode=input("Do you want to encrypt or decrypt? (Type 'e' or 'd'): ").strip().lower()
if mode not in ['e', 'd']:
    print("Invalid mode. Please enter 'e' for encrypt or 'd' for decrypt.")
elif mode == 'e':
    text = input("Enter the message to encrypt: ")
    shift = int(input("Enter the shift value: "))
    cypher_text = ''
    for letter in text:
        if letter.isalpha():
            shift_amount = shift % 26
            if letter.islower():
                cypher_text += chr((ord(letter) - ord('a') + shift_amount) % 26 + ord('a'))
            else:
                cypher_text += chr((ord(letter) - ord('A') + shift_amount) % 26 + ord('A'))
        else:
            cypher_text += letter
    print("Encrypted message:", cypher_text)
else:
    text = input("Enter the message to decrypt: ")
    shift = int(input("Enter the shift value: "))
    plain_text = ''
    for letter in text:
        if letter.isalpha():
            shift_amount = shift % 26
            if letter.islower():
                plain_text += chr((ord(letter) - ord('a') - shift_amount) % 26 + ord('a'))
            else:
                plain_text += chr((ord(letter) - ord('A') - shift_amount) % 26 + ord('A'))
        else:
            plain_text += letter
    print("Decrypted message:", plain_text)