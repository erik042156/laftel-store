from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage


class CartPage(BasePage):
    FIRST_ITEM_PRODUCT_LINK = (By.CSS_SELECTOR, 'a[href^="/products/"]')
    EMPTY_MESSAGE = (By.XPATH, '//p[normalize-space(.)="장바구니에 담긴 상품이 아직 없어요."]')
    INDIVIDUAL_DELETE_BUTTONS = (By.XPATH, '//button[normalize-space(@aria-label)="삭제"]')
    BULK_DELETE_BUTTON = (By.XPATH, '//button[normalize-space(.)="삭제" and not(@aria-label)]')
    DELETE_CONFIRM_DIALOG_HEADING = (By.XPATH, '//h2[normalize-space(.)="선택한 상품을 삭제하시겠어요?"]')
    DELETE_CONFIRM_BUTTON = (By.XPATH, '//div[@role="dialog"]//button[normalize-space(.)="삭제"]')
    DELETE_CANCEL_BUTTON = (By.XPATH, '//div[@role="dialog"]//button[normalize-space(.)="취소"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    PAYMENT_TOTAL_PRICE = (By.XPATH, '//p[normalize-space(.)="결제금액"]/following-sibling::span[1]')
    PRODUCT_TOTAL_PRICE = (By.XPATH, '//span[normalize-space(.)="총 상품 금액"]/following-sibling::span[1]')
    SHIPPING_FEE = (By.XPATH, '//span[normalize-space(.)="배송비"]/following-sibling::span[1]')
    PRODUCT_DISCOUNT = (By.XPATH, '//span[normalize-space(.)="상품 할인"]/following-sibling::span[1]')
    BOTTOM_BUY_BUTTON_TEXT = (By.XPATH, '//button[./p[contains(., "구매하기")]]/p')
    BOTTOM_BUY_BUTTON_COUNT = (By.XPATH, '//button[./p[contains(., "구매하기")]]/span')
    SHIPPING_NOTICE = (By.XPATH, '//p[contains(., "배송비")]/parent::div')
    BOTTOM_BUY_BUTTON = (By.XPATH, '//button[./p[contains(., "구매하기")]]')
    GUIDE_DIALOG_HEADING = (By.XPATH, '//div[@role="dialog"]//h2[contains(., "구매할 상품을 선택")]')
    GUIDE_DIALOG_CONFIRM_BUTTON = (By.XPATH, '//div[@role="dialog"]//button[normalize-space(.)="확인"]')
    SELECT_ALL_LABEL = (By.XPATH, '//span[starts-with(normalize-space(.), "전체선택")]')
    SELLER_GROUP_CHECKBOX = (By.XPATH, '(//input[@type="checkbox"])[2]')

    def open(self):
        self.driver.get(f"{BASE_URL}cart")

    def click_first_item(self):
        self.click(self.FIRST_ITEM_PRODUCT_LINK)

    def get_empty_message_text(self):
        return self.get_text(self.EMPTY_MESSAGE)

    def is_empty(self):
        return len(self.driver.find_elements(*self.EMPTY_MESSAGE)) > 0

    def get_item_count(self):
        return len(self.driver.find_elements(*self.FIRST_ITEM_PRODUCT_LINK))

    def wait_for_items_loaded(self):
        # 장바구니 진입 직후에는 실제 상품 링크 대신 스켈레톤 placeholder가 먼저
        # 렌더링되므로, 개수를 세기 전 실제 상품 링크가 나타날 때까지 기다린다.
        self._wait(self.FIRST_ITEM_PRODUCT_LINK)

    def wait_for_cart_loaded(self):
        # 장바구니 진입 직후 스켈레톤 상태에서는 상품 링크도 빈 상태 안내문도 아직
        # 없어, is_empty()를 곧바로 호출하면 "비어있지 않음"으로 오판할 수 있다.
        # 둘 중 하나가 나타날 때까지(실제 로딩 완료) 기다린 뒤 판단해야 한다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(*self.EMPTY_MESSAGE)) > 0
            or len(driver.find_elements(*self.FIRST_ITEM_PRODUCT_LINK)) > 0
        )

    def wait_for_item_count(self, expected_count):
        # 삭제 확인 후 목록이 실제로 갱신될 때까지는 짧은 지연이 있어,
        # 개수를 재확인하기 전에 기대 개수가 될 때까지 기다린다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(*self.FIRST_ITEM_PRODUCT_LINK)) == expected_count
        )

    def individual_delete_locator(self, index=1):
        return (By.XPATH, f'(//button[normalize-space(@aria-label)="삭제"])[{index}]')

    def click_individual_delete(self, index=1):
        self.click(self.individual_delete_locator(index))

    def click_bulk_delete(self):
        self.click(self.BULK_DELETE_BUTTON)

    def get_delete_confirm_heading_text(self):
        # 팝업 요소가 DOM에 나타난 직후에는 텍스트가 아직 채워지지 않은 경우가 있어,
        # 내용이 실제로 채워질 때까지 기다린 뒤 읽는다.
        self.wait_for_text(self.DELETE_CONFIRM_DIALOG_HEADING, "삭제")
        return self.get_text(self.DELETE_CONFIRM_DIALOG_HEADING)

    def confirm_delete(self):
        self.click(self.DELETE_CONFIRM_BUTTON)

    def cancel_delete(self):
        self.click(self.DELETE_CANCEL_BUTTON)

    def click_select_all(self):
        self.click_via_js(self.SELECT_ALL_CHECKBOX)

    def item_checkbox_locator(self, index=1):
        # 체크박스 순서: [1]=전체선택, [2]=판매자 그룹, [3]부터 개별 상품
        # (판매자가 "Laftel Store" 1곳뿐인 현재 테스트 데이터 기준).
        return (By.XPATH, f'(//input[@type="checkbox"])[{index + 2}]')

    def click_item_checkbox(self, index=1):
        self.click_via_js(self.item_checkbox_locator(index))

    def click_seller_group_checkbox(self):
        self.click_via_js(self.SELLER_GROUP_CHECKBOX)

    def is_select_all_checked(self):
        checkbox = self._wait(self.SELECT_ALL_CHECKBOX)
        return self.driver.execute_script("return arguments[0].checked;", checkbox)

    def is_seller_group_checked(self):
        checkbox = self._wait(self.SELLER_GROUP_CHECKBOX)
        return self.driver.execute_script("return arguments[0].checked;", checkbox)

    def is_item_checked(self, index=1):
        checkbox = self._wait(self.item_checkbox_locator(index))
        return self.driver.execute_script("return arguments[0].checked;", checkbox)

    def get_select_all_label_text(self):
        return self.get_text(self.SELECT_ALL_LABEL)

    def quantity_decrease_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 줄이기"])[{index}]')

    def quantity_increase_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 늘리기"])[{index}]')

    def quantity_value_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 줄이기"])[{index}]/following-sibling::span[1]')

    def item_amount_locator(self, index=1):
        return (By.XPATH, f'(//p[normalize-space(.)="상품금액"])[{index}]/following-sibling::p[1]')

    def increase_quantity(self, index=1):
        self.click(self.quantity_increase_locator(index))

    def decrease_quantity(self, index=1):
        self.click(self.quantity_decrease_locator(index))

    def get_quantity(self, index=1):
        return self.get_text(self.quantity_value_locator(index))

    def get_item_amount_text(self, index=1):
        return self.get_text(self.item_amount_locator(index))

    def is_quantity_decrease_disabled(self, index=1):
        return self._wait(self.quantity_decrease_locator(index)).get_attribute("aria-disabled") == "true"

    def try_click_disabled_quantity_decrease(self, index=1):
        # 비활성화된 버튼은 EC.element_to_be_clickable을 절대 만족하지 않으므로
        # 존재 여부만 확인(presence)한 뒤 그대로 클릭을 시도한다.
        self._wait(self.quantity_decrease_locator(index)).click()

    def click_bottom_buy_button(self):
        self.click(self.BOTTOM_BUY_BUTTON)

    def get_guide_dialog_text(self):
        # 팝업 요소가 DOM에 나타난 직후에는 텍스트가 아직 채워지지 않은 경우가 있어,
        # 내용이 실제로 채워질 때까지 기다린 뒤 읽는다.
        self.wait_for_text(self.GUIDE_DIALOG_HEADING, "선택")
        return self.get_text(self.GUIDE_DIALOG_HEADING)

    def click_guide_dialog_confirm(self):
        self.click(self.GUIDE_DIALOG_CONFIRM_BUTTON)

    def get_payment_total_price(self):
        return self.get_text(self.PAYMENT_TOTAL_PRICE)

    def get_product_total_price(self):
        return self.get_text(self.PRODUCT_TOTAL_PRICE)

    def get_shipping_fee_text(self):
        return self.get_text(self.SHIPPING_FEE)

    def get_product_discount_text(self):
        return self.get_text(self.PRODUCT_DISCOUNT)

    def get_bottom_buy_button_text(self):
        return self.get_text(self.BOTTOM_BUY_BUTTON_TEXT)

    def get_bottom_buy_button_count(self):
        return self.get_text(self.BOTTOM_BUY_BUTTON_COUNT)

    def get_shipping_notice_text(self):
        return self.get_text(self.SHIPPING_NOTICE)

    def ensure_all_selected(self):
        # 장바구니에 담긴 상품은 기본적으로 전체선택된 상태로 표시되므로,
        # 무조건 클릭하면 오히려 전체 해제가 되어버린다. 체크 여부를 먼저 확인한다.
        checkbox = self._wait(self.SELECT_ALL_CHECKBOX)
        if not self.driver.execute_script("return arguments[0].checked;", checkbox):
            self.click_select_all()

    def clear_cart(self):
        self.open()
        self.wait_for_cart_loaded()
        if self.is_empty():
            return
        self.ensure_all_selected()
        self.click_bulk_delete()
        self.confirm_delete()
        self._wait(self.EMPTY_MESSAGE)
