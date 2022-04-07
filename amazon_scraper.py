import re

from utils import get_soup, get_page, price_to_str




def get_apexDesktop(soup):
    return soup.find("div", id="apex_desktop")


def get_apexPriceToPay(soup):
    return soup.find(class_="apexPriceToPay")


def get_priceToPay(soup):
    return soup.find("span", class_="priceToPay")


def get_price(soup):
    return soup.find("span", id="price")


def get_product_name(soup):
    return soup.find("span", id="productTitle")


def get_product_price(soup):
    apexDesktop_soup = get_apexDesktop(soup)
    if get_price(soup):
        price = get_price(soup)
    elif get_apexPriceToPay(apexDesktop_soup):
        price = get_apexPriceToPay(apexDesktop_soup).find("span")
    elif get_priceToPay(apexDesktop_soup):
        price = get_priceToPay(apexDesktop_soup).find("span")
    return price




class Amazon:
    def __init__(self):
        pass


    def get_productASIN(self, URL):
        asin = re.search(r"/([a-zA-Z0-9]{10})(?:[/?]|$)", URL)
        return asin.group(1)


    def get_baseURL(self, product_id):
        return "https://www.amazon.in/dp/" + product_id


    def get_product_data(self, URL):
        try:
            self.product_id = self.get_productASIN(URL)
            self.base_url = self.get_baseURL(self.product_id)
        except Exception as err:
            print("Invalid URL")

        try:
            self.content = get_page(self.base_url)
            self.soup = get_soup(self.content)
        except Exception as err:
            print("Unable to get soup/page content")

        try:
            self.product_name = get_product_name(self.soup).text.strip()
            self.product_price = price_to_str(get_product_price(self.soup).text)
        except Exception as err:
            print("Unable to get product data")

        print(self.base_url)
        print(self.product_id)
        print(self.product_name)
        print(self.product_price)