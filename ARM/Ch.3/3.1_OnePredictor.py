"""3.1 OnePredictor.py"""
import pystan
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

az.style.use("arviz-darkgrid")
### Data
data = pystan.read_rdump("kidiq.data.R")

### First model: kid_score ~ mom_hs
data_1 = {key: data[key] for key in ("N", "kid_score", "mom_hs")}
kidscore_momhs_model = pystan.StanModel(file="kidscore_momhs.stan")
kidscore_momhs = kidscore_momhs_model.sampling(data=data_1, iter=500)
print(az.summary(kidscore_momhs))
az.plot_posterior(kidscore_momhs)
az.plot_pair(kidscore_momhs)

### Second model: lm(kid_score ~ mom_iq)
data_2 = {key: data[key] for key in ["N", "kid_score", "mom_iq"]}
kidscore_momiq_model = pystan.StanModel(file="kidscore_momiq.stan")
kidscore_momiq = kidscore_momiq_model.sampling(data=data_2, iter=500)
print(az.summary(kidscore_momiq))
az.plot_posterior(kidscore_momiq)
az.plot_pair(kidscore_momiq)

# Figure 3.1
# kidiq_data = data.frame(kid_score, mom_hs, mom_iq)
beta_post_1 = kidscore_momhs.extract("beta")["beta"]
beta_mean_1 = np.mean(beta_post_1, axis=0)
beta_mean_1
fig3_1, ax = plt.subplots(1)
ax.plot(
    data["mom_hs"] + np.random.randn(len(data["mom_hs"])) * 0.05,
    data["kid_score"],
    lw=0,
    marker="o",
)
ax.plot(
    np.linspace(-0.2, 1.2, 2),
    np.linspace(-0.2, 1.2, 2) * beta_mean_1[1] + beta_mean_1[0],
)
ax.set_xlabel("Mother completed high school")
ax.set_xticks([0, 1])
ax.set_ylabel("Child test score")
ax.set_yticks([20, 60, 100, 140])
fig3_1

# Figure 3.2
beta_post_2 = kidscore_momiq.extract("beta")["beta"]
beta_mean_2 = np.mean(beta_post_2, axis=0)
fig3_2, ax = plt.subplots(1)
ax.plot(data["mom_iq"], data["kid_score"], lw=0, marker="o")
ax.plot(
    np.linspace(60, 140, 2), np.linspace(60, 140, 2) * beta_mean_2[1] + beta_mean_2[0]
)
ax.set_xlabel("Mother IQ score")
ax.set_xticks([80, 100, 120, 140])
ax.set_ylabel("Child test score")
ax.set_yticks([20, 60, 100, 140])
fig3_2
