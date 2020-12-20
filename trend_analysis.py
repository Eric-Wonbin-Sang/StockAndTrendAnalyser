import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression

from General import Functions

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


def get_trend_df_list(init_trend_list):

    trend_list_list = Functions.group_list_by_size(init_trend_list, 5)
    py_trends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
    trends_df_list = []
    for trend_list in trend_list_list:

        py_trends.build_payload(
            trend_list,
            cat=0,
            timeframe="2017-01-01 2020-12-15",
            geo="US",
            gprop=""
        )

        trends_df = py_trends.interest_over_time()
        trends_df = trends_df.drop(["isPartial"], axis=1)

        for col in trends_df.columns:
            trends_df_list.append(trends_df[[col]])

    return trends_df_list


def show_trends(init_trend_list, graph_individually=False):

    def update_and_show_graph():
        plt.xlabel("Date")
        plt.ylabel("Searches")
        plt.title("Google Trends")
        plt.legend(loc="upper left")
        plt.grid()

        plt.show()

    trend_df_list = get_trend_df_list(init_trend_list)

    for trend, trend_df in zip(init_trend_list, trend_df_list):

        x_list = trend_df.index.factorize()[0].reshape(-1, 1)
        y_list = trend_df[trend].values
        linear_regression = LinearRegression()
        linear_regression.fit(x_list, y_list)
        y_predicted_list = linear_regression.predict(x_list)

        Functions.graph_x_list_and_y_list(trend_df.index, trend_df[trend], trend)
        Functions.graph_x_list_and_y_list(trend_df.index, y_predicted_list, "{} linear regression: {}".format(
            trend,
            "+" if (y_predicted_list[-1] - y_predicted_list[0]) / 2 > 0 else "-"
        ))

        if graph_individually:
            update_and_show_graph()

    if not graph_individually:
        update_and_show_graph()


def main():

    trend_list = [
        "prime",
        "shipping",
        "online shopping",
        "delivery",
        "amazon"
    ]

    show_trends(trend_list, graph_individually=True)


if __name__ == '__main__':
    main()
