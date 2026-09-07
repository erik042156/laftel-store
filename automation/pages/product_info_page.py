from locators.product_info_locators import ProductInfoLocators
from pages.base_page import BasePage


class ProductInfoPage(ProductInfoLocators, BasePage):
    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
