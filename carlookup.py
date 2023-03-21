from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup as soup
import ssl

def get_page(plate):
    ssl._create_default_https_context = ssl._create_unverified_context
    page_url = 'https://www.carjam.co.nz/car/?plate=' + plate
    req = Request(
        url=page_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    page_html_parsed = soup(webpage, 'html.parser')
    return page_html_parsed

def get_make_model_year(page):
    # obtain the section where make-model-year are located
    section = str(page.findAll('div', {'class':'report-section vehicle-section'})).split()
    all_values = []
    for char in section:
        if 'class="value">' in char:
            all_values += [char[14:-7]]
    try:
        all_values = all_values[:6]
        year, make, model, color, submodel, car_type = all_values[0], all_values[1], all_values[2], all_values[3], all_values[4], all_values[5]
    finally:
        year, make, model, color = all_values[0], all_values[1], all_values[2], all_values[3]

    # obtain the CC rating
    cc_rating_lookup = str(page.findAll('span', {'class':'value'}))
    cc_start_index = cc_rating_lookup.find('cc')
    cc_rating = cc_rating_lookup[cc_start_index-5:cc_start_index]

    # obtain a photo of the car
    photo_lookup = str(page.findAll('div', {'class':'thumbnail'}))
    photo_start_index = photo_lookup.find('src=') + 5
    photo_end_index = photo_start_index + photo_lookup[photo_start_index:].find('"')
    photo_url = photo_lookup[photo_start_index:photo_end_index]
    if photo_url[0:2] == '//':
        photo_url = 'https:' + photo_url

    
    return year, make, model, color, submodel, car_type, cc_rating, photo_url
    
def plate_lookup(plate):
    page_url = 'https://www.carjam.co.nz/car/?plate=' + plate.lower()
    page = get_page(plate)
    year, make, model, color, submodel, car_type, cc_rating, photo_url = get_make_model_year(page)

    return year, make, model, color, submodel, car_type, cc_rating, photo_url, page_url

print(plate_lookup('bzf512'))