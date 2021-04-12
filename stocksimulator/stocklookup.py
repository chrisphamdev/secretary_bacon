# This module handles the web scraping process, the data is obtained from marketwatch.com

from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup as soup
import ssl

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

def get_stock_page(symbol):
    #ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://www.marketwatch.com/investing/stock/{}'.format(symbol)
    client = urllib.request.urlopen(url)
    page_html = client.read()
    client.close()
    page_html_parsed = soup(page_html, 'html.parser')
    return page_html_parsed

def update_price(symbol):
    page_html = get_stock_page(symbol)
    # get current price
    current_price = str(page_html.findAll('h3', {'class':'intraday__price'})[0])
    current_price_start = current_price.rfind('">') + 2
    current_price_end = current_price.find('</bg-quote>')
    current_price = current_price[current_price_start:current_price_end]
    current_price = current_price.replace(',', '')
    current_price = float(current_price)
    
    # get current change
    current_change = str(page_html.findAll('span', {'class':'change--point--q'})[0])
    current_change_start = current_change.rfind('">') + 2
    current_change_end = current_change.find('</bg-quote>')
    current_change = float(current_change[current_change_start:current_change_end])

    # get current change in percent
    current_change_percent = str(page_html.findAll('span', {'class':'change--percent--q'})[0])
    current_change_percent_start = current_change_percent.rfind('">') + 2
    current_change_percent_end = current_change_percent.find('</bg-quote>')
    current_change_percent = float(current_change_percent[current_change_percent_start:current_change_percent_end-1])

    return current_price, current_change, current_change_percent

# get information from stock symbol, return an object of Stock class
def get_info(symbol):
    page_html = get_stock_page(symbol)

    url = 'https://www.marketwatch.com/investing/stock/{}'.format(symbol)
    # get stock name, company name, market
    stock_info_elm = page_html.findAll('div', {'class':'element element--company'})[0]

    # get ticker
    company_ticker = str(stock_info_elm.findAll('span', {'class':'company__ticker'})[0])
    company_ticker_start_index = company_ticker.find('ticker">') + len('ticker">')
    company_ticker_end_index = company_ticker.find('</span>')
    company_ticker = company_ticker[company_ticker_start_index:company_ticker_end_index]
    
    # get market
    company_market = str(stock_info_elm.findAll('span', {'class':'company__market'})[0])
    company_market_start_index = company_market.find('market">') + len('market">')
    company_market_end_index = company_market.find('</span>')
    company_market = company_market[company_market_start_index:company_market_end_index]
    
    # get company name
    company_name = str(stock_info_elm.findAll('h1', {'class':'company__name'})[0])
    name_start_index = company_name.find('name">') + len('name">')
    name_end_index = company_name.find('</h1>')
    company_name = company_name[name_start_index:name_end_index]
    
    # get current price, change and change in percentage
    current_price, current_change, current_change_percent = update_price(symbol)

    return Stock(symbol, company_name, current_price, current_change, current_change_percent, company_market, url)

print(get_info('AMZN'))
