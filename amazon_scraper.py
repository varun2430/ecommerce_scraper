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
        except Exception as err:
            print("unabel to get product title")
            print(err)
        return title.strip()


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
        except Exception as err:
            print("unable to get product price")
            print(err)
        return price


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
    
    URL = [ "https://www.amazon.in/dp/1526651637/ref=s9_acsd_al_bw_c2_x_5_t?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=TAQ8R2DB8W3XXH6G019A&pf_rd_t=101&pf_rd_p=c94ab90f-f846-4a79-bfd4-9277e12942be&pf_rd_i=976389031",
    "https://www.amazon.in/gp/product/B096VD213D/ref=s9_acss_bw_cg_WLM_3b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-6&pf_rd_r=5A3XDM8A18H5WGCJJHY2&pf_rd_t=101&pf_rd_p=899c625b-c7ed-4c88-8b7e-ae7bf2e7e58d&pf_rd_i=1389401031",
    "https://www.amazon.in/Jack-Jones-Mens-T-Shirt-2422204036_Coral_Medium/dp/B099FDNH5F/ref=sr_1_3?pf_rd_i=6648217031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=0485126c-6a8c-4591-8258-48e87a7c150a&pf_rd_r=CX6NR4SF6YJ812M4Q3WM&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1645787291&refinements=p_36%3A-39900%2Cp_72%3A1318476031%2Cp_85%3A10440599031&rnid=10440598031&rps=1&s=apparel&sr=1-3",
    "https://www.amazon.in/SanDisk-Ultra-Drive-Flash-128GB/dp/B084PJSSQ1/ref=Oct_d_obs_1375411031?pd_rd_i=B084PJSSQ1&pd_rd_r=e9ba37ba-2ee4-4ddb-829d-cbd1e08d5049&pd_rd_w=Y8nu4&pd_rd_wg=OSU3z&pf_rd_p=452e6737-1f7b-494e-b8b1-21478ecbd714&pf_rd_r=DZ0PAN1CFJ3DNJT4JS6Q",
    "https://www.amazon.in/Casio-FX-991EX-Scientific-Calculator-Black/dp/B011UK5DGY/ref=zg-bs_office_4/262-2961657-4032542?pd_rd_w=AEip5&pf_rd_p=56cde3ad-3235-46d2-8a20-4773248e8b83&pf_rd_r=FJ980AQVQ9K7KKZYJFH4&pd_rd_r=5debcdbb-313f-4ab7-bdca-2c5960f28715&pd_rd_wg=tLKOx&pd_rd_i=B011UK5DGY&psc=1"]

    for url in URL:
        print("")
        amz = AmazonAPI()
        amz.get_product_info(url)