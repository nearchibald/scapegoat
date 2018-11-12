# Asset Allocation with PCA (Offence and Defence portfolios)

# ref #1 https://cssanalytics.wordpress.com/2018/07/23/2d-asset-allocation-using-pca-part-1/
# ref #2 https://cssanalytics.wordpress.com/2018/08/21/2d-asset-allocation-using-pca-part-2/

import pandas as pd
from sklearn import decomposition, preprocessing
from matplotlib import pyplot as plt

class Offence_Defence_Portfolios():

    ''' Class performs asset allocation according to the weights in the 1st principal component.
        It needs a data frame with prices for a number of assets (at least 2).
        get_portfolios() returns cumsum of absolute returns for original and fitted portflios.
        threshold parameter (None by default) filters weigths,
        the more it closer to 1 the more extreme decomposition becomes.
    '''

    def __init__(self, Data, full_report=False):

        # calculate returns and normalize data
        self.full_report = full_report
        self.Data = Data.diff().dropna()
        self.data_normalized = pd.DataFrame(preprocessing.StandardScaler().fit_transform(Data))
        self.data_normalized.columns = Data.columns

    def fit_PCA(self):

        fa = decomposition.PCA()  # setup PCA
        principalComponents = fa.fit_transform(self.data_normalized)  # run PCA
        self.principalDf = pd.DataFrame(principalComponents)  # principal components time seires

        # def weights
        self.weights = pd.DataFrame(fa.components_)
        self.weights.columns = list(self.Data.columns)

        # # explained variance of components
        print("Explained variance by component: %s" % fa.explained_variance_ratio_)

        if self.full_report:
            print(pd.DataFrame(fa.components_)) # prints weights

        # select the first component and sort it
        first_comp = pd.Series(pd.DataFrame(fa.components_).iloc[0, :])  # select the first component and sort it
        first_comp.index = list(self.data_normalized.columns)
        self.first_comp = first_comp.sort_values()

        # # plot ordered weights of the first component
        if self.full_report:
            self.first_comp.plot(kind="bar")
            plt.show()

    def get_portfolios(self, threshold=None):

        # setup weights of Offence and Defence portfolios
        Offense = self.first_comp[self.first_comp > 0]
        Defense = self.first_comp[self.first_comp < 0]

        if len(Offense) == 0 or len(Defense) == 0:
            raise Warning("Offence or Defence portfolio is empty. Add more tickers")

        Offense = Offense / Offense.sum()
        Defense = Defense / Defense.sum()

        if threshold is not None:

            if threshold > 1 or threshold < 0:
                raise Warning("An unexpected value of threshold (use values >0 or <1)")

            pos_threshold = threshold * Offense.max()
            neg_threshold = threshold * Defense.max()

            Offense = Offense[Offense > pos_threshold]
            Defense = Defense[Defense > neg_threshold]

        # setup portfolio

        Off_equity = self.Data.loc[:, list(Offense.index)].multiply(Offense).sum(axis=1)
        Def_equity = self.Data.loc[:, list(Defense.index)].multiply(Defense).sum(axis=1)
        EqualWeights = self.Data.sum(axis=1)
        EqualWeights = EqualWeights / len(list(self.Data.columns))

        Off_equity.iloc[0] = 1
        Def_equity.iloc[0] = 1
        EqualWeights.iloc[0] = 1

        Portfolios = pd.DataFrame({"Offence": Off_equity.cumsum().values,
                                   "Defense": Def_equity.cumsum().values,
                                   "Equal_Weights": EqualWeights.cumsum().values}, index=list(Off_equity.index))

        # # plot Offence, Defence and Equal Weights portfolios
        if self.full_report:

            self.Portfolios.plot(legend=True)
            plt.show()

        return Portfolios

# todo: add sliding window with rebalance period to the example or to the class+
# todo: check the code, seems like offence and defence need to be switched
