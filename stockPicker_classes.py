# Base class: basic element of portfolio, inherting classes form the whole portfolio
class Portfolio:
    """Represents the basket of all investments (varible amount of titles)"""
    def __init__(self, *titles):
        self.titles = titles

#TODO: the organization needs to be rearranged;
# Saving plans need to be split up into single titles and differentiation between
# titles with data from the internet and investment with known interest
# otherwise there needs to be complicated de- and reconstruction done 


# Base class for general investment as a part of the portfolio
class Title:
    """Represents a general title in a portfolio"""
    def __init__(self, name):
        """Initialization with name"""
        self.name = name

# following class inherits from Title: One time traded part of portfolio (can only be bought as a whole)
class OneDateBuy(Title):
    """Represents an active or passive managed fund (ETF), can be traded """
    def __init__(self, name, number, buy_date):
        Title.__init__(self, name)
        self.number = number
        self.buy_date = buy_date 

# inherting class for regulary occurring buys eg. a saving plan
class SavingPlan(Title):
    """Represents a saving plan (deposit account or denominated funds)"""
    def __init__(self, name, value, start_date, end_date, period):
        """Initialization with basic information (period in days)""" 
        Title.__init__(self, name)
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        self.period = period

# inheriting class for funds, whose values need to be checked online
class FundSavingPlan(SavingPlan):
    """Represents a saving plan for active or passivly traded funds"""
    def __init__(self, name, value, start_date, end_date, period):
        SavingPlan.__init__(self, name, value, start_date, end_date, period)


# inheriting class for an investment with known interest
class AccountSavingPlan(SavingPlan):
    """Represents a saving plan for account, where the interest is known"""
    def __init__(self, name, value, start_date, end_date, period, interest):
        """Initialization with basic information (period in days, 
        interest in percent per year)""" 
        SavingPlan.__init__(self, name, value, start_date, end_date, period)
        self.interest = interest

#TODO: split title in different types of titles: Stocks (single buy), deposit account, Fund- / ETF-savings plan (periodic buy)
#this module contains the information about the titles of a portfolio (list of titles)
#the title can have different attributes:
#   - name: Short name for title eg. MSFT for Microsoft 
#   - buy_date: date when title was first bought the first time
#   - buy_amount: number of stocks or price of ETFs/ Funds
#   - period: interval, in which the title is bought (1d, 5d, etc.)
#   - etc. (depending on type of title)
#   -> target is to deploy portfolio to the script which handles the data analysis