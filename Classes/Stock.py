import os
import pickle
import yfinance as yf
import matplotlib.pyplot as plt

from General import Functions, Constants


class Stock:

    def __init__(self, ticker, info_dict, history_df):

        self.ticker = ticker
        self.info_dict = info_dict
        self.history_df = history_df

        self.company_name = self.info_dict["shortName"]

    def graph(self):
        recent2020_df = self.history_df["2020"]

        Functions.graph_x_list_and_y_list(recent2020_df.index, recent2020_df["Close"], self.company_name)

        plt.xlabel("Date")
        plt.ylabel("Price (dollars)")
        plt.title("{} Historical Closing Prices 2020".format(self.company_name))
        plt.legend(loc="upper left")
        plt.grid()

        plt.show()


def download_and_save_stock_list(ticker_name_list, period, data_dir):
    for ticker_name in ticker_name_list:
        ticker_name = ticker_name.upper()
        ticker = yf.Ticker(ticker_name)
        temp_stock = Stock(
            ticker_name,
            ticker.info,
            ticker.history(period=period)
        )
        stock_file_path = "{}/{} stock.p".format(data_dir, ticker_name)
        print("Attempting to save {}... ".format(ticker_name), end="")
        if not os.path.exists(stock_file_path):
            pickle.dump(temp_stock, open(stock_file_path, "wb"))
            print("saved!")
        else:
            print("exists!")


def get_saved_stock_info(data_dir):
    stock_list = []
    for file_name in os.listdir(data_dir):
        if file_name[-2:] == ".p":
            file_path = data_dir + "/" + file_name
            temp_stock = pickle.load(open(file_path, "rb"))
            stock_list.append(temp_stock)
    return stock_list


if __name__ == '__main__':
    download_and_save_stock_list(
        ticker_name_list=[
            "FB",
            "AMZN",
            "AAPL",
            "NFLX",
            "GOOG"
        ],
        period="5y",
        data_dir=Constants.stock_data_dir
    )
