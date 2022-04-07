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
        return page_content
    except Exception as err:
        print("unable to get page content")
        print(err)
        quit()

# BS4
def get_soup(URL):
    try:
        soup = BeautifulSoup(get_page_content(URL), "html.parser")
        return soup
    except Exception as err:
        print("bs4 error")
        print(err)
        quit()

def get_productTitle_span(soup):
    return soup.find("span", id="productTitle")

def get_apexDesktop_div(soup):
    return soup.find("div", id="apex_desktop")

def get_apexPriceToPay_class(soup):
    return soup.find(class_="apexPriceToPay")

def get_priceToPay_class(soup):
    return soup.find("span", class_="priceToPay")

def get_price_span(soup):
    return soup.find("span", id="price")

# Format
def price_to_float(price):
    return Decimal(re.sub(r'[^\d.]', '', price))





class AmazonAPI:
    def __init__(self):
        pass
    
    def get_baseURL(self, asin):
        return "https://www.amazon.in/dp/" + asin

    def get_productASIN(slef, URL):
        asin = re.search(r"/([a-zA-Z0-9]{10})(?:[/?]|$)", URL)
        return asin.group(1)

    def get_productTitle(self, soup):
        try:
            title = get_productTitle_span(soup).text
            return title.strip()
        except Exception as err:
            print("unabel to get product title")
            print(err)

    def get_productPrice(self, soup):
        apexDesktop_soup = get_apexDesktop_div(soup)
        try:
            if get_price_span(soup):
                price = get_price_span(soup).text
            elif get_apexPriceToPay_class(apexDesktop_soup):
                price = get_apexPriceToPay_class(apexDesktop_soup).find("span").text
            elif get_priceToPay_class(apexDesktop_soup):
                price = get_priceToPay_class(apexDesktop_soup).find("span").text
            price = price_to_float(price)
            return price
        except Exception as err:
            print("unable to get product price")
            print(err)

    def get_product_info(self, URL):
        try:
            self.asin = self.get_productASIN(URL)
            self.base_url = self.get_baseURL(self.asin)
        except Exception as err:
            print("invalid url")
            print(err)
            quit()

        self.soup = get_soup(self.base_url)
        self.product_title = self.get_productTitle(self.soup)
        self.product_price = self.get_productPrice(self.soup)

        print(self.asin)
        print(self.product_title)
        print(self.product_price)





if __name__ == "__main__":
    
    URL = "https://www.amazon.in/MSI-IPS-Level-Windows-RX5500M-B5DD-077IN/dp/B09BRCHW4B?ref_=Oct_DLandingS_D_794a656e_76&smid=A14CZOWI0VEHLG"

    amz = AmazonAPI()
    amz.get_product_info(URL)