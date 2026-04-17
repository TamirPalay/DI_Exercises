'''Given a list of numbers, write a function that returns the sum of every number. BUT you can have a malicious string inside the list.

my_list = [2,3,1,2,"four",42,1,5,3,"imanumber"]'''
def sum_numbers(lst):
    total = 0
    for item in lst:
        try:
            total += int(item)
        except (ValueError, TypeError):
            print(f"Warning: '{item}' is not a number and will be skipped.")
            continue
    return total

my_list = [2,3,1,2,"four",42,1,5,3,"imanumber"]
print(sum_numbers(my_list))