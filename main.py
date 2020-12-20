import ma_strategy
import trend_analysis


def main():

    do_ma_strategy = False
    if do_ma_strategy:
        ma_strategy.main()

    do_trend_analysis = True
    if do_trend_analysis:
        trend_analysis.main()
