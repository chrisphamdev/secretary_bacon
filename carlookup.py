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
    
    # obtain the make of the vehicle
    start_index_make = section_text.find('<nobr>')
    end_index_make = section_text.find('</nobr>')
    make = section_text[start_index_make+6:end_index_make]
    make = make[0].upper() + make[1:].lower()
    
    # obtain the model of the vehicle
    section_text = section_text[section_text.find('<span'):] #cut off the already obtained info
    start_index_model = section_text.find('>') + 1
    end_index_model = section_text.find('</span>')
    model = section_text[start_index_model:end_index_model]
    model = model[0].upper() + model[1:].lower()

    # obtain the color of the vehicle
    #cut off the already obtained info
    section_text = section_text[end_index_model:] 
    section_text = section_text[section_text.find('class="thin"'):]
    color_start_index = section_text.find('<nobr>')
    color_end_index = section_text.find('</nobr>')
    color = section_text[color_start_index+6:color_end_index-7].strip()
    
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

    
    return year, make, model, color, cc_rating, photo_url
    
def plate_lookup(plate):
    page_url = 'https://www.carjam.co.nz/car/?plate=' + plate.lower()
    page = get_page(plate)
    year, make, model, color, cc_rating, photo_url = get_make_model_year(page)

    return page_url, year, make, model, color, cc_rating, photo_url


