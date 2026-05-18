import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ─────────────────────────────────────────────
# Exercise 1: Matrix Operations
# ─────────────────────────────────────────────

matrix = np.array([[2, 1, 3],
                   [0, 4, 1],
                   [5, 2, 8]])

det = np.linalg.det(matrix)           # determinant scalar
inverse = np.linalg.inv(matrix)       # inverse matrix (only works if det != 0)

print("=== Exercise 1: Matrix Operations ===")
print("Matrix:\n", matrix)
print(f"Determinant: {det:.2f}")
print("Inverse:\n", np.round(inverse, 3))


# ─────────────────────────────────────────────
# Exercise 2: Statistical Analysis
# ─────────────────────────────────────────────

data = np.random.randint(1, 100, size=50)   # 50 random integers between 1–99

mean   = np.mean(data)
median = np.median(data)
std    = np.std(data)

print("\n=== Exercise 2: Statistical Analysis ===")
print(f"Mean:               {mean:.2f}")
print(f"Median:             {median:.2f}")
print(f"Standard Deviation: {std:.2f}")


# ─────────────────────────────────────────────
# Exercise 3: Date Manipulation
# ─────────────────────────────────────────────

# Build all days in January 2023 as numpy datetime64 objects
january_dates = np.arange('2023-01', '2023-02', dtype='datetime64[D]')

# Convert each date to YYYY/MM/DD string format
formatted = np.datetime_as_string(january_dates).astype('U10')
formatted = np.array([d.replace('-', '/') for d in formatted])

print("\n=== Exercise 3: Date Manipulation ===")
print("Original dates (first 5):", january_dates[:5])
print("Formatted dates (first 5):", formatted[:5])


# ─────────────────────────────────────────────
# Exercise 4: Data Manipulation with NumPy & Pandas
# ─────────────────────────────────────────────

# Create a 5×3 DataFrame with random integers
df = pd.DataFrame(np.random.randint(1, 100, size=(5, 3)),
                  columns=['A', 'B', 'C'])

# Conditional selection: rows where column A > 50
filtered = df[df['A'] > 50]

print("\n=== Exercise 4: Data Manipulation ===")
print("DataFrame:\n", df)
print("Rows where A > 50:\n", filtered)
print("Column sums:\n", df.sum())
print("Column means:\n", df.mean())


# ─────────────────────────────────────────────
# Exercise 5: Image Representation
# ─────────────────────────────────────────────

# Grayscale images are 2D arrays; pixel values range 0 (black) to 255 (white)
image = np.array([[  0,  50, 100, 150, 200],
                  [ 50, 100, 150, 200, 250],
                  [100, 150, 200, 250, 255],
                  [150, 200, 250, 255, 200],
                  [200, 250, 255, 200, 150]], dtype=np.uint8)

print("\n=== Exercise 5: Image Representation ===")
print("5×5 Grayscale image array (0=black, 255=white):\n", image)
print("Shape:", image.shape, "| Dtype:", image.dtype)


# ─────────────────────────────────────────────
# Exercise 6: Basic Hypothesis Testing
# ─────────────────────────────────────────────

np.random.seed(42)
productivity_before = np.random.normal(loc=50, scale=10, size=30)
productivity_after  = productivity_before + np.random.normal(loc=5, scale=3, size=30)

# H0: no difference in means  |  H1: after > before
# A paired t-test checks whether the mean difference between pairs is zero
t_stat, p_value = stats.ttest_rel(productivity_after, productivity_before)

print("\n=== Exercise 6: Hypothesis Testing ===")
print(f"Mean before: {productivity_before.mean():.2f}")
print(f"Mean after:  {productivity_after.mean():.2f}")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value:     {p_value:.6f}")
print("Result:", "Reject H0 — training improved productivity" if p_value < 0.05
                 else "Fail to reject H0")


# ─────────────────────────────────────────────
# Exercise 7: Complex Array Comparison
# ─────────────────────────────────────────────

arr1 = np.array([10, 25, 8, 42, 17])
arr2 = np.array([15, 20, 8, 39, 30])

# Returns a boolean array: True where arr1 element > arr2 element
comparison = arr1 > arr2

print("\n=== Exercise 7: Array Comparison ===")
print("Array 1:   ", arr1)
print("Array 2:   ", arr2)
print("arr1 > arr2:", comparison)


# ─────────────────────────────────────────────
# Exercise 8: Time Series Data Manipulation
# ─────────────────────────────────────────────

# Daily time series for all of 2023
dates = np.arange('2023-01-01', '2024-01-01', dtype='datetime64[D]')
values = np.random.randn(len(dates))   # simulated daily metric

# Cast comparison values to datetime64 to match the array dtype
q1 = values[(dates >= np.datetime64('2023-01-01')) & (dates <= np.datetime64('2023-03-31'))]
q2 = values[(dates >= np.datetime64('2023-04-01')) & (dates <= np.datetime64('2023-06-30'))]
q3 = values[(dates >= np.datetime64('2023-07-01')) & (dates <= np.datetime64('2023-09-30'))]
q4 = values[(dates >= np.datetime64('2023-10-01')) & (dates <= np.datetime64('2023-12-31'))]

print(f"Q1 (Jan-Mar): {len(q1)} days, mean={q1.mean():.3f}")
print(f"Q2 (Apr-Jun): {len(q2)} days, mean={q2.mean():.3f}")
print(f"Q3 (Jul-Sep): {len(q3)} days, mean={q3.mean():.3f}")
print(f"Q4 (Oct-Dec): {len(q4)} days, mean={q4.mean():.3f}")


# ─────────────────────────────────────────────
# Exercise 9: Data Conversion
# ─────────────────────────────────────────────

# NumPy → Pandas
np_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df_from_np = pd.DataFrame(np_array, columns=['X', 'Y', 'Z'])

# Pandas → NumPy
np_from_df = df_from_np.to_numpy()

print("\n=== Exercise 9: Data Conversion ===")
print("NumPy array:\n", np_array)
print("-> DataFrame:\n", df_from_np)
print("-> back to NumPy:\n", np_from_df)


# ─────────────────────────────────────────────
# Exercise 10: Basic Visualization
# ─────────────────────────────────────────────

x = np.linspace(0, 10, 100)        # 100 evenly spaced points from 0 to 10
y = np.random.randn(100).cumsum()  # random walk (cumulative sum of noise)

plt.figure(figsize=(8, 4))
plt.plot(x, y, color='steelblue', linewidth=1.5)
plt.title("Exercise 10: Random Walk Line Graph")
plt.xlabel("X")
plt.ylabel("Cumulative Value")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()