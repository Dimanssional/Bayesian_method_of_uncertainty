import pandas as pd

KNB = pd.DataFrame(pd.read_csv("KB_1.csv", delimiter=";"))
pd.set_option("display.max_rows", None, "display.max_columns", None)

print(KNB)

