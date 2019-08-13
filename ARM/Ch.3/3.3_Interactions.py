import pystan
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

az.style.use("arviz-darkgrid")

### Data

data = pystan.read_rdump("kidiq.data.R")

### Model: lm(kid_score ~ mom_hs + mom_iq + mom_hs:mom_iq)
data_1 = {key : data[key] for key in ["N", "kid_score", "mom_hs", "mom_iq"]}
kidiq_interaction_model = pystan.StanModel(file='kidiq_interaction.stan')
kidiq_interaction = kidiq_interaction_model.sampling(data = data_1, iter = 1000, chains = 4)
print(az.summary(kidiq_interaction))
az.plot_posterior(kidiq_interaction)
az.plot_pair(kidiq_interaction)

### Figures
beta_post = kidiq_interaction.extract("beta")["beta"]
beta_mean = np.mean(beta_post, axis=0)
kidiq.data <- data.frame(kid_score, mom_hs = as.factor(mom_hs), mom_iq)
levels(kidiq.data$mom_hs) <- c("No", "Yes")

# Figure 3.4 (a)
kid_score = data["kid_score"]
fig3_4, ax = plt.subplots(1)
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
        np.linspace(60, 140, 2) * (beta_mean[2] +  value * beta_mean[3]) + beta_mean[1] * value + beta_mean[0],
        color=colors[value],
        label=labels[value],
        lw=4,
    )
ax.legend()
ax.set_xlabel("Mother IQ score")
ax.set_xticks([80, 100, 120, 140])
ax.set_ylabel("Child test score")
ax.set_yticks([20, 60, 100, 140])
fig3_4


# Figure 3.4 (b)
ax.set_xticks([0, 50, 100, 150])
ax.set_yticks([0, 50, 100])
ax.set_xlim(0,150)
ax.set_ylim(-15, 150)
fig3_4
