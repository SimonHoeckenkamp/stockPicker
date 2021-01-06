import sqlite3
import datetime as datetime
import hashlib

import yfinance as yf

class User:
    """Represents user for stockPicker"""

    # TODO: password needs to be hashed; here or before saving to database 
    def __init__(self, username, email, password, portfolio=None):
        self.username = username
        self.email = email
        self.password = password
        self.portfolio = portfolio

    def save_to_db(self):
        print("Yeah")

    def add_portfolio(self, portfolio):
        self.portfolio.append(portfolio)

    @classmethod
    def get_user_from_db(cls, username, password):
        
        #TODO: insert code for db request here

        return cls


#import stock_picker_module as sp

# the user has entries: user_id, username, portfolio
# the portfolio has entries: portfolio_id, titles
# the title has entries: title_id, ticker_symbol, amount, buy_date, sell_date

#TODO: calc with full months
def calc_saving_plan_titles(ticker_symbol, value, first_buy_date, last_buy_date, period):
    """Function calcs saving plan  database, value is price per trade, 
    buy_date in format yyyy-mm-dd, period in days (default), or months"""

    # calc time difference and no of trades
    start_day = datetime.datetime.strptime(first_buy_date, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(last_buy_date, "%Y-%m-%d")

    # grab the data from yahoo finance a day before and two after
    ticker_df = yf.Ticker("MSFT").history(
        start=start_day-datetime.timedelta(days=1), 
        end=start_day+datetime.timedelta(days=2)
        )

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
        titles.append([
            date.strftime("%Y-%m-%d"), 
            ticker_symbol, 
            # following line calculates amount of titles from mean of low, high, opening and closing prices
            value / ticker_df[ticker_df.index == date.strftime("%Y-%m-%d")][["Open", "High", "Low", "Close"]].mean().mean()
            ])

    return(titles)

def add_saving_plan_titles(titles):
    """Function adds saving plan to database."""

    # connect to database and create a curser object for performing SQL commands
    conn = sqlite3.connect('stockPicker.db')
    c = conn.cursor()

    # Create table
    #c.execute('''CREATE TABLE titles ('id' INTEGER PRIMARY KEY, 'ticker' VARCHAR(255), 'buy_date' VARCHAR(255), 'amount' REAL)''')

    # Loop through titles and insert rows of data
    for title in titles:
        #print("('{}', '{}', '{}')".format(title[0], title[1], title[2]))
        c.execute("INSERT INTO titles (ticker, buy_date, amount) VALUES (:ticker, :buy_date, :amount)", 
                 {'ticker':title[0], 'buy_date':title[1], 'amount':title[2]})

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

def get_portfolio(user_id, portfolio_id):
    """Get portfolio data from database"""

def add_title_to_portfolio(portfolio_id, title_id):
    """Add title to portfolio - existing or not"""

add_saving_plan_titles(calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2000-02-02", 30))
add_saving_plan_titles(calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2020-05-12", 30))



#if __name__ == '__main__':