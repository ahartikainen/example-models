"""3.1 MultiplePredictors.py"""
import pystan
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

az.style.use("arviz-darkgrid")
### Data
data = pystan.read_rdump("kidiq.data.R")

### Model: kid_score ~ mom_hs + mom_iq
data_1 = {key: data[key] for key in ["N", "kid_score", "mom_hs", "mom_iq"]}
kidiq_multi_preds_model = pystan.StanModel(file="kidiq_multi_preds.stan")
kidiq_multi_preds = kidiq_multi_preds_model.sampling(data=data_1, iter=500, chains=4)
print(az.summary(kidiq_multi_preds))
az.plot_posterior(kidiq_multi_preds)
az.plot_pair(kidiq_multi_preds)

plt.plot(
    np.linspace(60, 140, len(data["mom_hs"])),
    np.linspace(60, 140, len(data["mom_hs"]))
    + beta_mean[2]
    + beta_mean[0]
    + beta_mean[1] * (data["mom_hs"]),
)

# Figure 3.3
beta_post = kidiq_multi_preds.extract("beta")["beta"]
beta_mean = np.mean(beta_post, axis=0)
fig3_3, ax = plt.subplots(1)
ax.scatter(
    data["mom_iq"],
    data["kid_score"],
    c=data["mom_hs"],
    cmap="Greys",
    vmin=-0.4,
    vmax=1.4,
    edgecolor="k",
)
colors = ["k", "gray"]
labels = ["No", "Yes"]
for value in [0, 1]:
    ax.plot(
        np.linspace(60, 140, 2),
        np.linspace(60, 140, 2) * beta_mean[2] + beta_mean[1] * value + beta_mean[0],
        color=colors[value],
        label=labels[value],
        lw=4,
    )
ax.legend()
ax.set_xlabel("Mother IQ score")
ax.set_xticks([80, 100, 120, 140])
ax.set_ylabel("Child test score")
ax.set_yticks([20, 60, 100, 140])
fig3_3
