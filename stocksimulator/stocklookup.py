# This module handles the web scraping process, the data is obtained from marketwatch.com

from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup as soup
import ssl
from yahoo_fin import stock_info


class Stock:
    def __init__(self, symbol, company_name, current_price, logo_url, url):
        self.symbol = symbol.upper()
        self.company_name = company_name
        self.current_price = round(current_price, 2)
        self.logo_url = logo_url

    def __str__(self):
        return '{} {} {}'.format(self.company_name, self.symbol, self.current_price)
    
    def __repr__(self):
        return __str__(self)

def get_stock_page(symbol):
    #ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://www.tradingview.com/symbols/{}'.format(symbol)
    client = urllib.request.urlopen(url)
    page_html = client.read()
    client.close()
    page_html_parsed = soup(page_html, 'html.parser')
    return page_html_parsed


# get information from stock symbol, return an object of Stock class
def get_info(symbol):
    page_html = get_stock_page(symbol)

    symbol = symbol.upper()

    url = 'https://www.tradingview.com/symbols/{}'.format(symbol)

    # get company logo
    company_logo = str(page_html.findAll('img', {'class':'tv-circle-logo tv-circle-logo--large tv-category-header__icon'}))
    company_logo_start_index = company_logo.find('src="') + 5
    from_start_index_to_end = company_logo[company_logo_start_index:]
    company_logo_end_index = from_start_index_to_end.find('"')
    logo_url = from_start_index_to_end[:company_logo_end_index]

    # get company name
    company_name = str(page_html.findAll('div', {'class':'tv-symbol-header__first-line'}))
    company_name_start_index = company_name.find('line"') + 6
    company_name_end_index = company_name.find('</div>')
    company_name = company_name[company_name_start_index:company_name_end_index]

    # get current price, change and change in percentage
    #current_price, current_change, current_change_percent = update_price(symbol)
    current_price = stock_info.get_live_price(symbol)

    return Stock(symbol, company_name, current_price, logo_url, url)
