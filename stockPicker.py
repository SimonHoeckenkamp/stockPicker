import sqlite3
import datetime as datetime

import yfinance as yf

#import stock_picker_module as sp

# the user has entries: user_id, username, portfolio
# the portfolio has entries: portfolio_id, titles
# the title has entries: title_id, ticker_symbol, amount, buy_date, sell_date

#TODO: calc with full months
def calc_saving_plan_titles(ticker_symbol, value, first_buy_date, last_buy_date, period):
    """Function calcs saving plan to database, value is price per trade, 
    buy_date in format yyyy-mm-dd, period in days (default), or months"""

    # calc time difference and no of trades
    start_day = datetime.datetime.strptime(first_buy_date, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(last_buy_date, "%Y-%m-%d")

    #loop throw the dates and append corresponding day
    dates = []
    while start_day < end_day:
        dates.append(start_day)
        start_day += datetime.timedelta(days=period)

    # TODO: control the input values throw an exception if neccessary
    if len(dates) == 0:
        print("wrong input in function 'calc_saving_plan_titles()'")  
    
    # fill a list with titles
    titles = []
    for date in dates:
        titles.append([date, value / 
            yf.Ticker(ticker_symbol).history(interval="1d", start=date)[["Open","High", "Low", "Close"]].mean().mean()])

    print("end of function...")



def add_saving_plan_titles(*titles):
    """Function adds saving plan to database."""

calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2000-02-02", 30)
calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2020-05-12", 30)



#if __name__ == '__main__':