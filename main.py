import pandas as pd
import sys

from Bayes_model import BayesModel
from GUI import Window
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    KNB = pd.DataFrame(pd.read_csv("Data/KNB2.csv", delimiter=","))
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    BayesianModel = BayesModel(KNB)
    KNB = BayesianModel.data_correct()
    print("Knowledge base:")
    print(KNB, "\n")

    print("Knowledge base with CTR:")
    BayesianModel.compute()
    print(KNB, "\n")

    glob = BayesianModel.compute_glob()
    print(KNB, "\n")

    print(f"O: {BayesianModel.get_O()}")
    print(f"GLOB: {glob}")

    App = QApplication(sys.argv)
    window = Window(KNB, glob)
    sys.exit(App.exec())
