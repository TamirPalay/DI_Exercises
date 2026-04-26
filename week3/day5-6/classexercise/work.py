'''
Read the file line by line
Read only the 5th line of the file
Read only the 5 first characters of the file
Read all the file and return it as a list of strings. Then split each word into letters
Find out how many occurences of the names "Darth", "Luke" and "Lea" are in the file
Append your first name at the end of the file
Append "SkyWalker" next to each first name "Luke"'''
with open("C:\\Users\\typal\\OneDrive\\Documents\\DI_Exercises\\week3\\day5-6\\classexercise\\nameslist.txt", 'r') as file:
    # Read the file line by line
    for line in file:
        print(line.strip())
    fifth_line = file.readlines()[4] 
    print(f"5th line: {fifth_line.strip()}")
    first_five_chars = file.read(5)
    print(f"First 5 characters: {first_five_chars}")
    file.seek(0)  # Reset file pointer to the beginning
    all_lines = file.readlines()
    all_words = [word for line in all_lines for word in line.split()]
    all_letters = [letter for word in all_words for letter in word]
    print(f"All letters: {all_letters}")
    name_counts = {"Darth": 0, "Luke": 0, "Lea": 0}
    for word in all_words:
        if word in name_counts:
            name_counts[word] += 1
    print(f"Name counts: {name_counts}")
with open("C:\\Users\\typal\\OneDrive\\Documents\\DI_Exercises\\week3\\day5-6\\classexercise\\nameslist.txt", 'a') as file:
    file.write("\nTamir")
with open("C:\\Users\\typal\\OneDrive\\Documents\\DI_Exercises\\week3\\day5-6\\classexercise\\nameslist.txt", 'r') as file:
    content = file.read()
    updated_content = content.replace("Luke", "Luke SkyWalker")
