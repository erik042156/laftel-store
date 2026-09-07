from selenium.webdriver.common.by import By


class ExchangeReturnInfoLocators:
    TITLE = (By.XPATH, '//h1[normalize-space(.)="교환/반품 안내"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="교환/반품 안내"]/ancestor::div[@role="dialog"]')
