import sqlite3  # connection to sqlite database
import datetime as datetime # datetime for converting dates
import hashlib  # hashing passwords in database

import yfinance as yf   # API for stock ticker requests

class Database_Entry_Exception(Exception):
    """A user-defined Exception for invalid access on database"""

    def __init__(self, no_of_rows):
        Exception.__init__(self)
        self.no_of_rows = no_of_rows

class User:
    """Represents user for stockPicker"""

    # form of database:
    # id, username, email, password

    # TODO: password needs to be hashed; here or before saving to database 
    # TODO: extend with portfolio information
    #def __init__(self, username, email, password, portfolio=None):
    def __init__(self, username, email, password, user_id=None, hashed_password=False):
        self.user_id = user_id
        self.username = username
        self.email = email

        # insert the hashed password
        # TODO: use salting for making saving password safer against brute force attacks
        if not hashed_password:
            self.password = hashlib.sha256(str(password).encode("utf-8")).hexdigest()
        else:
            self.password = password

        #self.portfolio = portfolio

    #print data of User instance
    def print_name(self):
        print("User:", "ID:", self.user_id, " -- name:", self.username, " -- email", self.email, " -- password", self.password)

    def save_to_db(self):
        # connect to database and create a curser object for performing SQL commands
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        #add user to the database
        c.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                {'username':self.username, 'email':self.email, 'password':self.password})

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    #def add_portfolio(self, portfolio):
    #    self.portfolio.append(portfolio)

    @classmethod
    def get_user_from_db(cls, username, password):
        # connect to database and create a curser object for performing SQL commands
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        hashed_password = hashlib.sha256(str(password).encode("utf-8")).hexdigest()

        rows = c.execute("SELECT * FROM users WHERE username=:username AND password=:password", 
                        {"username": username, "password": hashed_password}).fetchall()
        conn.commit()
        
        # Raise exception if no of users is invalid
        if len(rows) != 1:
            raise Database_Entry_Exception(len(rows))

        # close connection 
        conn.close()
        
        return cls(rows[0][1], rows[0][2], rows[0][3], user_id=rows[0][0], hashed_password=True)

class Title:
    """Represents title in portfolio e.g. a fraction of a fund or stocks"""

    def __init__(self, name, buy_date, sell_date, amount):
        self.name = name
        self.buy_date = buy_date
        self.sell_date = sell_date
        self.amount = amount

class Portfolio:
    """Connects User to Titles, one User can join different Titles in one Portfolio"""
    
    def __init__(self, user_id, title_ids):
        self.user_id = user_id
        self.title_ids = title_ids

    def add_title_to_portfolio(self, title_id):
        self.title_ids.append(title_id)

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


def test_function():
    #create database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    #delete database before test to have a fresh start
    c.execute('''DROP TABLE users''')
    conn.commit()

    # comment out if db already exists
    c.execute('''CREATE TABLE users ('id' INTEGER PRIMARY KEY, 'username' VARCHAR(255), 'email' VARCHAR(255), 'password' VARCHAR(255))''')

    # Save (commit) the changes
    conn.commit()

    # add first users
    User("Jon", "Jon@web.com", "password1").save_to_db()
    User("Jim", "Jim@web.com", "password2").save_to_db()
    User("Joe", "Joe@web.com", "password3").save_to_db()
    User("Tim", "Tim@web.com", "password4").save_to_db()
    User("Carl", "Carl@web.com", "password5").save_to_db()
    User("Jen", "Jen@web.com", "password6").save_to_db()

    #test the entries
    # for row in c.execute("SELECT * FROM users"):
    #     for col in row:
    #         print(col)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

test_function()

try:
    new_user = User.get_user_from_db("Jon", "password1")
    new_user.print_name()
except Database_Entry_Exception as ex:
    print("Database_Entry_Exception: Wrong Input - no users available")
except IndexError:
    print("IndexError")





#add_saving_plan_titles(calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2000-02-02", 30))
#add_saving_plan_titles(calc_saving_plan_titles("MSFT", 50.00, "2000-02-01", "2020-05-12", 30))



#if __name__ == '__main__':