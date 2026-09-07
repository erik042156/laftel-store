from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from locators.checkout_locators import CheckoutLocators
from pages.base_page import BasePage


def _switch_to_frame(driver, locator):
    def _predicate(d):
        try:
            d.switch_to.frame(d.find_element(*locator))
            return True
        except (NoSuchElementException, StaleElementReferenceException, NoSuchFrameException):
            return False

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(_predicate)


class CheckoutPage(CheckoutLocators, BasePage):
    def get_recipient_name_placeholder(self):
        return self._wait(self.RECIPIENT_NAME_INPUT).get_attribute("placeholder")

    def get_phone_placeholder(self):
        return self._wait(self.PHONE_INPUT).get_attribute("placeholder")

    def get_zip_code_placeholder(self):
        return self._wait(self.ZIP_CODE_INPUT).get_attribute("placeholder")

    def get_address_placeholder(self):
        return self._wait(self.ADDRESS_INPUT).get_attribute("placeholder")

    def get_shipping_request_value_text(self):
        return self.get_text(self.SHIPPING_REQUEST_DROPDOWN)

    def click_buy_button(self):
        self.click(self.BUY_BUTTON)

    def get_name_error_text(self):
        return self.get_text(self.NAME_ERROR)

    def get_phone_error_text(self):
        return self.get_text(self.PHONE_ERROR)

    def get_address_error_text(self):
        return self.get_text(self.ADDRESS_ERROR)

    def get_phone_value(self):
        return self._wait(self.PHONE_INPUT).get_attribute("value")

    def get_recipient_name_value(self):
        return self._wait(self.RECIPIENT_NAME_INPUT).get_attribute("value")

    def get_zip_code_value(self):
        return self._wait(self.ZIP_CODE_INPUT).get_attribute("value")

    def get_address_value(self):
        return self._wait(self.ADDRESS_INPUT).get_attribute("value")

    def wait_for_shipping_info_prefilled(self):
        # 계정에 저장된 배송지가 있으면 비동기로 채워진다(REQ-ORDER-019). 값이 실제로
        # 채워질 때까지 기다린 뒤 조회해야 한다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: driver.find_element(*self.RECIPIENT_NAME_INPUT).get_attribute("value") != ""
        )

    def type_phone(self, text):
        self.type_text(self.PHONE_INPUT, text)

    def click_shipping_request_dropdown(self):
        self.click(self.SHIPPING_REQUEST_DROPDOWN)

    def click_shipping_request_direct_input(self):
        self.click(self.SHIPPING_REQUEST_DIRECT_INPUT_OPTION)

    def type_shipping_request_text(self, text):
        self._wait(self.SHIPPING_REQUEST_TEXTAREA).send_keys(text)

    def get_shipping_request_text_value(self):
        return self._wait(self.SHIPPING_REQUEST_TEXTAREA).get_attribute("value")

    def get_shipping_request_char_count_text(self):
        return self.get_text(self.SHIPPING_REQUEST_CHAR_COUNT)

    def is_shipping_request_char_count_warning(self):
        # 글자 수 제한 초과를 시도하면 카운터 <strong>에 경고색 유틸리티 클래스("gDYihe")가
        # 추가된다(TC-ORDER-005의 필드 에러 문구와 동일한 클래스를 공유하는 디자인시스템
        # 공용 경고색 클래스로 실측 확인).
        classes = self._wait(self.SHIPPING_REQUEST_CHAR_COUNT).get_attribute("class")
        return "gDYihe" in classes.split()

    def get_payment_total_price(self):
        return self.get_text(self.PAYMENT_TOTAL_PRICE)

    def get_product_total_price(self):
        return self.get_text(self.PRODUCT_TOTAL_PRICE)

    def get_shipping_fee_text(self):
        return self.get_text(self.SHIPPING_FEE)

    def get_product_discount_text(self):
        return self.get_text(self.PRODUCT_DISCOUNT)

    def get_buy_button_text(self):
        return self.get_text(self.BUY_BUTTON)

    def get_buy_button_count(self):
        return self.get_text(self.BUY_BUTTON_COUNT)

    def type_recipient_name(self, text):
        self.type_text(self.RECIPIENT_NAME_INPUT, text)

    def _clear_via_keyboard(self, locator):
        # 최근 배송지가 저장된 계정은 받는 사람/휴대폰번호가 React 컨트롤드 입력에
        # 자동으로 채워져 있다(REQ-ORDER-019). element.clear()는 실제 키 입력 이벤트를
        # 발생시키지 않아 React 내부 상태가 갱신되지 않고, 이후 리렌더링 시 DOM 값이
        # 원래 채워진 값으로 되돌아간다(실측 확인). 실제 키 입력처럼 문자 수만큼
        # Backspace를 전송해야 React 상태까지 확실히 비워진다.
        element = self._wait(locator)
        current_length = len(element.get_attribute("value") or "")
        element.send_keys(Keys.END)
        for _ in range(current_length):
            element.send_keys(Keys.BACKSPACE)

    def clear_recipient_name(self):
        self._clear_via_keyboard(self.RECIPIENT_NAME_INPUT)

    def clear_phone(self):
        self._clear_via_keyboard(self.PHONE_INPUT)

    def fill_address_via_kakao_postcode_search(self, query):
        # "우편번호 찾기"(카카오 우편번호 서비스, TC-ORDER-006은 외부 모듈 의존 리스크로
        # 자동화 대상에서 Rejected)는 그 자체를 검증 대상으로 삼지 않는다. address1/
        # zipCode 입력란이 readonly라 이 모달을 거치지 않고는 유효한 주소를 확보할 방법이
        # 없어, 다른 TC(017/019)의 선행 조건을 충족시키기 위한 최소한의 수단으로만
        # 사용한다(검색 → 첫 번째 결과 클릭). 사용자 승인 하에 구현.
        self.click(self.FIND_ZIP_CODE_BUTTON)

        # 모달이 열리는 초기에 iframe이 재구성되며 존재하던 요소가 stale해지는
        # 경우가 있어, find+switch 자체를 (Stale/NoSuchElement 모두) 재시도한다.
        _switch_to_frame(self.driver, self.KAKAO_IFRAME)
        _switch_to_frame(self.driver, self.KAKAO_IFRAME)

        self._wait(self.KAKAO_SEARCH_INPUT).send_keys(query)
        self.click(self.KAKAO_SEARCH_BUTTON)
        self._wait(self.KAKAO_RESULT_ITEM).click()

        self.driver.switch_to.default_content()

    def ensure_all_agreements_unchecked(self):
        for checkbox in self.driver.find_elements(*self.AGREEMENT_CHECKBOXES):
            if self.driver.execute_script("return arguments[0].checked;", checkbox):
                self.driver.execute_script("arguments[0].click();", checkbox)

    def check_all_agreements(self):
        for checkbox in self.driver.find_elements(*self.AGREEMENT_CHECKBOXES):
            if not self.driver.execute_script("return arguments[0].checked;", checkbox):
                self.driver.execute_script("arguments[0].click();", checkbox)

    def get_agreement_guide_dialog_text(self):
        self.wait_for_text(self.AGREEMENT_GUIDE_DIALOG_HEADING, "동의")
        return self.get_text(self.AGREEMENT_GUIDE_DIALOG_HEADING)

    def click_agreement_guide_dialog_confirm(self):
        self.click(self.AGREEMENT_GUIDE_DIALOG_CONFIRM_BUTTON)
