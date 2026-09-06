from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ExchangeReturnInfoPage(BasePage):
    TITLE = (By.XPATH, '//h1[normalize-space(.)="교환/반품 안내"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="교환/반품 안내"]/ancestor::div[@role="dialog"]')

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
