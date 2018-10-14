from pandas_datareader import data

class Data():

    def __init__(self, tickers=None, start_date='2018-01-01', end_date='2018-06-01', source="yahoo", type = "Close"):

        self.Portfolios = {"ETFs": ["IVV", "EFA", "IEFA", "AGG", "IJH", "IWM", "IEMG", "IJR", "DVY"]}

        if tickers is None:
            self.tickers = self.Portfolios["ETFs"]
        else:
            self.tickers = tickers
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        self.source = source

    def load_data(self):

        self.Data = data.DataReader(self.tickers, self.source, self.start_date, self.end_date)

    def get_data(self):

        if type == "All":
            return self.Data
        else:
            return self.Data[self.type]

    def get_portfolio(self):

        return self.tickers