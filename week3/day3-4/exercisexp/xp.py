#Goal: Implement dunder methods for a Currency class to handle string representation, 
# integer conversion, addition, and in-place addition.
class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __add__(self, other):
        if isinstance(other, int):
            self.amount += other
            return self
        elif isinstance(other, Currency):
            if self.currency == other.currency:
                self.amount += other.amount
                return self
            else:
                raise TypeError(f"Cannot add between Currency type <{self.currency}> and <{other.currency}>")
        else:
            raise TypeError("Unsupported type for addition")
    
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __int__(self):
        return self.amount

    def __repr__(self):
        return f"'{self.amount} {self.currency}s'"


'''
Using the code above, implement the relevant methods and dunder methods which will output the results below.

Hint : When adding 2 currencies which don’t share the same label you should raise an error.
'''
c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

#the comment is the expected output
print(c1)
# '5 dollars'

print(int(c1))
# 5

print(repr(c1))
# '5 dollars'

print(c1 + 5)
# 10

print(c1 + c2)
# 15

print(c1) 
# 5 dollars

c1 += 5
print(c1)
# 10 dollars

c1 += c2
print(c1)
# 20 dollars

#print(c1 + c3)
# TypeError: Cannot add between Currency type <dollar> and <shekel>
