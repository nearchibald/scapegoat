# Asset Allocation with PCA (Offence and Defence portfolios)

# ref #1 https://cssanalytics.wordpress.com/2018/07/23/2d-asset-allocation-using-pca-part-1/
# ref #2 https://cssanalytics.wordpress.com/2018/08/21/2d-asset-allocation-using-pca-part-2/

import sys, os
sys.path.append("...//")
import pandas as pd
from sklearn import decomposition, preprocessing
import statsmodels.api as sm
from DataLoader import *
from matplotlib import pyplot as plt

class Offence_Defence_Portfolios():

    def __init__(self, Data):

        # calculate returns and normalize data
        self.Data = Data.diff().dropna()
        self.data_normalized = pd.DataFrame(preprocessing.StandardScaler().fit_transform(Data))
        self.data_normalized.columns = Data.columns

    def fit_PCA(self):

        fa = decomposition.PCA()  # setup PCA
        principalComponents = fa.fit_transform(self.data_normalized)  # run PCA
        self.principalDf = pd.DataFrame(principalComponents)  # principal components time seires

        # def weights
        self.weight = pd.DataFrame(fa.components_)
        self.weight.columns = list(self.Data.columns)

        # # explained variance of components
        print("Explained variance by component: %s" % fa.explained_variance_ratio_)
        # print(pd.DataFrame(fa.components_)) # prints weights

        # select the first component and sort it
        first_comp = pd.Series(pd.DataFrame(fa.components_).iloc[0, :])  # select the first component and sort it
        first_comp.index = list(Data.columns)
        self.first_comp = first_comp.sort_values()

        # # plot ordered weights of the first component
        # self.first_comp.plot(kind="bar")
        # plt.show()

    def get_portfolios(self):

        # setup weights of Offence and Defence portfolios
        Offense = self.first_comp[self.first_comp > 0]
        Offense = Offense / Offense.sum()
        Defense = self.first_comp[self.first_comp < 0]
        Defense = Defense / Defense.sum()

        # setup portfolio
        Def_equity = self.Data.loc[:, list(Defense.index)].multiply(Defense).sum(axis=1)
        Off_equity = self.Data.loc[:, list(Offense.index)].multiply(Offense).sum(axis=1)
        EqualWeights = self.Data.sum(axis=1)
        EqualWeights = EqualWeights / len(list(self.Data.columns))
        EqualWeights.iloc[0] = 1
        Def_equity.iloc[0] = 1
        Off_equity.iloc[0] = 1

        Portfolios = pd.DataFrame({"Offence": Off_equity.cumsum().values,
                                   "Defense": Def_equity.cumsum().values,
                                   "Equal_Weights": EqualWeights.cumsum().values}, index=list(Off_equity.index))

        # # print Offence, Defence and Equal Weights portfolios
        # self.Portfolios.plot(legend=True)
        # plt.show()

        return Portfolios


# setup the data
Data = Data()
Data.load_data()
Data = Data.get_data()

# todo: add example
# todo: add full_report func

Port = Offence_Defence_Portfolios(Data)
Port.fit_PCA()
Port = Port.get_portfolios()

Port.plot(legend=True)
plt.show()