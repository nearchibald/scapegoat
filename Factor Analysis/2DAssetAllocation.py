# Exploratory Factor Analysis described here

# https://cssanalytics.wordpress.com/2018/07/23/2d-asset-allocation-using-pca-part-1/
# https://cssanalytics.wordpress.com/2018/08/21/2d-asset-allocation-using-pca-part-2/

import sys, os
sys.path.append("...//")
import pandas as pd
from sklearn import decomposition, preprocessing
import statsmodels.api as sm
from DataLoader import *
from matplotlib import pyplot as plt

# setup the data
Data = Data(tickers = ["IVV", "EFA", "IEFA", "AGG"])
Data.load_data()
Data = Data.get_data()

# Steps:
# 0) make a returns
# 1) check the distribution by principal components (weights)
# 2) check the first component's composition  for PC1
# 3)

data_normalized = pd.DataFrame(preprocessing.StandardScaler().fit_transform(Data))
data_normalized.columns = Data.columns
# plt.plot(data_normalized)
# plt.show()

fa = decomposition.PCA(n_components=2)
principalComponents = fa.fit_transform(data_normalized)

principalDf = pd.DataFrame(principalComponents)
print(principalDf)
plt.plot(principalDf)
plt.show()


print("Explained variance by component: %s" %fa.explained_variance_ratio_)
print(pd.DataFrame(fa.components_))

# http://emmanuel-klinger.net/factor-analysis-principal-component-analysis-and-scikit-learn.html
# https://www.youtube.com/watch?time_continue=323&v=kApPBm1YsqU
