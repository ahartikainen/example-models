import numpy as np
from scipy import stats
from scipy.stats.mstats_basic import mquantiles as quantiles
import matplotlib.pyplot as plt


# CI for continuous data

y = np.array([35,34,38,35,37])
n = len(y)
estimate = np.mean(y)
se = np.std(y, ddof=1)/np.sqrt(n)
int_50 = estimate + stats.t.ppf([0.25,0.75],n-1)*se
int_95 = estimate + stats.t.ppf([0.025,0.975],n-1)*se
print("Continuous data:\nCI 50: ({:.3f}, {:.3f})\nCI 90: ({:.3f}, {:.3f})".format(*int_50, *int_95), end="\n\n")

# CI for proportions

y = 700
n = 1000
estimate = y/n
se = np.sqrt(estimate*(1-estimate)/n)
int_95 = estimate + stats.norm.ppf([0.025,0.975])*se
print("Proportional data:\nCI 95: ({:.3f}, {:.3f})".format(*int_95), end="\n\n")

# CI for discrete data

y = np.repeat([0,1,2,3,4], [600,300,50,30,20])
n = len(y)
estimate = np.mean(y)
se = np.std(y, ddof=1)/np.sqrt(n)
int_50 = estimate + stats.t.ppf([0.25,0.75],n-1)*se
int_95 = estimate + stats.t.ppf([0.025,0.975],n-1)*se
print("Discrete data:\nCI 50: ({:.3f}, {:.3f})\nCI 90: ({:.3f}, {:.3f})".format(*int_50, *int_95), end="\n\n")

# Plot Figure 2.3

polls = np.genfromtxt("polls.dat")
support = polls[:,2] / (polls[:,2]+polls[:,3])
year =  polls[:,0] + (polls[:,1]-6)/12
y_se = np.sqrt(support * (1 - support)/1000)
y_max = 100 * (support + y_se)
y_min = 100 * (support - y_se)

# TODO: mpl
#limits = aes(ymax=y.max,ymin=y.min)
#frame1 = data.frame(year=year,support=support*100)
#m <- ggplot(frame1,aes(x=year,y=support))
#m + geom_point() + scale_y_continuous("Percentage Support for the Death #Penalty") + scale_x_continuous("Year") + theme_bw() + #geom_pointrange(limits)

# Weighted averages

N = np.array([65633200,80523700,59685200]) # population sizes FR, DE, IT
p = np.array([0.55,0.61,0.38])  # estimated proportions of Yes responses
se = np.array([0.02,0.03,0.03])

w_avg = np.sum(N*p)/np.sum(N)
se_w_avg = np.sqrt (np.sum ((N*se/np.sum(N))**2))
int_95 = w_avg + np.array([-2,2])*se_w_avg
print("Weighted averages:\nCI 95: ({:.3f}, {:.3f}))".format(*int_95), end="\n\n")

# CI using simulations

n_men = 500
p_hat_men = 0.75
se_men = np.sqrt(p_hat_men*(1-p_hat_men)/n_men)

n_women = 500
p_hat_women = 0.65
se_women = np.sqrt(p_hat_women*(1-p_hat_women)/n_women)

n_sims = 10000
p_men = stats.norm.rvs(p_hat_men, se_men, size=n_sims)
p_women = stats.norm.rvs(p_hat_women, se_women, size=n_sims)
ratio = p_men/p_women
int_95 = quantiles(ratio, prob=[.025,.975])
print("Simulations:\nCI 95: ({:.3f}, {:.3f}))".format(*int_95))