class Person():
    def __init__(self, first_name, age, last_name=""):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"
    def is_18(self):
        return self.age >= 18

class Family():
    def __init__(self, last_name, members):
        self.last_name = last_name
        self.members = members
    def born(self, first_name, age):
        new_member = Person(first_name, age, self.last_name)
        self.members.append(new_member)
        print(f"Congratulations! {new_member.first_name} {new_member.last_name} was born!")
        return new_member
    
    def check_majority(self,first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friend")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print(f"No family member named {first_name} found.")
    
    def family_presentation(self):
        print(f"Family {self.last_name} members:")
        for member in self.members:
            print(f"{member.first_name}, {member.age} years old")

# Example usage
family_members = [
    Person("John", 40, "Smith"),
    Person("Jane", 38, "Smith"),
    Person("Emily", 16, )
]
family = Family("Smith", family_members)
family.family_presentation()
new_baby = family.born("Michael", 0)
family.check_majority("Emily")
family.check_majority("Michael")
family.check_majority("John")
family.check_majority("Jane")
family.check_majority("Nonexistent")


