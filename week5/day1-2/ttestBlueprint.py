from sklearn.datasets import load_iris
from scipy.stats import ttest_ind, t
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. LOAD THE DATA ──────────────────────────────────────────────────────────
print("\n[STEP 1] Loading dataset...")
iris = load_iris()

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)

iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

print("Dataset loaded successfully.")
print(f"Total rows: {len(iris_df)}")
print("Columns:", list(iris_df.columns))
print("Species present:", iris_df['species'].unique())


# ── 2. EXTRACT THE TWO GROUPS WE WANT TO COMPARE ─────────────────────────────
print("\n[STEP 2] Extracting groups for comparison...")

setosa_petal_length = iris_df[iris_df['species'] == 'setosa']['petal length (cm)']
versicolor_petal_length = iris_df[iris_df['species'] == 'versicolor']['petal length (cm)']

n1 = len(setosa_petal_length)
n2 = len(versicolor_petal_length)

print(f"Setosa sample size (n1): {n1}")
print(f"Versicolor sample size (n2): {n2}")

setosa_mean = setosa_petal_length.mean()
versicolor_mean = versicolor_petal_length.mean()

print(f"\nMean petal length for Setosa: {setosa_mean:.3f}")
print(f"Mean petal length for Versicolor: {versicolor_mean:.3f}")

print("\nExplanation:")
print("- We are comparing the average petal lengths of two independent groups.")
print("- If these averages are far apart, the groups may be statistically different.")


# ── 3. RUN THE T-TEST ─────────────────────────────────────────────────────────
print("\n[STEP 3] Running independent t-test...")

t_stat, p_val = ttest_ind(setosa_petal_length, versicolor_petal_length)

print(f"T-statistic (calculated) = {t_stat:.2f}")
print(f"P-value                 = {p_val:.2e}")

print("\nExplanation:")
print("- The T-statistic measures how far apart the group means are relative to variation.")
print("- The P-value tells us the probability of seeing this difference if there was NO real difference.")


# ── 4. INTERPRET THE T-STATISTIC ─────────────────────────────────────────────
print("\n[STEP 4] Interpreting T-statistic...")

if abs(t_stat) < 2:
    print(f"Since |T| = {abs(t_stat):.2f} is small (< 2), the groups are likely similar.")
elif abs(t_stat) < 10:
    print(f"Since |T| = {abs(t_stat):.2f} is moderate, the groups are somewhat different.")
else:
    print(f"Since |T| = {abs(t_stat):.2f} is VERY large, the groups are extremely different.")

print("Note: The sign of T indicates direction (which group has larger values).")

print("\nDirection insight:")
if t_stat < 0:
    print("- The negative T-stat means the FIRST group has smaller values than the SECOND.")
else:
    print("- The positive T-stat means the FIRST group has larger values than the SECOND.")


# ── 5. DETERMINE TEST TYPE (ONE-TAILED VS TWO-TAILED) ─────────────────────────
print("\n[STEP 5] Determining test type (one-tailed vs two-tailed)...")

alpha = 0.05  # define here so it's available

print("Explanation:")
print("- A one-tailed test checks for a difference in ONE direction only.")
print("- A two-tailed test checks for a difference in BOTH directions.")

print("\nIn this case:")
print("- We are asking: 'Are the means different?'")
print("- We did NOT specify a direction beforehand.")

print("\nTherefore:")
print("- This is a TWO-TAILED test.")
print("- The difference could be either higher or lower.")

print("\nT-table implication:")
print(f"- Alpha = {alpha}")
print(f"- Each tail gets alpha/2 = {alpha/2}")
print("- This is why we use (1 - alpha/2) when calculating the critical value.")


# ── 6. CRITICAL VALUE (T-TABLE LOGIC) ─────────────────────────────────────────
print("\n[STEP 6] Calculating critical value (t-table approach)...")

df = n1 + n2 - 2

print(f"Degrees of freedom (df) = {n1} + {n2} - 2 = {df}")

critical_value = t.ppf(1 - alpha/2, df)

print(f"Critical t-value (two-tailed) = +/- {critical_value:.3f}")

print("\nExplanation:")
print("- The critical value is the cutoff from the t-distribution table.")
print("- If the calculated T exceeds this value, we reject the null hypothesis.")


# ── 7. COMPARE T-STAT WITH CRITICAL VALUE ─────────────────────────────────────
print("\n[STEP 7] Comparing calculated T with critical T...")

print(f"Calculated |T| = {abs(t_stat):.3f}")
print(f"Critical |T|   = {critical_value:.3f}")

if abs(t_stat) > critical_value:
    print("\nSince the calculated |T| is GREATER than the critical value:")
    print(f"{abs(t_stat):.3f} > {critical_value:.3f}")
    print("Decision: Reject the null hypothesis (t-table method).")
else:
    print("\nSince the calculated |T| is LESS than or equal to the critical value:")
    print(f"{abs(t_stat):.3f} <= {critical_value:.3f}")
    print("Decision: Fail to reject the null hypothesis (t-table method).")


# ── 8. SIGNIFICANCE CHECK (P-VALUE METHOD) ────────────────────────────────────
print("\n[STEP 8] Checking statistical significance using P-value...")

print(f"Alpha = {alpha}")
print(f"P-value = {p_val:.2e}")

print("\nDecision logic:")
print("- If P-value < alpha : reject the null hypothesis")
print("- If P-value >= alpha : fail to reject the null hypothesis")

if p_val < alpha:
    print(f"\nSince {p_val:.2e} < {alpha}, we REJECT the null hypothesis.")
else:
    print(f"\nSince {p_val:.2e} >= {alpha}, we FAIL to reject the null hypothesis.")


# ── 9. FINAL INTERPRETATION ───────────────────────────────────────────────────
print("\n[STEP 9] Final interpretation...")

print("General interpretation:")
print("- A very small P-value suggests strong evidence against the null hypothesis.")
print("- A large |T| relative to the critical value also supports this conclusion.")

# Data-specific conditional interpretation
if p_val < alpha and abs(t_stat) > critical_value:
    print("\nData-specific interpretation:")
    print("- The two groups are clearly statistically different.")
    print("- The feature being tested is highly effective at separating these groups.")
    
    if "setosa" in iris_df['species'].values:
        print("- In this dataset, Setosa petals are much smaller than Versicolor petals.")
elif p_val < alpha:
    print("\nData-specific interpretation:")
    print("- There is a statistically significant difference, but effect size may vary.")
else:
    print("\nData-specific interpretation:")
    print("- No strong evidence of a difference between the groups.")


# ── 10. VISUALIZE THE DISTRIBUTIONS ───────────────────────────────────────────
print("\n[STEP 10] Plotting distributions...")

sns.histplot(setosa_petal_length, color="skyblue", label="Iris Setosa", kde=True)
sns.histplot(versicolor_petal_length, color="red", label="Iris Versicolor", kde=True)

plt.title(
    f"Iris Petal Length Comparison\nT-statistic: {t_stat:.2f}, P-value: {p_val:.2e}"
)

plt.xlabel("Petal Length (cm)")
plt.ylabel("Frequency")
plt.legend()

plt.show()

print("\nVisualization insight:")
print("- If distributions barely overlap -> strong difference")
print("- If they overlap heavily -> weak or no difference")