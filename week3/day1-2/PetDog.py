#Exercise 3: Dogs Domesticated
from random import random

from Dog import Dog

class PetDog(Dog):
    def __init__(self, name, age, weight, trained=False):
        super().__init__(name, age, weight)
        self.trained = trained

    def train(self):
        print(self.bark())
        self.trained = True
        return f"{self.name} is now trained!"

    #Implement a play(*args) method that prints “<dog_names> all play together”.*args on this method is a list of dog instances.
    def play(self, *other_dogs):
        dog_names = [self.name] + [dog.name for dog in other_dogs]
        print(f"{', '.join(dog_names)} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
            trick= tricks[int(random() * len(tricks))]
            return f"{self.name} {trick}!"
        else:
            return f"{self.name} is not trained yet!"

# Test PetDog methods
my_dog = PetDog("Fido", 2, 10)
buddy = PetDog("Buddy", 3, 12)
max_dog = PetDog("Max", 1, 8)
print(my_dog.train())
my_dog.play(buddy, max_dog)
print(my_dog.do_a_trick())