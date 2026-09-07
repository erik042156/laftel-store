from selenium.webdriver.common.by import By


class ProductInfoLocators:
    TITLE = (By.XPATH, '//h1[normalize-space(.)="상품정보 제공고시"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="상품정보 제공고시"]/ancestor::div[@role="dialog"]')
