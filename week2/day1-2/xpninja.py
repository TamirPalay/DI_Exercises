'''
Write a function called get_full_name() that takes three arguments: 1: first_name, 2: middle_name 3: last_name.
middle_name should be optional, if it’s omitted by the user, the name returned should only contain the first and the last name.
For example, get_full_name(first_name="john", middle_name="hooker", last_name="lee") will return John Hooker Lee.
But get_full_name(first_name="bruce", last_name="lee") will return Bruce Lee.'''

def get_full_name(first_name, middle_name="", last_name=""):
    if middle_name:
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()

print(get_full_name("John", "Fitzgerald", "Kennedy"))
print(get_full_name("Bruce", last_name="Lee"))
print(get_full_name("Alice", last_name="Smith"))