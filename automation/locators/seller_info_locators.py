from selenium.webdriver.common.by import By


class SellerInfoLocators:
    TITLE = (By.XPATH, '//h1[normalize-space(.)="판매자 정보"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="판매자 정보"]/ancestor::div[@role="dialog"]')
