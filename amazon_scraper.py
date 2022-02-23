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
    return soup.find(id="productTitle")

def get_apexDesktop_div(soup):
    return soup.find(id="apex_desktop")

def get_apexPriceToPay_class(soup):
    return soup.find(class_="apexPriceToPay")

def get_priceToPay_class(soup):
    return soup.find(class_="priceToPay")

def get_price_span(soup):
    return soup.find(id="price")

# Format
def price_to_float(price):
    return Decimal(re.sub(r'[^\d.]', '', price))





class AmazonAPI:
    def __init__(self):
        pass


    def get_productASIN(slef, URL):
        asin = re.search(r"/([a-zA-Z0-9]{10})(?:[/?]|$)", URL)
        return asin.group(1)


    def get_productTitle(self, soup):
        try:
            title = get_productTitle_span(soup).string
        except Exception as err:
            print("unabel to get product title")
            print(err)
        return title.strip()


    def get_productPrice(self, soup):
        apexDesktop_soup = get_apexDesktop_div(soup)
        try:
            if get_price_span(soup):
                price = get_price_span(soup).string

            elif get_apexPriceToPay_class(apexDesktop_soup):
                price = get_apexPriceToPay_class(apexDesktop_soup).find("span").string

            elif get_priceToPay_class(apexDesktop_soup):
                price = get_priceToPay_class(apexDesktop_soup).find("span").string
        except Exception as err:
            print("unable to get product price")
            print(err)
        return price_to_float(price)


    def get_product_info(self, URL):

        try:
            self.asin = self.get_productASIN(URL)
            self.base_url = "https://www.amazon.in/dp/" + self.asin
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
    
    URL = "https://www.amazon.in/Previous-Question-Chapterwise-Topicwise-Solutions/dp/B09HTLGSQF/ref=sr_1_6?pf_rd_i=976389031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=1bbcfb5b-c408-4b8e-a900-fbf00d05056f&pf_rd_r=3ET3WSDC3TKAJH8B80GH&pf_rd_s=merchandised-search-8&pf_rd_t=30901&qid=1645617822&refinements=p_85%3A10440599031%2Cp_n_binding_browse-bin%3A9839915031%2Cp_n_availability%3A1318484031&rps=1&s=books&sr=1-6"

    amz = AmazonAPI()
    amz.get_product_info(URL)