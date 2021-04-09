# This class represents a share on the market
from .stocklookup import update_price

class Stock:
    def __init__(self, symbol, company_name, current_price, current_change, current_change_percent, market, url):
        self.symbol = symbol.upper()
        self.company_name = company_name
        self.current_price = current_price
        self.current_change = current_change
        self.current_change_percent = current_change_percent
        self.market = market

    def price_update(self):
        self.current_price, self.current_change, self.current_change_percent = update_price(self.symbol)

    def __str__(self):
        return '{} {} {}%'.format(self.symbol, self.current_price, self.current_change_percent)
    
    def __repr__(self):
        return __str__(self)