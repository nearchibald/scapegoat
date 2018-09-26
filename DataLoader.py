from pandas_datareader import data

Portfolios = {"ETFs": ["IVV", "EFA", "IEFA", "AGG", "IJH", "IWM", "IEMG", "IJR", "DVY"]}

class DataLoader():

    def __init__(self, tickers = None, start_date = '2017-01-01', end_date = '2018-01-01', source = "yahoo"):

        if tickers is None: # todo: set-up warning and process this somehow later
            self.tickers = []
        else:
            self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.source = source

    def load_data(self):

        return data.DataReader(self.tickers, self.source, self.start_date, self.end_date)

    def get_portfolio(self):

        return self.tickers