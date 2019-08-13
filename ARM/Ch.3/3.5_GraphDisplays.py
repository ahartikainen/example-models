import pystan
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

az.style.use("arviz-darkgrid")

### Data

data = pystan.read_rdump("kidiq.data.R")

### Regression line as a function of one input variable
data_2 = {key : data[key] for key in ["N", "kid_score", "mom_iq"]}
stan_model_2 = pystan.StanModel(file='kidscore_momiq.stan')
stanfit_2 = stan_model_2.sampling(data=data_2,
                  iter=500, chains=4)
print(az.summary(stanfit_2, var_names =["beta", "sigma"])) # missing 'lp__'

# Figure 3.2
beta_post_2 = stanfit_2.extract("beta")["beta"]
beta_mean_2 = np.mean(beta_post_2, axis=0)
#kidiq.data.2 <- data.frame(kid_score, mom_iq)
#p2 <- ggplot(kidiq.data.2, aes(x = mom_iq, y = kid_score)) +
#    geom_point() +
#    geom_abline(aes(intercept = beta.mean.2[1], slope = beta.mean.2[2])) +
#    scale_x_continuous("Mother IQ score", breaks = c(80, 100, 120, 140)) +
#    scale_y_continuous("Child test score", breaks = c(20, 60, 100, 140)) +
#    theme_bw()
#print(p2)

### Two fitted regression lines

## Model with no interaction: kid_score ~ mom_hs + mom_iq
data_3 = {key : data[key] for key in ["N", "kid_score", "mom_hs", "mom_iq"]}
stanmodel_3 = pystan.StanModel(file='kidiq_multi_preds.stan')
stanfit_3 = stanmodel_3.sampling(data=data_3,
                  iter=500, chains=4)
print(az.summary(stanfit_3, var_names = ["beta", "sigma"])) # "lp__"

# Figure 3.3
# dev.new()
# beta.post.3 <- extract(stanfit.3, "beta")$beta
# beta.mean.3 <- colMeans(beta.post.3)
# kidiq.data.3 <- data.frame(kid_score, mom_hs = as.factor(mom_hs), mom_iq)
# levels(kidiq.data.3$mom_hs) <- c("No", "Yes")
# p3 <- ggplot(kidiq.data.3, aes(x = mom_iq, y = kid_score, color = mom_hs)) +
#     geom_point() +
#     geom_abline(aes(intercept = beta.mean.3[1] + beta.mean.3[2] * (mom_hs == "Yes"),
#                     slope = beta.mean.3[3], color = mom_hs)) +
#     scale_x_continuous("Mother IQ score", breaks = c(80, 100, 120, 140)) +
#     scale_y_continuous("Child test score", breaks = c(20, 60, 100, 140)) +
#     scale_color_manual("Mother\ncompleted\nhigh\nschool",
#                        values = c("No" = "black", "Yes" = "gray")) +
#     theme_bw()
# print(p3)

## Model with interaction: kid_score ~ mom_hs + mom_iq + mom_hs:mom_iq
stanmodel_4 = pystan.StanModel(file='kidiq_interaction.stan')
stanfit_4 = stanmodel_4.sampling(data=data_3,
                  iter=500, chains=4)
print(az.summary(stanfit_4, var_names = ["beta", "sigma"])) # "lp__"

# Figure 3.4 (a)
# dev.new()
# beta.post.4 <- extract(stanfit.4, "beta")$beta
# beta.mean.4 <- colMeans(beta.post.4)
# p4 <- ggplot(kidiq.data.3, aes(x = mom_iq, y = kid_score, color = mom_hs)) +
#     geom_point() +
#     geom_abline(aes(intercept = beta.mean.4[1] + beta.mean.4[2] * (mom_hs == "Yes"),
#                     slope = beta.mean.4[3] + beta.mean.4[4] * (mom_hs == "Yes"),
#                     color = mom_hs)) +
#     scale_color_manual("Mother\ncompleted\nhigh\nschool",
#                        values = c("No" = "black", "Yes" = "gray")) +
#     theme_bw()
# print(p4 + scale_x_continuous("Mother IQ score", breaks = c(80, 100, 120, 140)) +
#     scale_y_continuous("Child test score", breaks = c(20, 60, 100, 140)))

