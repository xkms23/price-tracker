from bs4 import BeautifulSoup
import requests
import cloudscraper

class BaseScraper:
    def __init__(self):
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'Accept' : 'application/x-clarify-gzip',
            #'Accept-Encoding' : 'gzip, deflate, br'
        }
        self.adv = False

    def get_html(self, url):
        r = requests.post(url, headers=self.HEADERS)
        return r.text

    def get_html_advanced(self, url):
        r = cloudscraper.create_scraper(delay=10).get(url)
        return r.text

    def get_soup(self, url, adv):

        if adv:

        test = BeautifulSoup(self.get_html(url), 'html.parser')
        if test.title.text == 'Just a moment...':
            return BeautifulSoup(self.get_html_advanced(url), 'html.parser')
        return BeautifulSoup(self.get_html(url), 'html.parser')

    def get_price(self):
        pass

class AmazonScraper(BaseScraper):
    def __init__(self, url, adv):
        super().__init__()
        self.url = url
        self.adv = adv

    def get_price(self):
        soup = self.get_soup(self.url)
        price_whole = soup.find('span', 'a-price-whole').get_text()[:-1]
        price_fraction = soup.find('span', 'a-price-fraction').get_text()
        return float(f'{price_whole}.{price_fraction}')

class XKomScraper(BaseScraper):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_price(self):
        soup = self.get_soup(self.url)
        print(soup.prettify())
        price = float(soup.find('span', 'parts__ScreenReaderPrice-sc').get_text()[6:15].replace(' ', '').replace(',', '.'))
        return price

class App:
    def __init__(self):
        self.available_sites = {
            "www.amazon.": (AmazonScraper, []),
            "www.x-kom.pl" : (XKomScraper, [])
        }
        self.start()

    def start(self):
        url = input("Enter the URL:\n")

        for k, v in self.available_sites.items():
            if k in url:
                Scraper, arg = v
                price = Scraper(url).get_price()
                print(price)

if __name__ == '__main__':
    App()
