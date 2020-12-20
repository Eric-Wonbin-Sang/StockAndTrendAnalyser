import os
import pickle
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


def get_saved_stock_info(data_dir):
    stock_list = []
    for file_name in os.listdir(data_dir):
        if file_name[-2:] == ".p":
            file_path = data_dir + "/" + file_name
            temp_stock = pickle.load(open(file_path, "rb"))
            stock_list.append(temp_stock)
    return stock_list


