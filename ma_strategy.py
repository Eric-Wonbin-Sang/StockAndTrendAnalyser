import numpy as np
import matplotlib.pyplot as plt

from Classes import Stock

from General import Constants


def get_rolling_col_name_list(rolling_period_list):
    return ["{} Day MA".format(rolling_period) for rolling_period in rolling_period_list]


def get_ma_strategy_df_list(stock_list, rolling_period_list):

    ma_strategy_df_list = []

    for stock in stock_list:

        close_df = stock.history_df["2020"]
        close_df = close_df.drop(["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"], axis=1)

        rolling_col_name_list = get_rolling_col_name_list(rolling_period_list)
        for rolling_period, rolling_col_name in zip(rolling_period_list, rolling_col_name_list):
            close_df[rolling_col_name] = close_df["Close"].rolling(window=rolling_period).mean()

        close_df["MA Delta"] = close_df[rolling_col_name_list[1]] - close_df[rolling_col_name_list[0]]
        close_df["sign"] = np.where(close_df["MA Delta"] > 0, True, False)
        close_df["sign lagged"] = close_df["sign"].shift(1)
        close_df["raw signal"] = np.where(close_df["sign"] != close_df["sign lagged"], close_df["MA Delta"], False)
        close_df["signal"] = np.where(close_df["raw signal"], close_df[rolling_col_name_list[0]], np.NaN)
        close_df["Buy"] = np.where(close_df["raw signal"] < 0, close_df["Close"], np.NaN)
        close_df["Sell"] = np.where(close_df["raw signal"] > 0, close_df["Close"], np.NaN)

        ma_strategy_df_list.append(close_df)

    return ma_strategy_df_list


def print_buy_sell_stats(stock_list, ma_strategy_df_list):
    for i, ma_strategy_df in enumerate(ma_strategy_df_list):
        print(
            "Stock: {}\n\tBuy Count: {}\n\tSell Count: {}".format(
                stock_list[i].company_name,
                ma_strategy_df["Buy"].count(),
                ma_strategy_df["Sell"].count()
            )
        )


def graph_ma_strategy_df_list(stock_list, rolling_period_list, ma_strategy_df_list):
    for i, ma_strategy_df in enumerate(ma_strategy_df_list):

        plt.plot(ma_strategy_df.index, ma_strategy_df["Close"], label="Closing", zorder=1)
        for rolling_col_name in get_rolling_col_name_list(rolling_period_list):
            plt.plot(ma_strategy_df.index, ma_strategy_df[rolling_col_name], label=rolling_col_name, zorder=1)

        plt.scatter(ma_strategy_df.index, ma_strategy_df["signal"],
                    color="indigo", marker='o', alpha=1, zorder=2, label="MA Intersections")
        plt.scatter(ma_strategy_df.index, ma_strategy_df["Buy"],
                    color='green', marker='^', alpha=1, zorder=3, label="Buy Signals")
        plt.scatter(ma_strategy_df.index, ma_strategy_df["Sell"],
                    color='red', marker='v', alpha=1, zorder=3, label="Sell Signals")

        plt.xlabel("Date")
        plt.ylabel("Price (dollars)")
        plt.title("{} Historical Closing Prices 2020".format(stock_list[i].company_name))
        plt.legend(loc="upper left")
        plt.grid()

        plt.show()


def main():

    stock_list = Stock.get_saved_stock_info(data_dir=Constants.stock_data_dir)

    rolling_period_list = [5, 25]

    ma_strategy_df_list = get_ma_strategy_df_list(stock_list, rolling_period_list)

    print_buy_sell_stats(stock_list, ma_strategy_df_list)

    graph_ma_strategy_df_list(stock_list, rolling_period_list, ma_strategy_df_list)


main()
