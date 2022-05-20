from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup as soup
import ssl

def get_page(plate):
    ssl._create_default_https_context = ssl._create_unverified_context
    page_url = 'https://www.carjam.co.nz/car/?plate=' + plate
    client = urllib.request.urlopen(page_url)
    profile_html = client.read()
    client.close()
    page_html_parsed = soup(profile_html, 'html.parser')
    return page_html_parsed

def get_make_model_year(page):
    # obtain the section where make-model-year are located
    section = page.findAll('div', {'class':'col-md-12'})
    section_text = str(section)

    # obtain the year of the vehicle
    last_index_year = section_text.find('</a>')
    year = section_text[last_index_year-4:last_index_year]

    
page = get_page('BZF512')
get_make_model_year(page)