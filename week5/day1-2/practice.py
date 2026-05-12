from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# # Gaussian Distribution
# mu, sigma = 0, 0.1  # mean and standard deviation
# gaussian_dist = stats.norm(mu, sigma)
# print("PDF at x=0.5:", gaussian_dist.pdf(0.5))

# # Plotting Gaussian Distribution
# x_gaussian = np.linspace(-0.5, 0.5, 100)
# pdf_gaussian = gaussian_dist.pdf(x_gaussian)
# plt.figure(figsize=(6, 4))
# plt.plot(x_gaussian, pdf_gaussian)
# plt.title('Gaussian Distribution\n$\mu=0$, $\sigma=0.1$')
# plt.xlabel('x')
# plt.ylabel('PDF')
# plt.show()

# # Plotting Binomial Distribution
# x_binom = np.arange(0, n+1)
# pmf_binom = binom_dist.pmf(x_binom)
# plt.figure(figsize=(6, 4))
# plt.bar(x_binom, pmf_binom)
# plt.title('Binomial Distribution\n$n=10$, $p=0.5$')
# plt.xlabel('Number of Successes')
# plt.ylabel('PMF')
# plt.show()

# # Poisson Distribution
# lambda_ = 3  # rate
# poisson_dist = stats.poisson(lambda_)
# print("PMF for 3 events:", poisson_dist.pmf(3))

# # Plotting Poisson Distribution
# x_poisson = np.arange(0, 10)
# pmf_poisson = poisson_dist.pmf(x_poisson)
# plt.figure(figsize=(6, 4))
# plt.bar(x_poisson, pmf_poisson)
# plt.title('Poisson Distribution\n$\lambda=3$')
# plt.xlabel('Number of Events')
# plt.ylabel('PMF')
# plt.show()

import numpy as np
from scipy import stats

# Example data
x = np.array([2,4,6,8,10])
y = np.array([3,5,7,9,11])

# Performing linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# The slope and intercept of the regression line
print("Slope:", slope)
print("Intercept:", intercept)

plt.plot(x, slope*x + intercept, color='red', label='Fitted line')
plt.scatter(x, y, label='Data points')
plt.title('Linear Regression Example')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

print("The slope of the line is", slope, "and the intercept is", intercept)
print("This means there is a 1-1 relationship between x and y, as the slope is 1. This means that for every increase of 1 in x, y also increases by 1. The intercept is 1, which means that when x is 0, y would be 1 according to the fitted line.")

# Comparing three diets using ANOVA yielded an F-value of 9.7 and a P-value of 0.001.

# 1. Discuss what the F-value and P-value signify in this scenario.

# 2. What can be concluded about the diet effectiveness based on these values?
print("The F-value of 9.7 indicates that there is a significant difference in the means of the three diets. The P-value of 0.001 is much less than the common alpha level of 0.05, which suggests that we can reject the null hypothesis that all diets have the same effect. Therefore, we can conclude that at least one diet is significantly different in effectiveness compared to the others.")