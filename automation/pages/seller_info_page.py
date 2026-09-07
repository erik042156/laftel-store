from locators.seller_info_locators import SellerInfoLocators
from pages.base_page import BasePage


class SellerInfoPage(SellerInfoLocators, BasePage):
    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
