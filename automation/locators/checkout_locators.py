from selenium.webdriver.common.by import By


class CheckoutLocators:
    RECIPIENT_NAME_INPUT = (By.CSS_SELECTOR, 'input[name="name"]')
    PHONE_INPUT = (By.CSS_SELECTOR, 'input[name="cellphone"]')
    ZIP_CODE_INPUT = (By.CSS_SELECTOR, 'input[name="zipCode"]')
    ADDRESS_INPUT = (By.CSS_SELECTOR, 'input[name="address1"]')
    ADDRESS_DETAIL_INPUT = (By.CSS_SELECTOR, 'input[name="address2"]')
    FIND_ZIP_CODE_BUTTON = (By.XPATH, '//button[normalize-space(.)="우편번호 찾기"]')
    SHIPPING_REQUEST_DROPDOWN = (By.CSS_SELECTOR, 'button[aria-haspopup="listbox"]')
    BUY_BUTTON = (By.XPATH, '//button[contains(., "구매하기")]')
    NAME_ERROR = (By.XPATH, '//input[@name="name"]/following-sibling::span[@data-part="error-text"]')
    PHONE_ERROR = (By.XPATH, '//input[@name="cellphone"]/following-sibling::span[@data-part="error-text"]')
    ADDRESS_ERROR = (By.XPATH, '//input[@name="address1"]/following-sibling::span[@data-part="error-text"]')
    SHIPPING_REQUEST_DIRECT_INPUT_OPTION = (By.XPATH, '//*[@role="option" and normalize-space(.)="직접입력"]')
    SHIPPING_REQUEST_TEXTAREA = (By.CSS_SELECTOR, 'textarea[name="customDeliveryRequest"]')
    SHIPPING_REQUEST_CHAR_COUNT = (
        By.XPATH,
        '//textarea[@name="customDeliveryRequest"]/following-sibling::span[1]/strong',
    )
    PAYMENT_TOTAL_PRICE = (By.XPATH, '//h2[normalize-space(.)="결제금액"]/following-sibling::span[1]')
    PRODUCT_TOTAL_PRICE = (By.XPATH, '//span[normalize-space(.)="총 상품 금액"]/following-sibling::span[1]')
    SHIPPING_FEE = (By.XPATH, '//span[normalize-space(.)="배송비"]/following-sibling::span[1]')
    PRODUCT_DISCOUNT = (By.XPATH, '//span[normalize-space(.)="상품 할인"]/following-sibling::span[1]')
    BUY_BUTTON_COUNT = (By.XPATH, '//button[contains(., "구매하기")]/span')
    KAKAO_IFRAME = (By.TAG_NAME, "iframe")
    KAKAO_SEARCH_INPUT = (By.ID, "region_name")
    KAKAO_SEARCH_BUTTON = (By.XPATH, '//button[normalize-space(.)="검색"]')
    KAKAO_RESULT_ITEM = (By.CSS_SELECTOR, "li")
    AGREEMENT_CHECKBOXES = (By.CSS_SELECTOR, 'input[name^="checkbox-"]')
    AGREEMENT_GUIDE_DIALOG_HEADING = (
        By.XPATH,
        '//div[@role="dialog" and @data-state="open"]//h2[contains(., "결제에 동의해 주세요")]',
    )
    AGREEMENT_GUIDE_DIALOG_CONFIRM_BUTTON = (
        By.XPATH,
        '//div[@role="dialog" and @data-state="open"]//button[normalize-space(.)="확인"]',
    )
