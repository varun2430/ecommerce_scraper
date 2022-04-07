

from utils import get_page, get_soup



class Flipkart:
    def __init__(self):
        pass


    def get_product_data(self, URL):
        try:
            self.content = get_page(URL)
            self.soup = get_soup(self.content)
        except Exception as err:
            print("Unable to get soup/page content")
