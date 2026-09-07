from selenium.webdriver.common.by import By


class NoticeLocators:
    TITLE = (By.XPATH, '//h1[normalize-space(.)="유의사항"]')
    DIALOG_CONTENT = (By.XPATH, '//h1[normalize-space(.)="유의사항"]/ancestor::div[@role="dialog"]')
