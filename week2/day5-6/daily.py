class Farm:
    def __init__(self, farm_name):
        # ... code to initialize name and animals attributes ...
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type=None, count=1, **kwargs):
        if animal_type:
            if animal_type in self.animals:
                self.animals[animal_type] += count
            else:
                self.animals[animal_type] = count
        
        for animal, quantity in kwargs.items():
            if animal in self.animals:
                self.animals[animal] += quantity
            else:
                self.animals[animal] = quantity

    def get_info(self):
        # ... code to format animal info from animals dictionary ...
        print(f"{self.name}'s farm\n")
        for animal, count in self.animals.items():
            print(f"{animal} : {count}")
        print("\nE-I-E-I-0!")
    
    def get_animal_types(self):
        animals=sorted(self.animals.keys())
        for animal in animals:
            print(animal)
        
    def get_short_info(self):
        animals = sorted(self.animals.keys())
        animal_strings = []
        for animal in animals:
            if self.animals[animal] > 1:
                animal_strings.append(animal + "s")
            else:
                animal_strings.append(animal)
        
        if len(animal_strings) == 1:
            animals_str = animal_strings[0]
        else:
            animals_str = ", ".join(animal_strings[:-1]) + " and " + animal_strings[-1]
        
        return f"{self.name}'s farm has {animals_str}."

# Test the code 
macdonald = Farm("McDonald")
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)
macdonald.add_animal('chicken', 11)
macdonald.get_info()
#output:
# McDonald's farm

# cow : 5
# sheep : 2
# goat : 12

#     E-I-E-I-0!

macdonald.get_animal_types()
print(macdonald.get_short_info())