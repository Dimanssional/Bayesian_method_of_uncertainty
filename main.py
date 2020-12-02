import pandas as pd
import sys

from Bayes_model import BayesModel
from GUI import Window
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    KNB = pd.DataFrame(pd.read_csv("Data/KNB_1.csv", delimiter=","))

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    BayesianModel = BayesModel(KNB)
    KNB = BayesianModel.data_correct()
    print(KNB)

    print(BayesianModel.compute_prior())
    print(BayesianModel.compute_ctr())
    print(KNB)
    glob = "%.1f" % BayesianModel.compute_glob()
    print(glob)
    print(BayesianModel.get_O())
    print(KNB)
    print(BayesianModel.__str__())

    App = QApplication(sys.argv)
    window = Window(KNB, glob)
    sys.exit(App.exec())
