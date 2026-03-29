class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age

# Step 1: Create cat objects
cat1 = Cat("Fluffy", 3)
cat2 = Cat("Whiskers", 5)
cat3 = Cat("Mittens", 2)

# Step 2: Create a function to find the oldest cat
def find_oldest_cat(cat1, cat2, cat3):
    if cat1.age > cat2.age and cat1.age > cat3.age:
        return cat1
    elif cat2.age > cat1.age and cat2.age > cat3.age:
        return cat2
    elif cat3.age > cat1.age and cat3.age > cat2.age:
        return cat3
    else:
        print("There is a tie between the cats ages.")
        return None  # In case of a tie

# Step 3: Print the oldest cat's details
oldest_cat = find_oldest_cat(cat1, cat2, cat3)
if oldest_cat is not None:
    print(f"The oldest cat is {oldest_cat.name} and is {oldest_cat.age} years old.")
    
class Dog:
    def __init__(self, dog_name, height):
        self.name = dog_name
        self.height = height
    
    def bark(self):
        return self.name + " goes woof!"
    def jump(self):
        return self.name + " jumps " + str(self.height * 2) + " cm high!"
    
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Teacup", 20)

print("David's dog's name is " + davids_dog.name + " and it is " + str(davids_dog.height) + " cm tall.")
print("Sarah's dog's name is " + sarahs_dog.name + " and it is " + str(sarahs_dog.height) + " cm tall.")
print(davids_dog.bark())
print(sarahs_dog.bark())
print(davids_dog.jump())
print(sarahs_dog.jump())

if davids_dog.height > sarahs_dog.height:
    print(davids_dog.name + " is taller than " + sarahs_dog.name)
elif davids_dog.height < sarahs_dog.height:
    print(sarahs_dog.name + " is taller than " + davids_dog.name)
else:
    print(davids_dog.name + " and " + sarahs_dog.name + " are the same height.")
    
    
class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics
    
    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)
stairway = Song(["There's a lady who's sure", "all that glitters is gold", "and she's buying a stairway to heaven"])
stairway.sing_me_a_song()

class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []
    
    def add_animal(self, *args):
        for animal in args:
            if animal not in self.animals:
                self.animals.append(animal)
    
    def get_animals(self):
        for animal in self.animals:
            print(animal)
    
    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
    
    def sort_animals(self):
        sorted_animals = {}
        for animal in self.animals:
            first_letter = animal[0]
            if first_letter not in sorted_animals:
                sorted_animals[first_letter] = []
            sorted_animals[first_letter].append(animal)
        
        for key in sorted_animals:
            sorted_animals[key].sort()
        
        return sorted_animals
    def get_groups(self):
        sorted_animals = self.sort_animals()
        for key in sorted_animals:
            print(f"{key}: {sorted_animals[key]}")

# Step 2: Create a Zoo instance
brooklyn_safari = Zoo("Brooklyn Safari")

# Step 3: Use the Zoo methods
brooklyn_safari.add_animal("Giraffe")
brooklyn_safari.add_animal("Bear")
brooklyn_safari.add_animal("Baboon")
brooklyn_safari.get_animals()
brooklyn_safari.sell_animal("Bear")
brooklyn_safari.get_animals()
brooklyn_safari.sort_animals()
brooklyn_safari.get_groups()