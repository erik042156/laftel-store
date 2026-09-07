from selenium.webdriver.common.action_chains import ActionChains

from config.settings import BASE_URL
from locators.product_detail_locators import ProductDetailLocators
from pages.base_page import BasePage


class ProductDetailPage(ProductDetailLocators, BasePage):
    def open(self, product_id):
        self.driver.get(f"{BASE_URL}products/{product_id}")

    def click_back(self):
        self.click(self.BACK_BUTTON)

    def click_search_icon(self):
        self.click(self.SEARCH_ICON)

    def click_cart_icon(self):
        self.click(self.CART_ICON)

    def get_login_prompt_text(self):
        # 팝업 요소가 DOM에 나타난 직후에는 텍스트가 아직 채워지지 않은 경우가 있어,
        # 내용이 실제로 채워질 때까지 기다린 뒤 읽는다.
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def click_main_list_product(self):
        self.click(self.MAIN_LIST_PRODUCT_LINK)

    def get_carousel_pagination_text(self):
        return self.get_text(self.CAROUSEL_PAGINATION)

    def _swipe_carousel(self, direction):
        # ChromeDriver W3C Actions의 포인터 상태가 세션 내 반복 드래그에서
        # 누적 이탈(MoveTargetOutOfBoundsException)하는 문제가 있어, 테스트는
        # 페이지를 새로 연 직후 이 메서드를 1회만 호출하는 것을 전제로 한다
        # (AUTOMATION_GUIDE 7.2절).
        viewport = self._wait(self.IMAGE_CAROUSEL_VIEWPORT)
        width = viewport.size["width"]
        offset = int(width * 0.6)
        steps = 6
        delta = (-offset if direction == "next" else offset) // steps
        actions = ActionChains(self.driver)
        actions.move_to_element(viewport).click_and_hold()
        for _ in range(steps):
            actions.move_by_offset(delta, 0)
        actions.release()
        actions.perform()

    def go_to_next_image(self):
        self._swipe_carousel("next")

    def go_to_prev_image(self):
        self._swipe_carousel("prev")

    def click_ip_title_link(self):
        self.click(self.IP_TITLE_LINK)

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self):
        return self.get_text(self.PRODUCT_PRICE)

    def click_related_card(self, index=1):
        self.click(self.related_card_locator(index))

    def click_related_card_wish_icon(self, index=1):
        self.click(self.related_card_wish_icon_locator(index))

    def is_related_card_wish_filled(self, index=1):
        return self._wait(self.related_card_wish_icon_locator(index)).get_attribute("aria-pressed") == "true"

    def click_related_more(self):
        self.click(self.RELATED_MORE_LINK)

    def click_detail_more_toggle(self):
        self.click(self.DETAIL_MORE_TOGGLE)

    def get_detail_toggle_text(self):
        return self.get_text(self.DETAIL_MORE_TOGGLE)

    def click_product_info_accordion(self):
        self.click(self.PRODUCT_INFO_ACCORDION)

    def click_exchange_return_info_accordion(self):
        self.click(self.EXCHANGE_RETURN_INFO_ACCORDION)

    def click_seller_info_accordion(self):
        self.click(self.SELLER_INFO_ACCORDION)

    def click_notice_accordion(self):
        self.click(self.NOTICE_ACCORDION)

    def click_buy_button(self):
        self.click(self.BUY_BUTTON)

    def get_buy_button_text(self):
        return self.get_text(self.BUY_BUTTON)

    def is_buy_button_enabled(self):
        return self._wait(self.BUY_BUTTON).is_enabled()

    def try_click_disabled_buy_button(self):
        # 비활성화된 버튼은 EC.element_to_be_clickable을 절대 만족하지 않으므로
        # 존재 여부만 확인(presence)한 뒤 그대로 클릭을 시도한다.
        self._wait(self.BUY_BUTTON).click()

    def is_bottom_wish_icon_active(self):
        return self._wait(self.BOTTOM_WISH_ICON).is_enabled()

    def click_wish_icon(self):
        self.click(self.BOTTOM_WISH_ICON)

    def is_wish_icon_filled(self):
        return self._wait(self.BOTTOM_WISH_ICON).get_attribute("aria-pressed") == "true"

    def is_option_dropdown_present(self):
        return len(self.driver.find_elements(*self.OPTION_DROPDOWN_TRIGGER)) > 0

    def is_option_dropdown_open(self):
        trigger = self._wait(self.OPTION_DROPDOWN_TRIGGER)
        return trigger.get_attribute("aria-expanded") == "true"

    def click_option_dropdown(self):
        # 옵션 상품은 "구매하기" 클릭 직후 드롭다운이 이미 펼쳐진 상태로 시작하므로,
        # 닫혀 있을 때만 클릭한다(이미 열린 상태에서 클릭하면 오히려 닫혀버림).
        if not self.is_option_dropdown_open():
            self.click(self.OPTION_DROPDOWN_TRIGGER)

    def get_option_items(self):
        return self.driver.find_elements(*self.OPTION_ITEMS)

    def is_option_sold_out(self, index):
        return self.get_option_items()[index].get_attribute("aria-disabled") == "true"

    def click_option_by_index(self, index):
        item = self.get_option_items()[index]
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"});', item)
        item.click()

    def get_quantity(self):
        return self.get_text(self.QUANTITY_VALUE)

    def is_quantity_decrease_disabled(self):
        return self._wait(self.QUANTITY_DECREASE).get_attribute("aria-disabled") == "true"

    def increase_quantity(self):
        self.click(self.QUANTITY_INCREASE)

    def decrease_quantity(self):
        self.click(self.QUANTITY_DECREASE)

    def get_total_price(self):
        return self.get_text(self.TOTAL_PRICE)

    def click_add_to_cart_button(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def click_buy_now_button(self):
        self.click(self.BUY_NOW_BUTTON)

    def get_add_to_cart_toast_text(self):
        return self.get_text(self.ADD_TO_CART_TOAST)

    def get_cart_icon_badge_count(self):
        return self.get_text(self.CART_ICON_BADGE)
