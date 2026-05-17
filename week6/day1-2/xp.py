import numpy as np

# ── Exercise 1: Array Creation ───────────────────────────────────────
print("=" * 45)
print("Exercise 1: Array Creation")
arr1 = np.arange(10)
print("1D array from 0 to 9:")
print(repr(arr1))

# ── Exercise 2: Type Conversion ──────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 2: Type Conversion")
arr2 = np.array([3.14, 2.17, 0, 1, 2]).astype(int)
print("Float list converted to int array:")
print(repr(arr2))

# ── Exercise 3: Multi-Dimensional Array ──────────────────────────────
print("\n" + "=" * 45)
print("Exercise 3: 3x3 Array (values 1–9)")
arr3 = np.arange(1, 10).reshape(3, 3)
print(repr(arr3))

# ── Exercise 4: Random 2D Array ──────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 4: 4x5 Random Float Array")
arr4 = np.round(np.random.rand(4, 5), 2)  # rounded to 2 decimals for readability
print(repr(arr4))

# ── Exercise 5: Indexing ─────────────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 5: Select Second Row")
arr5 = np.array([[21,22,23,22,22],
                 [20,21,22,23,24],
                 [21,22,23,22,22]])
print("Full array:")
print(repr(arr5))
print("Second row (index 1):")
print(repr(arr5[1]))  # index 1 = second row

# ── Exercise 6: Reversing Elements ───────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 6: Reverse a 1D Array")
arr6 = np.arange(10)
print("Original:", repr(arr6))
arr6_reversed = arr6[::-1]  # slice with step -1 reverses the array
print("Reversed:", repr(arr6_reversed))

# ── Exercise 7: Identity Matrix ───────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 7: 4x4 Identity Matrix")
arr7 = np.eye(4)
print(repr(arr7))

# ── Exercise 8: Aggregation ───────────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 8: Sum and Average")
arr8 = np.arange(10)  # [0, 1, 2, ... 9]
print("Array:", arr8)
print(f"Sum: {np.sum(arr8)}, Average: {np.mean(arr8)}")

# ── Exercise 9: Reshape ───────────────────────────────────────────────
print("\n" + "=" * 45)
print("Exercise 9: 1–20 Reshaped to 4x5")
arr9 = np.arange(1, 21).reshape(4, 5)
print(repr(arr9))

# ── Exercise 10: Conditional Selection ───────────────────────────────
print("\n" + "=" * 45)
print("Exercise 10: Extract Odd Numbers")
arr10 = np.arange(1, 10)
print("Original array:", arr10)
odd_numbers = arr10[arr10 % 2 != 0]  # boolean mask: keep elements where remainder != 0
print("Odd numbers only:", repr(odd_numbers))