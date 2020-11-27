import numpy as np
import pandas as pd


class BayesModel:

    def __init__(self, data):
        self.prior_probs = []
        self.posterior_probs = []

        self.OH = []
        self.L = []

        self.O = None
        self.OHE_i = None
        self.GLOB = None

        self.data = data

    def get_O(self):
        return np.array(self.O).reshape(-1, 1)

    def data_correct(self) -> pd.DataFrame:
        self.data = self.data.rename(index=self.data.iloc[:, 0])
        del self.data["Unnamed: 0"]

        self.data = self.data.fillna(self.data.median())
        self.data.iloc[:, 4:] = self.data.iloc[:, 4:].astype("int")
        self.data.iloc[:, :4] = self.data.iloc[:, :4].astype("float")
        return self.data

    def __str__(self):
        return "Compute combinational functions CTR and GLOB"

    def compute_prior(self):
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                self.prior_probs.append(self.data["P(Ei)"].iloc[i] + ((1 - self.data["P(Ei)"].iloc[i]) / self.data["Max"].iloc[i])
                                        * self.data["OD"].iloc[i])
            else:
                self.prior_probs.append(self.data["P(Ei)"].iloc[i] + (self.data["P(Ei)"].iloc[i] / np.abs(self.data["Min"].iloc[i]))
                                        * self.data["OD"].iloc[i])

        return self.prior_probs

    def __add_to_dataframe(self, title, add):
        self.data[title] = add
        return self.data

    def compute_ctr(self):
        self.data = self.__add_to_dataframe("P(E|E`)", self.prior_probs)
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                self.posterior_probs.append(self.data["P(H)"].iloc[i] + ((self.data["P(H|Ei)"].iloc[i] - self.data["P(H)"].iloc[i])
                        / (1 - self.data["P(Ei)"].iloc[i])) * (self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i]))
            else:
                self.posterior_probs.append(self.data["P(H)"].iloc[i] + ((self.data["P(H)"].iloc[i] - self.data["P(H|~Ei)"].iloc[i])
                    / (self.data["P(Ei)"].iloc[i])) * (self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i]))

        self.data = self.__add_to_dataframe("P(H|E`)", self.posterior_probs)
        return self.posterior_probs

    def compute_O(self):
        return self.data["P(H)"].iloc[1] / (1 - self.data["P(H)"].iloc[1])

    def compute_OH(self):
        OH = []
        for i in range(len(self.data["OD"])):
            OH.append(self.data["P(H|E`)"].iloc[i] / (1 - self.data["P(H|E`)"].iloc[i]))

        self.data = self.__add_to_dataframe("O(H|E`)", OH)
        return OH

    def compute_L(self):
        self.O = self.compute_O()
        self.OH = self.compute_OH()

        L = []

        for i in range(len(self.data["OD"])):
            L.append(self.data["O(H|E`)"].iloc[i] / self.O)

        self.data = self.__add_to_dataframe("L", L)
        return L

    def compute_glob(self):
        self.L = self.compute_L()
        L_all = self.data["L"].prod()

        self.OHE_i = (L_all) * self.O

        self.GLOB = self.OHE_i / (1 + self.OHE_i)
        return self.GLOB

