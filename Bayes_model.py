import numpy as np
import pandas as pd


class BayesModel(object):

    def __init__(self, data):
        # list of all posterior probabilities
        self.posterior_probs = []
        # list of all CTR functions
        self.ctr = []

        self.OH = []
        self.L = []

        # prior chance
        self._O = None
        self.OHE_i = None
        self.GLOB = None
        # our knowledge base
        self.data = data

    def __str__(self):
        return "Computing combinational functions CTR and GLOB"

    def get_O(self):
        '''getter for O'''
        return "%.1f" % self._O.astype(np.float)

    def data_correct(self) -> pd.DataFrame:

        '''function for data correction
        Change NaN data to median value of corresponding attribue
        Transforming type of some attributes
        '''

        self.data = self.data.rename(index=self.data.iloc[:, 0])
        del self.data["Unnamed: 0"]

        self.data = self.data.fillna(self.data.median())
        self.data.iloc[:, 4:] = self.data.iloc[:, 4:].astype("int")
        self.data.iloc[:, :4] = self.data.iloc[:, :4].astype("float")
        return self.data

    def compute_posterior(self):
        '''function for computiong posterior probabilities
        Formula P(E|E`) = P(Ei) + (1 - P(Ei)) / Max
        If attribute OD < 0
        Formula P(E|E`) = P(Ei) + P(Ei) / Min
        '''
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                self.posterior_probs.append(self.data["P(Ei)"].iloc[i] + ((1 - self.data["P(Ei)"].iloc[i]) / self.data["Max"].iloc[i])
                                        * self.data["OD"].iloc[i])
            else:
                self.posterior_probs.append(self.data["P(Ei)"].iloc[i] + (self.data["P(Ei)"].iloc[i] / np.abs(self.data["Min"].iloc[i]))
                                        * self.data["OD"].iloc[i])

        self.posterior_probs = [round(num, 2) for num in self.posterior_probs]
        return self.posterior_probs

    def __add_to_dataframe(self, title, add):
        ''' Private function for add data to dataframe
        title - title of adding attribute
        add - value of adding attribute
        '''
        self.data[title] = add
        return self.data

    def compute_ctr(self):

        '''Computing CTR function
        Formula P(H|E`) = P(H) + ((P(H|Ei) - P(H)) / (1 - P(Ei))) * (P(E|E`) - P(Ei))
        If attribute OD < 0
        Formula P(H|E`) = P(H) + ((P(H) - P(H|~Ei)) / (P(Ei))) * (P(E|E`) - P(Ei))'''

        self.data = self.__add_to_dataframe("P(E|E`)", self.posterior_probs)
        for i in range(len(self.data["OD"])):
            if self.data["OD"].iloc[i] > 0:
                self.ctr.append(self.data["P(H)"].iloc[i] + ((self.data["P(H|Ei)"].iloc[i] - self.data["P(H)"].iloc[i])
                        / (1 - self.data["P(Ei)"].iloc[i])) * (self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i]))
            else:
                self.ctr.append(self.data["P(H)"].iloc[i] + ((self.data["P(H)"].iloc[i] - self.data["P(H|~Ei)"].iloc[i])
                    / (self.data["P(Ei)"].iloc[i])) * (self.data["P(E|E`)"].iloc[i] - self.data["P(Ei)"].iloc[i]))

        self.ctr = [round(num, 1) for num in self.ctr]
        self.data = self.__add_to_dataframe("P(H|E`)", self.ctr)
        return self.ctr

    def compute(self):
        '''computing posterior and CTR'''
        self.posterior_probs = self.compute_posterior()
        self.ctr = self.compute_ctr()

    def compute_O(self):
        '''function to calculate apriore chance'''
        return self.data["P(H)"].iloc[1] / (1 - self.data["P(H)"].iloc[1])

    def compute_OH(self):
        '''function to calculate logical sufficiency for all rules'''
        OH = []
        for i in range(len(self.data["OD"])):
            OH.append(self.data["P(H|E`)"].iloc[i] / (1 - self.data["P(H|E`)"].iloc[i]))

        OH = [round(num, 2) for num in OH]
        self.data = self.__add_to_dataframe("O(H|E`)", OH)
        return OH

    def compute_L(self):
        '''compute LS'''
        self._O = self.compute_O()
        self.OH = self.compute_OH()

        L = []

        for i in range(len(self.data["OD"])):
            L.append(self.data["O(H|E`)"].iloc[i] / self._O)

        L = [round(num, 2) for num in L]
        self.data = self.__add_to_dataframe("L", L)
        return L

    def compute_glob(self):
        '''stock contributions of individual rules with the same conclusion to the a posterior probability of races'''
        self.L = self.compute_L()
        L_all = self.data["L"].prod()

        self.OHE_i = (L_all) * self._O

        self.GLOB = self.OHE_i / (1 + self.OHE_i)
        return "%.2f" % self.GLOB

