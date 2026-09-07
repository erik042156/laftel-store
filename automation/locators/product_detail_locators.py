from selenium.webdriver.common.by import By


class ProductDetailLocators:
    BACK_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="뒤로가기"]')
    SEARCH_ICON = (By.CSS_SELECTOR, 'button[aria-label="검색"]')
    CART_ICON = (By.CSS_SELECTOR, 'button[aria-label="장바구니"]')
    LOGIN_PROMPT_HEADING = (By.XPATH, '//h2[normalize-space(.)="로그인 후 이용해 주세요."]')
    MAIN_LIST_PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='/products/']:not([target='_blank'])")
    IMAGE_CAROUSEL_VIEWPORT = (By.XPATH, '(//div[@aria-label="상품 이미지 상세보기"])[1]/parent::div/parent::div')
    CAROUSEL_PAGINATION = (By.XPATH, '//div[not(*) and contains(., "/")]')
    IP_TITLE_LINK = (By.CSS_SELECTOR, 'a[href^="/ip/"]')
    PRODUCT_NAME = (By.TAG_NAME, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, 'div[aria-label="상품 가격 정보"]')
    RELATED_MORE_LINK = (By.CSS_SELECTOR, 'a[href$="/related"]')
    DETAIL_MORE_TOGGLE = (By.XPATH, '//button[normalize-space(.)="상세정보 더보기" or normalize-space(.)="상세정보 접기"]')
    PRODUCT_INFO_ACCORDION = (By.XPATH, '//button[normalize-space(.)="상품정보 제공고시"]')
    EXCHANGE_RETURN_INFO_ACCORDION = (By.XPATH, '//button[normalize-space(.)="교환/반품 안내"]')
    SELLER_INFO_ACCORDION = (By.XPATH, '//button[normalize-space(.)="판매자 정보"]')
    NOTICE_ACCORDION = (By.XPATH, '//button[normalize-space(.)="유의사항"]')
    BUY_BUTTON = (
        By.XPATH,
        '//button[normalize-space(.)="구매하기" or normalize-space(.)="품절" or normalize-space(.)="판매종료"]',
    )
    BOTTOM_WISH_ICON = (
        By.XPATH,
        '//button[normalize-space(.)="구매하기" or normalize-space(.)="품절" or normalize-space(.)="판매종료"]'
        '/parent::div/parent::div//button[@aria-label="찜하기" or @aria-label="찜 해제"]',
    )
    OPTION_DROPDOWN_TRIGGER = (By.CSS_SELECTOR, 'button[aria-haspopup="listbox"]')
    OPTION_ITEMS = (By.CSS_SELECTOR, '[role="listbox"] [role="option"]')
    QUANTITY_DECREASE = (By.CSS_SELECTOR, 'button[aria-label="수량 줄이기"]')
    QUANTITY_INCREASE = (By.CSS_SELECTOR, 'button[aria-label="수량 늘리기"]')
    QUANTITY_VALUE = (By.XPATH, '//button[@aria-label="수량 줄이기"]/following-sibling::span[1]')
    TOTAL_PRICE = (By.XPATH, '//span[normalize-space(.)="총 금액"]/parent::span/following-sibling::span[1]')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="장바구니에 담기"]')
    BUY_NOW_BUTTON = (By.XPATH, '//button[normalize-space(.)="바로구매"]')
    ADD_TO_CART_TOAST = (By.CSS_SELECTOR, 'div[role="status"]')
    CART_ICON_BADGE = (By.XPATH, '//button[@aria-label="장바구니"]//span')

    def related_card_locator(self, index=1):
        return (
            By.XPATH,
            '(//a[starts-with(@href, "/products/") and not(contains(@href, "/related"))])'
            f"[{index}]",
        )

    def related_card_wish_icon_locator(self, index=1):
        return (
            By.XPATH,
            '(//a[starts-with(@href, "/products/") and not(contains(@href, "/related"))])'
            f'[{index}]//button[@aria-label="찜하기" or @aria-label="찜 해제"]',
        )
