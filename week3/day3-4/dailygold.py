'''Notice : solve this exercise using a lambda function.

Ask a user for the following inputs 5 times:
Name (string)
Age (int)
Score (int)
Build a list of tuples using these inputs, each tuple should contain a name, age and score.
Sort the list by the following priority Name > Age > Score.'''
user_data = []
for i in range(5):
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    score = int(input("Enter your score: "))
    user_data.append((name, age, score))
sorted_data = sorted(user_data, key=lambda x: (x[0], x[1], x[2]))
print(sorted_data)