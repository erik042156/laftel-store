from locators.not_found_locators import NotFoundLocators
from pages.base_page import BasePage


class NotFoundPage(NotFoundLocators, BasePage):
    def get_message_text(self):
        return self.get_text(self.MESSAGE_HEADING)
