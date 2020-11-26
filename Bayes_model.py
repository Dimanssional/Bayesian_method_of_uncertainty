import numpy as np


class BayesModel:

    def __init__(self, data):
        self.prior_probs = []
        self.posterior_probs = []

        self.data = data

    def __str__(self):
        return "Compute combinational functions CTR and GLOB"

    def compute_prior(self):
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                P = (self.data["P(Ei)"].iloc[i] + ((1 - self.data["P(Ei)"].iloc[i]) / self.data["Max"].iloc[i]) * self.data["OD"].iloc[i])
                self.prior_probs.append(P)
            else:
                P = (self.data["P(Ei)"].iloc[i] + (self.data["P(Ei)"].iloc[i] / np.abs(self.data["Min"].iloc[i])) * self.data["OD"].iloc[i])
                self.prior_probs.append(P)

        return self.prior_probs

    def add_to_dataframe(self, title, add):
        self.data[title] = add
        return self.data

    def compute_ctr(self):
        self.data = self.add_to_dataframe("P(E|E`)", self.prior_probs)
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                P = self.data["P(H)"].iloc[i] + ((self.data["P(H|Ei)"].iloc[i] - self.data["P(H)"].iloc[i])/(1 - self.data["P(Ei)"].iloc[i]))\
                        *(self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i])
                self.posterior_probs.append(P)
            else:
                P = self.data["P(H)"].iloc[i] + ((self.data["P(H)"].iloc[i] - self.data["P(H|~Ei)"].iloc[i]) / (self.data["P(Ei)"].iloc[i])) \
                    * (self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i])
                self.posterior_probs.append(P)

        self.data = self.add_to_dataframe("P(H|E`)", self.posterior_probs)
        return self.posterior_probs



