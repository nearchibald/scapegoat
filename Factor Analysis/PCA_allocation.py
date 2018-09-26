# Exploratory Factor Analysis described here

# http://www.capitalspectator.com/excerpt-part-ii-quantitative-investment-portfolio-analytics-in-r/
#                               OR here
# https://cssanalytics.wordpress.com/2018/07/23/2d-asset-allocation-using-pca-part-1/
# https://cssanalytics.wordpress.com/2018/08/21/2d-asset-allocation-using-pca-part-2/

import pandas as pd
from sklearn import decomposition, preprocessing
import statsmodels.api as sm

# setup the data
# Transform data to returns if needed
Data = sm.datasets.longley.load_pandas().data # todo: substitute a real data from Data Loader

data_normalized = preprocessing.scale(Data) # Normalization
fa = decomposition.FactorAnalysis(n_components=2)
fa.fit(data_normalized)
print(fa.components_)
print(fa.explained_variance_)

# https://www.dummies.com/programming/big-data/data-science/data-science-using-python-to-perform-factor-and-principal-component-analysis/
# https://www.analyticsvidhya.com/blog/2016/03/practical-guide-principal-component-analysis-python/
# http://emmanuel-klinger.net/factor-analysis-principal-component-analysis-and-scikit-learn.html
