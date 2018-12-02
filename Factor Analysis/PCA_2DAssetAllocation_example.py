import sys, os
sys.path.append("...//")
from DataLoader import *
from PCA_2DAssetAllocation import *


# setup the data
Data = Data()
Data.load_data()
Data = Data.get_data()

Port = Offence_Defence_Portfolios(Data)
Port.fit_PCA()
Port = Port.get_portfolios()

Port.plot(legend=True)
plt.show()