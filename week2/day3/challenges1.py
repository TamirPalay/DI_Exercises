# Exercise 1 - Insert Item at Index
my_list = [1, 2, 3, 5]
my_list.insert(3, 4)
print(my_list)  # [1, 2, 3, 4, 5]


# Exercise 2 - Count Spaces in a String
def count_spaces(s):
    count = 0
    for char in s:
        if char == ' ':
            count += 1
    return count

print(count_spaces("hello world foo bar"))  # 3


# Exercise 3 - Count Upper and Lower Case Letters
def count_cases(s):
    upper = 0
    lower = 0
    for char in s:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
    print(f"Upper: {upper}, Lower: {lower}")

count_cases("Hello World")  # Upper: 2, Lower: 8


# Exercise 4 - Sum of Array (without built-in)
def my_sum(arr):
    total = 0
    for n in arr:
        total += n
    return total

print(my_sum([1, 5, 4, 2]))  # 12


# Exercise 5 - Find Max in List
def find_max(arr):
    max_val = arr[0]
    for n in arr:
        if n > max_val:
            max_val = n
    return max_val

print(find_max([0, 1, 3, 50]))  # 50


# Exercise 6 - Factorial
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial(4))  # 24


# Exercise 7 - Count Element in List (without .count())
def list_count(lst, item):
    count = 0
    for el in lst:
        if el == item:
            count += 1
    return count

print(list_count(['a', 'a', 't', 'o'], 'a'))  # 2


# Exercise 8 - L2 Norm
def norm(lst):
    return sum(x ** 2 for x in lst) ** 0.5

print(norm([1, 2, 2]))  # 3.0


# Exercise 9 - Check if List is Monotonic
def is_mono(lst):
    ascending = all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))
    descending = all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))
    return ascending or descending

print(is_mono([7, 6, 5, 5, 2, 0]))  # True
print(is_mono([2, 3, 3, 3]))        # True
print(is_mono([1, 2, 0, 4]))        # False


# Exercise 10 - Print Longest Word
def longest_word(lst):
    longest = lst[0]
    for word in lst:
        if len(word) > len(longest):
            longest = word
    print(longest)

longest_word(["cat", "elephant", "dog"])  # elephant


# Exercise 11 - Separate Integers and Strings
def separate(lst):
    ints = []
    strings = []
    for item in lst:
        if isinstance(item, int):
            ints.append(item)
        elif isinstance(item, str):
            strings.append(item)
    return ints, strings

print(separate([1, "hello", 2, "world", 3]))  # ([1, 2, 3], ['hello', 'world'])


# Exercise 12 - Check Palindrome
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]

print(is_palindrome('radar'))  # True
print(is_palindrome('John'))   # False


# Exercise 13 - Count Words with Length > k
def sum_over_k(sentence, k):
    return sum(1 for word in sentence.split() if len(word) > k)

sentence = 'Do or do not there is no try'
print(sum_over_k(sentence, 2))  # 3


# Exercise 14 - Average Value in Dictionary
def dict_avg(d):
    return sum(d.values()) / len(d)

print(dict_avg({'a': 1, 'b': 2, 'c': 8, 'd': 1}))  # 3.0


# Exercise 15 - Common Divisors of 2 Numbers
def common_div(a, b):
    return [i for i in range(2, min(a, b) + 1) if a % i == 0 and b % i == 0]

print(common_div(10, 20))  # [2, 5, 10]


# Exercise 16 - Check if Number is Prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(11))  # True


# Exercise 17 - Print Elements Where Index and Value are Even
def weird_print(lst):
    result = [lst[i] for i in range(len(lst)) if i % 2 == 0 and lst[i] % 2 == 0]
    print(result)

weird_print([1, 2, 2, 3, 4, 5])  # [2, 4]


# Exercise 18 - Count Argument Types
def type_count(**kwargs):
    counts = {}
    for val in kwargs.values():
        t = type(val).__name__
        counts[t] = counts.get(t, 0) + 1
    print(', '.join(f"{t}: {c}" for t, c in counts.items()))

type_count(a=1, b='string', c=1.0, d=True, e=False)  # bool: 2, int: 1, str: 1, float: 1


# Exercise 19 - Mimic str.split()
def my_split(s, sep=None):
    result = []
    current = ''
    if sep is None:
        s = s.strip()
        for char in s:
            if char == ' ':
                if current:
                    result.append(current)
                    current = ''
            else:
                current += char
    else:
        for char in s:
            if char == sep:
                result.append(current)
                current = ''
            else:
                current += char
    if current:
        result.append(current)
    return result

print(my_split("hello world foo"))      # ['hello', 'world', 'foo']
print(my_split("a,b,c,d", ','))         # ['a', 'b', 'c', 'd']


# Exercise 20 - Convert String to Password Format
def to_password(s):
    replacements = {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$'}
    return ''.join(replacements.get(c.lower(), c) for c in s)

print(to_password("mypassword"))  # myp@$$w0rd
