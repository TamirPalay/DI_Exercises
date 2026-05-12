
from scipy.stats import ttest_ind, t
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv("week5/day1-2/plants.csv")
print(data.head())

groups=data['Group'].unique()
print("Groups:", groups)
group1=data[data['Group']==groups[0]]['Weight']
group2=data[data['Group']==groups[1]]['Weight']
group3=data[data['Group']==groups[2]]['Weight']

t_stat, p_val=ttest_ind(group2, group3)
print(f"T-statistic: {t_stat:.2f}")
print(f"P-value: {p_val:.2e}")
alpha=0.05
if p_val < alpha:
    print("Reject the null hypothesis: There is a significant difference between the groups.")
    print("Since the p-value is less than 0.05, we reject the null hypothesis and conclude that there is a significant difference in weights between Group 2 and Group 3.")
else:
    print("Fail to reject the null hypothesis: No significant difference between the groups.")
    print("Since the p-value is greater than 0.05, we fail to reject the null hypothesis and conclude that there is no significant difference in weights between Group 2 and Group 3.")


