import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Request
def get_headers():
    return {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'}

def get_page_content(URL):
    try:
        page_content = requests.get(URL, headers=get_headers(), verify=False).content
    except Exception as err:
        print("unable to get page content")
        print(err)
        quit()
    return page_content

# BS4
def get_soup(URL):
    try:
        soup = BeautifulSoup(get_page_content(URL), "html.parser")
    except Exception as err:
        print("bs4 error")
        print(err)
        quit()
    return soup

def get_productTitle_span(soup):
    return soup.find("span", class_="B_NuCI")

def get_productPrice_div(soup):
    return soup.find("div", class_="_30jeq3 _16Jk6d")


# Format
def price_to_float(price):
    return Decimal(re.sub(r'[^\d.]', '', price))





class FlipkartAPI:
    def __init__(self):
        pass


    def get_baseURL(self, URL):
        return URL[:URL.index("&lid")]

    def get_productID(self, base_url):
        pid = re.search(r"=([a-zA-Z0-9]{16})", base_url)
        return pid.group(1)


    def get_productTitle(self, soup):
        try:
            title = get_productTitle_span(soup).text
        except Exception as err:
            print("unable to get product title")
            print(err)
        return title

    
    def get_productPrice(self, soup):
        try:
            price = get_productPrice_div(soup).text
            price = price_to_float(price)           
        except Exception as err:
            print("unable to get product price")
            print(err)
        return price


    def get_product_info(self, URL):
        try:
            self.base_url = self.get_baseURL(URL)
            self.pid = self.get_productID(self.base_url)
        except Exception as err:
            print("invalid url")
            print(err)
            quit()

        self.soup = get_soup(self.base_url)
        self.product_title = self.get_productTitle(self.soup)
        self.product_price = self.get_productPrice(self.soup)

        print(self.pid)
        print(self.product_title)
        print(self.product_price)






if __name__ == "__main__":

    URL = "https://www.flipkart.com/yonex-mavis-200i-green-cap-nylon-shuttle-yellow/p/itmf3y44hzvgzb3q?pid=STLEKPFGJRHZHGHR&lid=LSTSTLEKPFGJRHZHGHRS3L7QV&marketplace=FLIPKART&store=abc%2Fegs&srno=b_1_4&otracker=browse&fm=organic&iid=f41c966a-560e-494b-8b9b-847776ee49b4.STLEKPFGJRHZHGHR.SEARCH&ppt=browse&ppn=browse&ssid=uhtzrywf7k0000001645780313523"

    flk = FlipkartAPI()
    flk.get_product_info(URL)