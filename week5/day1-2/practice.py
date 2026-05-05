# from scipy import stats
# import numpy as np
# import matplotlib.pyplot as plt

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
x = np.array([5, 10, 15, 20, 25])
y = np.array([12, 24, 37, 43, 50])

# Performing linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# The slope and intercept of the regression line
print("Slope:", slope)
print("Intercept:", intercept)
print("R-value:", r_value)
print("P-value:", p_value)
print("Standard Error:", std_err)