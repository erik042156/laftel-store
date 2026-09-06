from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RelatedProductsPage(BasePage):
    TITLE = (By.TAG_NAME, "h1")
    GRID_ITEM_LINKS = (By.CSS_SELECTOR, 'a[href^="/products/"]')

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_grid_item_count(self):
        return len(self.driver.find_elements(*self.GRID_ITEM_LINKS))
