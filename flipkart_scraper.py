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

    URL = [ "https://www.flipkart.com/acer-aspire-7-core-i5-10th-gen-8-gb-512-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-a715-75g-50ta-a715-75g-41g-a715-75g-52aa-gaming-laptop/p/itm365d5a348ad9c?pid=COMG2KBG2K4GFFF7&lid=LSTCOMG2KBG2K4GFFF78YBPHO&marketplace=FLIPKART&store=4rr%2Ftz1&spotlightTagId=BestvalueId_4rr%2Ftz1&srno=b_1_3&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=c414703c-341a-4ce0-94f4-293ace434103.COMG2KBG2K4GFFF7.SEARCH&ppt=browse&ppn=browse&ssid=udduxj3zgw0000001645786871745",
    "https://www.flipkart.com/asus-vivobook-gaming-core-i5-9th-gen-8-gb-1-tb-hdd-256-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-f571gt-hn1062t-laptop/p/itm17141ef4f3a14?pid=COMG5QHN77MU7AGD&lid=LSTCOMG5QHN77MU7AGD4M21N0&marketplace=FLIPKART&store=4rr%2Ftz1&srno=b_1_4&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=c414703c-341a-4ce0-94f4-293ace434103.COMG5QHN77MU7AGD.SEARCH&ppt=browse&ppn=browse",
    "https://www.flipkart.com/acer-aspire-7-ryzen-5-hexa-core-5500u-8-gb-512-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-a715-42g-gaming-laptop/p/itm4385fddc2c72c?pid=COMGYCG8ZBXWPYUU&lid=LSTCOMGYCG8ZBXWPYUUYQDSM8&marketplace=FLIPKART&store=4rr%2Ftz1&srno=b_1_5&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=c414703c-341a-4ce0-94f4-293ace434103.COMGYCG8ZBXWPYUU.SEARCH&ppt=browse&ppn=browse",
    "https://www.flipkart.com/asus-tuf-gaming-f17-2021-core-i5-11th-gen-8-gb-1-tb-ssd-windows-10-home-4-gb-graphics-nvidia-geforce-rtx-3050-144-hz-fx706hc-hx070t-laptop/p/itmce7443dfb4e63?pid=COMG3ZF8XHHDEMTV&lid=LSTCOMG3ZF8XHHDEMTVFXM49Y&marketplace=FLIPKART&store=4rr%2Ftz1&srno=b_1_6&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=en_bJtKxD0vLaqn9t9L1ZYawtRkC31hMamj72f8xinBMcWWOdWGvHUS2ij7iyZJ%2FziLdZ1yWtHMXstYG174BU7MCw%3D%3D&ppt=browse&ppn=browse",
    "https://www.flipkart.com/msi-gf63-thin-core-i7-10th-gen-8-gb-1-tb-hdd-256-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-max-q-60-hz-10scxr-1617in-10sc-610in-gaming-laptop/p/itm1e259df16e2f5?pid=COMG2K9ZZYFYGPHZ&lid=LSTCOMG2K9ZZYFYGPHZNV5YXK&marketplace=FLIPKART&store=4rr%2Ftz1&srno=b_1_7&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=c414703c-341a-4ce0-94f4-293ace434103.COMG2K9ZZYFYGPHZ.SEARCH&ppt=browse&ppn=browse" ]

    for url in URL:
        print("")
        flk = FlipkartAPI()
        flk.get_product_info(url)