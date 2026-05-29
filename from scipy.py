from scipy.stats import chi2
p1 = 1 - chi2.cdf(22.32, 15)  # P(S^2 >= 7.44) for n=16
p2 = chi2.cdf(7.68, 15)       # P(S^2 <= 2.56) for n=16
p3 = 1 - chi2.cdf(43.15, 29)  # for n=30
p4 = chi2.cdf(14.85, 29)
print(p1,p2,p3,p4)