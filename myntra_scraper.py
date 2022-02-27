import json
import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Request
def get_headers():
    return {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

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

def get_pdpData_script(soup):
    for s in soup.find_all("script"):
        if 'pdpData' in s.text:
            script = s.get_text(strip=True)
            break
    return script

# Format
def price_to_float(price):
    return Decimal(re.sub(r'[^\d.]', '', price))

def script_to_JSON(script):
    return (json.loads(script[script.index('{'):]))["pdpData"]





class MyntraAPI:
    def __init__(self):
        pass

    def get_productID(self, product_data):
        return product_data["id"]

    def get_baseURL(self, pid):
        return "https://www.myntra.com/" + str(pid)

    def get_productTitle(self, product_data):
        try:
            title = product_data["name"]
            return title
        except Exception as err:
            print("unable to get product title")
            print(err)

    
    def get_productPrice(self, product_data):
        try:
            price = product_data["price"]["discounted"]
            return Decimal(price)
        except Exception as err:
            print("unable to get product price")
            print(err)


    def get_product_info(self, URL):
        self.soup = get_soup(URL)
        try:
            self.product_data = script_to_JSON(get_pdpData_script(self.soup))
        except Exception as err:
            print("unable to get pdpData")
            print(err)
            quit()

        self.pid = self.get_productID(self.product_data)
        self.product_title = self.get_productTitle(self.product_data)
        self.product_price = self.get_productPrice(self.product_data)

        print(self.pid)
        print(self.product_title)
        print(self.product_price)
        print(self.get_baseURL(self.pid))





if __name__ == "__main__":

    URL = ["https://www.myntra.com/shirts/highlander/highlander-black-slim-fit-casual-shirt/1265389/buy",
    "https://www.myntra.com/sweatshirts/adidas/adidas-men-black-solid-crew-3s-sweatshirt/12946394/buy",
    "https://www.myntra.com/tshirts/hm/hm-men-green-solid-regular-fit-round-neck-t-shirt/16590968/buy",
    "https://www.myntra.com/shirts/park-avenue/park-avenue-men-black-slim-fit-formal-shirt/16550160/buy",
    "https://www.myntra.com/blazers/van-heusen/van-heusen-men-charcoal-grey-slim-fit-checked-single-breasted-formal-blazer/16887280/buy"]

    for url in URL:
        print("")
        myt = MyntraAPI()
        myt.get_product_info(url)