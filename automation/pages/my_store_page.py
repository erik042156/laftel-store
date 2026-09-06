from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage

_STATUS_BADGE_LABELS = {"품절", "판매종료", "예약구매", "NEW"}


class MyStorePage(BasePage):
    WISH_MENU_BADGE_COUNT = (By.XPATH, '//span[starts-with(normalize-space(.), "찜")]/span')
    WISH_MENU_LINK = (By.XPATH, '//button[.//span[normalize-space(.)="찜"]]')
    LOGIN_PROMPT_HEADING = (By.XPATH, '//h2[normalize-space(.)="로그인 후 이용해 주세요."]')
    LOGIN_PROMPT_CANCEL_BUTTON = (By.XPATH, '//button[normalize-space(.)="취소"]')
    LOGIN_PROMPT_LOGIN_BUTTON = (By.XPATH, '//button[normalize-space(.)="로그인"]')

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

    def get_current_url(self):
        return self.driver.current_url

    def _first_product_link_after_heading(self, heading_text):
        return (
            By.XPATH,
            f'//h2[normalize-space(.)="{heading_text}"]/following::a[starts-with(@href, "/products/")][1]',
        )

    def _section_card_locator(self, heading_text, index=1):
        return (
            By.XPATH,
            f'//h2[normalize-space(.)="{heading_text}"]/following::a[starts-with(@href, "/products/")][{index}]',
        )

    def _section_card_wish_icon_locator(self, heading_text, index=1):
        return (
            By.XPATH,
            f'//h2[normalize-space(.)="{heading_text}"]/following::a[starts-with(@href, "/products/")]'
            f'[{index}]//button[@aria-label="찜하기" or @aria-label="찜 해제"]',
        )

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
        links = self.driver.find_elements(
            By.XPATH, '//h2[normalize-space(.)="찜한 상품"]/following::a[starts-with(@href, "/products/")]'
        )
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
        for span in card.find_elements(By.XPATH, ".//span[not(*)]"):
            if span.text in _STATUS_BADGE_LABELS:
                return span.text
        return None
