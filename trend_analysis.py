import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression

from General import Functions

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


def group_list_by_size(trend_list, list_size):
    # This groups any one dimensional list and groups it into lists with length of up to list_size
    if not trend_list:
        return []
    if len(trend_list) < list_size:
        return [trend_list]
    data_list_list = list([list(x) for x in zip(*[iter(trend_list)] * list_size)])
    if len(trend_list) % list_size != 0:
        data_list_list.append(trend_list[-(len(trend_list) % list_size):])
    return data_list_list


def get_trend_df_list(init_trend_list):

    trend_list_list = group_list_by_size(init_trend_list, 5)
    py_trends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
    trends_df_list = []
    for trend_list in trend_list_list:

        py_trends.build_payload(
            trend_list,
            cat=0,
            timeframe="2019-01-01 2020-12-15",
            geo="US",
            gprop=""
        )

        trends_df = py_trends.interest_over_time()
        trends_df = trends_df.drop(["isPartial"], axis=1)

        for col in trends_df.columns:
            trends_df_list.append(trends_df[[col]])

    return trends_df_list


def show_trends(init_trend_list):

    trend_df_list = get_trend_df_list(init_trend_list)

    for trend, trend_df in zip(init_trend_list, trend_df_list):

        rolling_name = "{} Rolling".format(trend)
        trend_df[rolling_name] = trend_df[trend].rolling(window=30).mean()

        x_list = trend_df.index.factorize()[0].reshape(-1, 1)
        y_list = trend_df[trend].values
        linear_regression = LinearRegression()
        linear_regression.fit(x_list, y_list)
        y_predicted_list = linear_regression.predict(x_list)

        Functions.graph_x_list_and_y_list(trend_df.index, trend_df[trend], trend)
        # graph_x_list_and_y_list(trend_df.index, trend_df[rolling_name], rolling_name)
        Functions.graph_x_list_and_y_list(trend_df.index, y_predicted_list, "{} linear regression: {}".format(
            trend,
            "+" if (y_predicted_list[-1] - y_predicted_list[0]) / 2 > 0 else "-"
        ))

        plt.xlabel("Date")
        plt.ylabel("Searches")
        plt.title("Trends")
        plt.legend(loc="upper left")
        plt.grid()

        plt.show()


show_trends(["prime", "shipping", "work from home", "online shopping", "delivery", "restaurants"])
