from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductInfoPage(BasePage):
    TITLE = (By.XPATH, '//h1[normalize-space(.)="상품정보 제공고시"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="상품정보 제공고시"]/ancestor::div[@role="dialog"]')

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
