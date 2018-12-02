import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import ta
import random

import sys, os
sys.path.append("...//")
from DataLoader import *

def SMA(df, n, attribute = "Close"):
    """Calculate the simple moving average for the given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = df[attribute].shift(1).rolling(n, min_periods=n).mean()
    return MA

# import data
Data = Data(tickers=["EFA"], type = "All")
Data.load_data()
Data = Data.get_data()

# filter data and add additional features
Data = Data[["Open", "High", "Low", "Close"]]
Data["O-C"] = Data["Open"] - Data["Close"]
Data["H-L"] = Data["High"] - Data["Low"]
Data["3d SMA"] = SMA(Data, 3)
Data["10d SMA"] = SMA(Data, 10)
Data["30d SMA"] = SMA(Data, 30)
Data["StDev"] = Data["Close"].shift(1).rolling(5).std()

print(Data.head(30))