# Figure 3.4 (b)
# dev.new()
# print(p4 +
#       scale_x_continuous("Mother IQ score", limits = c(0, 150), breaks = seq(0, 150, 50)) +
#       scale_y_continuous("Child test score", limits = c(-15, 150), breaks = c(0, 50, 100)))

### Displaying uncertainty in the fitted regression (Figure 3.10)

#dev.new()
# n = 100
# ndx = sample(nrow(beta.post.2), n)
# kidiq.post.2 <- data.frame(sampled.int = beta.post.2[ndx,1],
#                            sampled.slope = beta.post.2[ndx,2],
#                            id = ndx)
# p5 <- ggplot(kidiq.data.2, aes(x = mom_iq, y = kid_score)) +
#     geom_point() +
#     geom_abline(aes(intercept = sampled.int, slope = sampled.slope, group = id),
#                 data = kidiq.post.2, alpha = 0.05) +
#     geom_abline(aes(intercept = beta.mean.2[1], slope = beta.mean.2[2])) +
#     scale_x_continuous("Mother IQ score", breaks = c(80, 100, 120, 140)) +
#     scale_y_continuous("Child test score", breaks = c(20, 60, 100, 140)) +
#     theme_bw()
# print(p5)

### Displaying using one plot for each input variable (Figure 3.11)

# dev.new()
# n <- 100
# ndx <- sample(nrow(beta.post.3), n)
# mom_hs.mean <- mean(mom_hs)
# mom_iq.mean <- mean(mom_iq)
# kidiq.post.3 <- data.frame(
#     sampled.hs.int = beta.post.3[ndx, 1] + beta.post.3[ndx, 3] * mom_iq.mean,
#     sampled.iq.int = beta.post.3[ndx, 1] + beta.post.3[ndx, 2] * mom_hs.mean,
#     sampled.hs.slope = beta.post.3[ndx,2],
#     sampled.iq.slope = beta.post.3[ndx,3],
#     id = ndx
#     )
#
# p6 <- ggplot(kidiq.data.3, aes(x = mom_iq, y = kid_score)) +
#     geom_point() +
#     geom_abline(aes(intercept = sampled.iq.int, slope = sampled.iq.slope, group = id),
#                 data = kidiq.post.3, alpha = 0.05) +
#     geom_abline(aes(intercept = beta.mean.3[1] + beta.mean.3[2] * mom_hs.mean,
#                     slope = beta.mean.3[3])) +
#     scale_x_continuous("Mother IQ score", breaks = c(80, 100, 120, 140)) +
#     scale_y_continuous("Child test score", breaks = c(20, 60, 100, 140)) +
#     theme_bw()


# p7 <- ggplot(data.frame(kid_score, mom_hs, mom_iq), aes(x = mom_hs, y = kid_score)) +
#     geom_jitter(position = position_jitter(width = 0.05, height = 0.05)) +
#     geom_abline(aes(intercept = sampled.hs.int, slope = sampled.hs.slope, group = id),
#                 data = kidiq.post.3, alpha = 0.05) +
#     geom_abline(aes(intercept = beta.mean.3[1] + beta.mean.3[3] * mom_iq.mean,
#                     slope = beta.mean.3[2])) +
#     scale_x_continuous("Mother completed high school", breaks = c(0, 1)) +
#     scale_y_continuous("Child test score", breaks = c(0, 50, 100, 150)) +
#     theme_bw()

# pushViewport(viewport(layout = grid.layout(1, 2)))
# print(p6, vp = viewport(layout.pos.row = 1, layout.pos.col = 1))
# print(p7, vp = viewport(layout.pos.row = 1, layout.pos.col = 2))
