# Exercise 1 - Patterns

# Pattern 1: Triangle centered
rows = 5
for i in range(1, rows + 1):
    spaces = ' ' * (rows - i)
    stars = '*' * (2 * i - 1)
    print(spaces + stars)

print()

# Pattern 2: Right-aligned staircase
rows = 5
for i in range(1, rows + 1):
    spaces = ' ' * (rows - i)
    stars = '*' * i
    print(spaces + stars)

print()

# Pattern 3: Hourglass staircase
rows = 5
for i in range(1, rows + 1):         # ascending half: 1 to 5 stars
    print('*' * i)
for i in range(rows, 0, -1):         # descending half: 5 to 1 stars
    spaces = ' ' * (rows - i)
    stars = '*' * i
    print(spaces + stars)


# Exercise 2 - Selection Sort Analysis

my_list = [2, 24, 12, 354, 233]      # list to be sorted: [2, 24, 12, 354, 233]

for i in range(len(my_list) - 1):    # outer loop: i goes 0,1,2,3 (each position to fill)
    minimum = i                       # assume current position holds the minimum

    for j in range(i + 1, len(my_list)):   # inner loop: scan everything after i
        if (my_list[j] < my_list[minimum]):  # found a smaller value
            minimum = j                       # update index of minimum
            if (minimum != i):               # if minimum moved, swap
                my_list[i], my_list[minimum] = my_list[minimum], my_list[i]

# Purpose: Selection Sort - repeatedly finds the minimum in the unsorted portion
# and swaps it into the correct position.
#
# Step-by-step trace:
#   Start:     [2, 24, 12, 354, 233]
#   i=0: min stays at 0 (2 is already smallest) → [2, 24, 12, 354, 233]
#   i=1: j=2 → 12 < 24, min=2, swap(1,2)       → [2, 12, 24, 354, 233]
#   i=2: j=3 → 354 > 24, j=4 → 233 > 24        → [2, 12, 24, 354, 233]
#   i=3: j=4 → 233 < 354, min=4, swap(3,4)      → [2, 12, 24, 233, 354]
#
# Final output: [2, 12, 24, 233, 354]

print(my_list)  # [2, 12, 24, 233, 354]
