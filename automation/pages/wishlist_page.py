from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from locators.wishlist_locators import WishlistLocators
from pages.base_page import BasePage


class WishlistPage(WishlistLocators, BasePage):
    def open(self):
        self.driver.get(f"{BASE_URL}my/wish")

    def click_first_item(self):
        self.click(self.FIRST_ITEM_PRODUCT_LINK)

    def click_product_tab(self):
        self.click(self.PRODUCT_TAB)

    def click_work_tab(self):
        self.click(self.WORK_TAB)

    def is_edit_link_present(self):
        return any(link.is_displayed() for link in self.driver.find_elements(*self.EDIT_LINK))

    def wait_for_edit_link_hidden(self):
        # 탭 전환 시 패널이 화면에서 사라지기까지 약간의 렌더링 지연이 있어 즉시
        # 판정하면 간헐적으로 실패할 수 있다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_edit_link_present())

    def is_product_present(self, product_id):
        links = self.driver.find_elements(*self.FIRST_ITEM_PRODUCT_LINK)
        return any(f"/products/{product_id}" in link.get_attribute("href") for link in links)

    def wait_for_product_present(self, product_id):
        # SPA 초기 진입 직후에는 상품 목록이 비동기로 채워지므로, 목록이 실제로
        # 렌더링될 때까지 기다린 뒤 판정한다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: self.is_product_present(product_id))

    def wait_for_product_absent(self, product_id):
        # "작품" 탭에서 찜 해제 후 "상품" 탭으로 전환하면 반영까지 약간의 지연이 있어
        # (실측 약 0.5초), 전환 직후 즉시 판정하면 간헐적으로 실패할 수 있다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_product_present(product_id))

    def click_work_section_title(self, index=1):
        self.click(self._work_section_title_link_locator(index))

    def click_work_section_heart(self, index=1):
        self.click(self._work_section_heart_locator(index))

    def click_product_wish_icon(self, product_id):
        self.click(self._product_wish_icon_locator(product_id))

    def is_product_wish_icon_filled(self, product_id):
        return self._wait(self._product_wish_icon_locator(product_id)).get_attribute("aria-pressed") == "true"

    def wait_for_product_wish_icon_state(self, product_id, filled):
        self.wait_for_attribute_value(
            self._product_wish_icon_locator(product_id), "aria-pressed", "true" if filled else "false"
        )

    def find_work_section_index(self, ip_id):
        sections = self.driver.find_elements(*self.WORK_SECTION)
        for i, section in enumerate(sections, start=1):
            if f'/ip/{ip_id}"' in section.get_attribute("innerHTML"):
                return i
        return None

    def is_work_section_present(self, ip_id):
        return self.find_work_section_index(ip_id) is not None

    def wait_for_work_section_present(self, ip_id):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: self.is_work_section_present(ip_id))

    def wait_for_work_section_absent(self, ip_id):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_work_section_present(ip_id))

    def get_product_status_badge_text(self, product_id):
        card = self._wait(self.product_link_locator(product_id))
        return self.get_status_badge_text(card)

    def click_product(self, product_id):
        self.click(self.product_link_locator(product_id))

    def get_login_prompt_text(self):
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def click_login_prompt_cancel(self):
        self.click(self.LOGIN_PROMPT_CANCEL_BUTTON)

    def click_login_prompt_login(self):
        self.click(self.LOGIN_PROMPT_LOGIN_BUTTON)

    def click_edit_link(self):
        self.click(self.EDIT_LINK)
        # "편집하기" 클릭 시 BasePage.click()의 scrollIntoView로 스크롤 위치가 변경되어,
        # 편집 모드 헤더("전체 선택" 등)가 뷰포트 밖/다른 요소에 가려진 상태로 남아
        # element_to_be_clickable이 영구 타임아웃될 수 있다. 최상단으로 복귀시켜 해결한다.
        self.driver.execute_script("window.scrollTo(0, 0);")
        self._wait(self.SELECT_ALL_CHECKBOX)  # 편집 모드 헤더가 렌더링될 때까지 대기

    def click_cancel_edit(self):
        self.click(self.CANCEL_EDIT_LINK)
        self._wait(self.EDIT_LINK)  # 편집 모드 해제(일반 화면 복귀) 대기

    def click_delete_selected(self):
        self.click(self.DELETE_SELECTED_LINK)

    def get_delete_confirm_dialog_text(self):
        # headless 환경에서는 WebElement.text가 렌더링 가시성 판정에 실패해 빈 문자열을
        # 반환하는 경우가 있어(AUTOMATION_GUIDE 7.15절과 동일 패턴), get_attribute
        # ("textContent")로 대체한다.
        return self._wait(self.DELETE_CONFIRM_DIALOG).get_attribute("textContent")

    def confirm_delete(self):
        self.click(self.DELETE_CONFIRM_BUTTON)

    def cancel_delete(self):
        self.click(self.DELETE_CANCEL_BUTTON)

    def click_select_all(self):
        # element_to_be_clickable(가시성 요구)가 이 버튼에서는 영구 타임아웃되는
        # 현상이 있어(원인 불명, AUTOMATION_GUIDE 7.15절), 존재 확인 후 JS로 클릭한다.
        self.click_via_js(self.SELECT_ALL_CHECKBOX)

    def get_selected_count_text(self):
        # 이 span은 .text(가시성 기반) 판정이 불안정해(AUTOMATION_GUIDE 7.15절)
        # textContent를 직접 읽는다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: "(" in (driver.find_element(*self.SELECTED_COUNT_TEXT).get_attribute("textContent") or "")
        )
        return self._wait(self.SELECTED_COUNT_TEXT).get_attribute("textContent")

    def click_item_card(self, index=1):
        self.click(self.item_card_locator(index))

    def is_item_selected(self, index=1):
        return self._wait(self.item_card_locator(index)).get_attribute("aria-pressed") == "true"

    def get_item_card_count(self):
        return len(self.driver.find_elements(*self.ITEM_CARD))
