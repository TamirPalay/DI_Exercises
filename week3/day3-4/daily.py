class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is not None:
            self.radius = radius
        elif diameter is not None:
            self.radius = diameter / 2
        else:
            raise ValueError("Either radius or diameter must be provided.")
    
    @property
    def diameter(self):
        return self.radius * 2
    
    def getArea(self):
        return 3.14 * self.radius ** 2
    def __repr__(self):
        return f"Circle with radius: {self.radius}"
    
    #Add two circles together and return a new circle with the new radius — use a dunder method (__add__).
    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(radius=self.radius + other.radius)
        else:
            raise TypeError("Unsupported type for addition")
    
    #✅ Compare two circles to see which is bigger — use a dunder method (__gt__).
    def __gt__(self, other):
        if isinstance(other, Circle):
            return self.radius > other.radius
        else:
            raise TypeError("Unsupported type for comparison")

    #✅ Compare two circles to check if they are equal — use a dunder method (__eq__).
    def __eq__(self, other):
        if isinstance(other, Circle):
            return self.radius == other.radius
        else:
            raise TypeError("Unsupported type for comparison")
        
    # Store multiple circles in a list and sort them — implement __lt__ or other comparison methods.
    def __lt__(self, others):
        others.append(self)
        return sorted(others, key=lambda x: x.radius)

#Example usage:
c1 = Circle(radius=5)
c2 = Circle(diameter=20)
print(c1)  # Circle with radius: 5
print(c2)  # Circle with radius: 10.0
c3 = c1 + c2
print(c3)  # Circle with radius: 15.0
print(c1 > c2)  # False
print(c1 == c2)  # False    
circles = [c1, c2, c3]
sorted_circles = sorted(circles, key=lambda x: x.radius)
print(sorted_circles)  # [Circle with radius: 5, Circle with radius: 10.0, Circle with radius: 15.0]
    
    
