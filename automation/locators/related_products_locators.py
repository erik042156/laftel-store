from selenium.webdriver.common.by import By


class RelatedProductsLocators:
    TITLE = (By.TAG_NAME, "h1")
    GRID_ITEM_LINKS = (By.CSS_SELECTOR, 'a[href^="/products/"]')
