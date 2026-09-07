from locators.exchange_return_info_locators import ExchangeReturnInfoLocators
from pages.base_page import BasePage


class ExchangeReturnInfoPage(ExchangeReturnInfoLocators, BasePage):
    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
