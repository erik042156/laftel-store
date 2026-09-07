from config.settings import BASE_URL
from locators.my_store_locators import MyStoreLocators
from pages.base_page import BasePage


class MyStorePage(MyStoreLocators, BasePage):
    def open(self):
        self.driver.get(f"{BASE_URL}my")

    def click_wish_menu(self):
        self.click(self.WISH_MENU_LINK)

    def get_login_prompt_text(self):
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def click_login_prompt_cancel(self):
        self.click(self.LOGIN_PROMPT_CANCEL_BUTTON)

    def click_login_prompt_login(self):
        self.click(self.LOGIN_PROMPT_LOGIN_BUTTON)

    def click_wish_section_product(self):
        self.click(self._first_product_link_after_heading("찜한 상품"))

    def click_recent_section_product(self):
        self.click(self._first_product_link_after_heading("최근 본 상품"))

    def click_recommend_section_product(self):
        self.click(self._first_product_link_after_heading("추천 상품"))

    def get_recent_section_first_product_href(self):
        return self._wait(self._first_product_link_after_heading("최근 본 상품")).get_attribute("href")

    def get_wish_menu_badge_count(self):
        return self.get_text(self.WISH_MENU_BADGE_COUNT)

    def is_wish_section_item_filled(self, index=1):
        return self._wait(self._section_card_wish_icon_locator("찜한 상품", index)).get_attribute("aria-pressed") == "true"

    def is_wish_section_containing_product(self, product_id):
        links = self.driver.find_elements(*self.section_product_links_locator("찜한 상품"))
        return any(f"/products/{product_id}" in link.get_attribute("href") for link in links)

    def is_recent_section_item_filled(self, index=1):
        return self._wait(self._section_card_wish_icon_locator("최근 본 상품", index)).get_attribute("aria-pressed") == "true"

    def click_recent_section_item_wish_icon(self, index=1):
        self.click(self._section_card_wish_icon_locator("최근 본 상품", index))

    def wait_for_recent_section_item_state(self, index, filled):
        self.wait_for_attribute_value(
            self._section_card_wish_icon_locator("최근 본 상품", index), "aria-pressed", "true" if filled else "false"
        )

    def get_recent_section_item_href(self, index=1):
        return self._wait(self._section_card_locator("최근 본 상품", index)).get_attribute("href")

    def get_recent_section_item_status_badge_text(self, index=1):
        card = self._wait(self._section_card_locator("최근 본 상품", index))
        return self.get_status_badge_text(card)
