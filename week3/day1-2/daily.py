
import math
class Pagination:
    def __init__(self, items=None, page_size=10):
        if items is None:
            items = []
        self.items = items
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(items) / page_size)
    def get_visible_items(self):
        start_idx = self.current_idx * self.page_size
        end_idx = start_idx + self.page_size
        return self.items[start_idx:end_idx]
    def go_to_page(self, page_num):
        if page_num < 1 or page_num > self.total_pages:
            print("Entered invalid page number check")            
            raise ValueError("Page number out of range. There are only {} pages.".format(self.total_pages))
        self.current_idx = page_num - 1
        
    def first_page(self):
        self.current_idx = 0
        return self
    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self
    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self
    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self
    def __str__(self):
        visible_items = self.get_visible_items()
        return "\n".join(visible_items)
'''
Step 6: Test Your Code

Use the following test cases:
'''
alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)
print("Total Pages:", p.total_pages)
print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

p.next_page()
print(p.get_visible_items())
# ['e', 'f', 'g', 'h']

p.last_page()
print(p.get_visible_items())
# ['y', 'z']

p.go_to_page(2)
# p.go_to_page(10)
# print(p.current_idx + 1)
# Output: ValueError

#p.go_to_page(0)
# Raises ValueError

'''
Bonus: upgrade your code by changing the return statement in a way that will allor you to concatenate methods like this:
p.nextPage().nextPage().nextPage().getVisibleItems()
output: [‘m’, ‘n’, ‘o’, ‘p’]'''
print(p.next_page().next_page().next_page().get_visible_items())

