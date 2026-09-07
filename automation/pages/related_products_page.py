from locators.related_products_locators import RelatedProductsLocators
from pages.base_page import BasePage


class RelatedProductsPage(RelatedProductsLocators, BasePage):
    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_grid_item_count(self):
        return len(self.driver.find_elements(*self.GRID_ITEM_LINKS))
