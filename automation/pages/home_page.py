from config.settings import BASE_URL
from locators.home_locators import HomeLocators
from pages.base_page import BasePage


class HomePage(HomeLocators, BasePage):
    def open(self):
        self.driver.get(BASE_URL)

    def click_search_entry(self):
        self.click(self.SEARCH_ENTRY)

    def open_search_result(self, keyword):
        self.driver.get(f"{BASE_URL}search?keyword={keyword}")

    def open_ip_page(self, ip_id):
        self.driver.get(f"{BASE_URL}ip/{ip_id}")

    def click_wish_icon(self, index=1):
        self.click(self.wish_icon_locator(index))

    def is_wish_icon_filled(self, index=1):
        return self._wait(self.wish_icon_locator(index)).get_attribute("aria-pressed") == "true"

    def wait_for_wish_icon_state(self, index, filled):
        self.wait_for_attribute_value(self.wish_icon_locator(index), "aria-pressed", "true" if filled else "false")

    def get_login_prompt_text(self):
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def get_wish_toast_text(self):
        self.wait_for_text(self.WISH_TOAST, "찜")
        return self.get_text(self.WISH_TOAST)
