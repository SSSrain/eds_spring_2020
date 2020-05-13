import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def parse_page(search, page):
    ffox = webdriver.Firefox()

    url = 'https://www.avito.ru/moskva/'

    ffox.get(url)

    search_field = ffox.find_element_by_id('search')
    search_field.send_keys('{}'.format(search))

    search_button = ffox.find_element_by_class_name(
        'index-buttonElement-3wfmP.button-button-2Fo5k.button-size-s-3-rn6.button-default-mSfac')
    search_button.click()

    cur_url = ffox.current_url
    url = cur_url + '&p={}'.format(page)
    ffox.get(url)
    ffox.close()


    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    advertisement = soup.find_all('div', {'class': 'item__line'})

    data = []

    for adv in advertisement:

        price = (adv.find('span', {'class': 'snippet-price'}).get_text().strip())
        title = (adv.find('a', {'class': 'snippet-link'}).get_text().strip())
        link = ('https://www.avito.ru' + (adv.find('a', {'class': 'snippet-link'}).get('href')))
        try:
            metro = (adv.find('span', {'class': 'item-address-georeferences-item__content'}).get_text().strip())
        except:
            metro = (None)
        try:
            distance = (adv.find('span', {'class': 'item-address-georeferences-item__after'}).get_text().strip())

        except:
            distance = (None)

        data.append({'title': title, 'price': price,
                     'metro': metro, 'distance': distance, 'link': link})

    return data


search = 'сибирская кошка'
page = '2'

result = pd.DataFrame(parse_page(search, page))
result = result.sort_values('price')
print(result)
