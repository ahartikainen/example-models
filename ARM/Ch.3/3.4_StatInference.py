import pystan
import arviz as az

az.style.use("arviz-darkgrid")
### Data

data = pystan.read_rdump("kidiq.data.R")

### Model (kidiq_multi_preds.stan): kid_score ~ mom_hs + mom_iq

data_1 = {key : data[key] for key in ["N", "kid_score", "mom_hs", "mom_iq"]}
kidiq_multi_preds_model = pystan.StanModel(file='kidiq_multi_preds.stan')
kidiq_multi_preds = kidiq_multi_preds_model.sampling(data=data_1, iter=500, chains=4)
print(az.summary(kidiq_multi_preds))
az.plot_posterior(kidiq_multi_preds)
az.plot_pair(kidiq_multi_preds)
