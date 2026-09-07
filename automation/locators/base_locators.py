from selenium.webdriver.common.by import By


class BaseLocators:
    STATUS_BADGE_SPAN = (By.XPATH, ".//span[not(*)]")
