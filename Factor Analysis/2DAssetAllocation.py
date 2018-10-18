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

# setup the data
Data = Data()
Data.load_data()
Data = Data.get_data()

# todo: make a class
# todo: add example
# todo: add full_report func

### start ref #1

# make returns and normilize data

Data = Data.diff().dropna()
data_normalized = pd.DataFrame(preprocessing.StandardScaler().fit_transform(Data))
data_normalized.columns = Data.columns

# plt.plot(data_normalized)
# plt.show()

fa = decomposition.PCA() # setup PCA
principalComponents = fa.fit_transform(data_normalized) # run PCA

principalDf = pd.DataFrame(principalComponents) # principal components time seires

# plt.plot(principalDf.iloc[:, :3]) # print first 3 components
# plt.show()

# explained variance of components
print("Explained variance by component: %s" %fa.explained_variance_ratio_)
# print(pd.DataFrame(fa.components_)) # prints weights
first_comp = pd.Series(pd.DataFrame(fa.components_).iloc[0, :]) # select the first component
first_comp.index = list(Data.columns)
first_comp = first_comp.sort_values()

# first_comp.plot(kind="bar") # plots ordered weights of the first component
# plt.show()

### finish ref #1

### start ref #2

# setup weights of Offence and Defence portfolios
Offense = first_comp[first_comp > 0]
Offense = Offense / Offense.sum()
Defense = first_comp[first_comp < 0]
Defense = Defense / Defense.sum()

# setup portfolio
Def_equity = Data.loc[:, list(Defense.index)].multiply(Defense).sum(axis=1)
Off_equity = Data.loc[:, list(Offense.index)].multiply(Offense).sum(axis=1)
EqualWeights = Data.sum(axis = 1)
EqualWeights = EqualWeights / len(list(Data.columns))
EqualWeights.iloc[0] = 1
Def_equity.iloc[0] = 1
Off_equity.iloc[0] = 1

Portfolios = pd.DataFrame({"Offence": Off_equity.cumsum().values,
                           "Defense": Def_equity.cumsum().values,
                           "Equal_Weights": EqualWeights.cumsum().values}, index=list(Off_equity.index))

# print Offence, Defence and Equal Weights portfolios
Portfolios.plot(legend=True)
plt.show()

### finish ref #2