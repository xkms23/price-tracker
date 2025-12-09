from bs4 import BeautifulSoup
# import urllib.request
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3'
} 

def get_html(url_):
    response = requests.get(url_, headers=HEADERS)
    text = response.text
    return text

# Implementation using urllib.request

# def get_html(url_):
#     fp = urllib.request.urlopen(url_)
#     mbytes = fp.read()
#     html = mbytes.decode("utf-8")
#     fp.close()
#     return html

def get_soup(url_):
    soup = get_html(url_)
    return BeautifulSoup(soup, 'html.parser')

def get_amazon_price(url_):
    soup = get_soup(url_)
    price_whole = soup.find('span', 'a-price-whole').get_text()[:-1]
    price_fraction = soup.find('span', 'a-price-fraction').get_text()
    price = float(f'{price_whole}.{price_fraction}')
    return price

available_sites = {
    "www.amazon.": (get_amazon_price, [])
}

url = input("Enter the URL\n")

for k, v in available_sites.items():
    if k in url:
        func, arg =  v
        price = func(url)
        print(price)



