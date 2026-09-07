from selenium.webdriver.common.by import By


class CartLocators:
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

    def individual_delete_locator(self, index=1):
        return (By.XPATH, f'(//button[normalize-space(@aria-label)="삭제"])[{index}]')

    def item_checkbox_locator(self, index=1):
        # 체크박스 순서: [1]=전체선택, [2]=판매자 그룹, [3]부터 개별 상품
        # (판매자가 "Laftel Store" 1곳뿐인 현재 테스트 데이터 기준).
        return (By.XPATH, f'(//input[@type="checkbox"])[{index + 2}]')

    def quantity_decrease_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 줄이기"])[{index}]')

    def quantity_increase_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 늘리기"])[{index}]')

    def quantity_value_locator(self, index=1):
        return (By.XPATH, f'(//button[@aria-label="수량 줄이기"])[{index}]/following-sibling::span[1]')

    def item_amount_locator(self, index=1):
        return (By.XPATH, f'(//p[normalize-space(.)="상품금액"])[{index}]/following-sibling::p[1]')
