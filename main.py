import pandas as pd
from Bayes_model import BayesModel

KNB = pd.DataFrame(pd.read_csv("KNB2.csv", delimiter=","))

pd.set_option("display.max_rows", None, "display.max_columns", None)

BayesianModel = BayesModel(KNB)
KNB = BayesianModel.data_correct()
print(KNB)

print(BayesianModel.compute_prior())
print(BayesianModel.compute_ctr())
print(KNB)
print(BayesianModel.compute_glob())
print(BayesianModel.get_O())
print(KNB)