"""
Module to pull historic stock data from Quandl
(requires account, has free level) https://www.quandl.com/
"""
# import needed modules
import logging
import os

import numpy as np
import pandas as pd
import quandl

from src.utilities import config_logging

# setup required -- establish a Quandl account, and get an API key;
# set this up in your environment variables; restart your computer if necessary
config_logging()
try:
    quandl.ApiConfig.api_key = os.environ.get("quandl.ApiConfig.api_key")
except OSError:
    logging.error("Your Quandl API key is not configured correctly", OSError)


def create_efficient_frontier(selected_tickers, period_start_date, period_end_date):
    """
    function to retrieve stock history data for inputs over a date range, and return a
    dataframe of ticker symbols used and another DataFrame of potential portfolio combinations
    :param selected_tickers: stock ticker symbols of interest
    :type selected_tickers: list
    :param period_start_date: beginning date, use correct format
    :param period_end_date: end date, use correct format
    :return: two dataframes, one for ticker symbols, one for portofolio of potential combinations
    """
    # retrieve closing prices of selected_tickers with Quandl API, between the start and end dates
    data = quandl.get_table('WIKI/PRICES', ticker=selected_tickers,
                            qopts={'columns': ['date', 'ticker', 'adj_close']},
                            date={'gte': period_start_date, 'lte': period_end_date}, paginate=True)

    # reorganise data setting date as index
    # with columns of tickers and their corresponding adjusted prices
    clean = data.set_index('date')
    table = clean.pivot(columns='ticker')

    # calculate daily and annual returns of the stocks
    returns_daily = table.pct_change()
    returns_annual = returns_daily.mean() * 250

    # get daily and covariance of returns of the stock
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 250

    # empty lists to store returns, volatility and weights of imaginary portfolios
    port_returns = []
    port_volatility = []
    stock_weights = []

    # set the number of combinations for imaginary portfolios
    num_assets = len(selected_tickers)

    # edit this constant to explore more or less combinations of portfolios
    num_portfolios = 100000

    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = np.sum(weights)
        returns = np.dot(weights, returns_annual)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                 'Volatility': port_volatility}

    # extend original dictionary to include each ticker and weight
    logging.info(selected_tickers)

    for counter, symbol in enumerate(selected_tickers):
        logging.info(f"  counter: {counter} symbol: {symbol}")
        portfolio[symbol + '_Weight'] = [Weight[counter] for Weight in stock_weights]

    # make a nice DataFrame of the extended dictionary
    df = pd.DataFrame(portfolio)

    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility'] + [stock + '_Weight' for stock in selected_tickers]

    # reorder DataFrame columns
    df = df[column_order]

    # export results to a file, to explore in a jupyter notebook
    df.to_csv("data/quandl_test2.csv", sep=',', encoding='utf-8')

    # export tickers and headers to a file, for easy analysis in the jupyter notebook
    # just grab the first row of our DataFrame and export
    df_tickers = df[0:0]
    df_tickers.to_csv("data/quandl_test2_tickers.csv")

    return df_tickers, df


if __name__ == '__main__':
    # set variables for the tickers we want to include in our portfolio, and
    # the start/end dates for the historic trading data we want to pull
    tickers = ['AAPL', 'AMZN', 'FB', 'GOOG', 'INTC', 'NVDA', 'TSLA']
    start_date = "2019-01-01"
    end_date = "2019-06-01"

    create_efficient_frontier(selected_tickers=tickers,
                              period_start_date=start_date,
                              period_end_date=end_date)
