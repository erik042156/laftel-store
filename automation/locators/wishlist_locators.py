from selenium.webdriver.common.by import By


class WishlistLocators:
    # 비활성 탭의 패널도 DOM에 함께 남아있어(7.13/7.14절) href만으로 매칭하면 숨겨진
    # 탭의 카드가 함께 잡혀 항상-존재로 오판될 수 있으므로, 활성 탭패널로 범위를 좁힌다.
    FIRST_ITEM_PRODUCT_LINK = (
        By.XPATH,
        '//*[@role="tabpanel" and @aria-hidden="false"]//a[starts-with(@href, "/products/")]',
    )
    PRODUCT_TAB = (By.XPATH, '//button[@role="tab" and normalize-space(.)="상품"]')
    WORK_TAB = (By.XPATH, '//button[@role="tab" and normalize-space(.)="작품"]')
    # 비활성 탭의 패널도 DOM에는 남아있어(display 처리) 존재 여부만으로는 판단할 수
    # 없으므로, 실제 화면에 보이는지(is_displayed)로 판정한다.
    EDIT_LINK = (By.XPATH, '//button[normalize-space(.)="편집하기"]')
    CANCEL_EDIT_LINK = (By.XPATH, '//button[normalize-space(.)="편집취소"]')
    DELETE_SELECTED_LINK = (By.XPATH, '//button[normalize-space(.)="선택삭제"]')
    # 비활성 탭 패널에도 이전 렌더링 잔여물이 남아있을 수 있어(7.13/7.14절과 동일 유형)
    # 활성 tabpanel로 범위를 좁힌다.
    SELECT_ALL_CHECKBOX = (
        By.XPATH,
        '//*[@role="tabpanel" and @aria-hidden="false"]//button[@role="checkbox" and @aria-label="전체 선택"]',
    )
    SELECTED_COUNT_TEXT = (By.XPATH, '//*[@role="tabpanel" and @aria-hidden="false"]//span[@aria-live="polite"]')
    # 편집 모드에서는 카드 링크(<a>) 위에 선택 토글용 오버레이(role="button",
    # aria-pressed)가 덮여 있어, 실제 클릭 대상은 이 오버레이다.
    ITEM_CARD = (
        By.XPATH,
        '//*[@role="tabpanel" and @aria-hidden="false"]//div[@role="button" and @aria-pressed]',
    )
    # "작품" 탭은 IP별로 <section>이 분리되어 있고, 각 섹션은 /ip/{id} 링크(제목)와
    # 그 형제 위치의 찜 버튼(작품 단위 전체 해제), 그리고 캐러셀(상품 카드들)로 구성된다.
    WORK_SECTION = (By.XPATH, '//section[.//a[starts-with(@href, "/ip/")]]')
    # 동일 dialog가 이전 렌더링 잔여물로 hidden 상태로도 DOM에 남아있어(체크아웃
    # 페이지의 약관 안내 팝업과 동일 유형), data-state="open"으로 활성 다이얼로그만 특정한다.
    DELETE_CONFIRM_DIALOG = (
        By.XPATH,
        '//div[@data-scope="dialog" and @data-part="content" and @data-state="open"]',
    )
    DELETE_CONFIRM_BUTTON = (
        By.XPATH,
        '//div[@data-scope="dialog" and @data-part="content" and @data-state="open"]'
        '//button[normalize-space(.)="삭제"]',
    )
    DELETE_CANCEL_BUTTON = (
        By.XPATH,
        '//div[@data-scope="dialog" and @data-part="content" and @data-state="open"]'
        '//button[normalize-space(.)="취소"]',
    )
    LOGIN_PROMPT_HEADING = (By.XPATH, '//h2[normalize-space(.)="로그인 후 이용해 주세요."]')
    LOGIN_PROMPT_CANCEL_BUTTON = (By.XPATH, '//button[normalize-space(.)="취소"]')
    LOGIN_PROMPT_LOGIN_BUTTON = (By.XPATH, '//button[normalize-space(.)="로그인"]')

    def _work_section_title_link_locator(self, index=1):
        return (By.XPATH, f'({self.WORK_SECTION[1]})[{index}]//a[starts-with(@href, "/ip/")]')

    def _work_section_heart_locator(self, index=1):
        return (
            By.XPATH,
            f'({self.WORK_SECTION[1]})[{index}]//a[starts-with(@href, "/ip/")]'
            '/following-sibling::button[@aria-label="찜하기" or @aria-label="찜 해제"][1]',
        )

    def _product_wish_icon_locator(self, product_id):
        # 비활성 탭의 패널도 DOM에 함께 남아있어(7.4/7.13절 유사 문제), href만으로
        # 매칭하면 숨겨진 패널의 동일 상품 카드가 먼저 잡혀 클릭이 항상 타임아웃될 수
        # 있다. 현재 활성 상태인 tabpanel(@aria-hidden="false") 안으로 범위를 좁힌다.
        return (
            By.XPATH,
            f'//*[@role="tabpanel" and @aria-hidden="false"]//a[@href="/products/{product_id}"]'
            '//button[@aria-label="찜하기" or @aria-label="찜 해제"]',
        )

    def product_link_locator(self, product_id):
        return (By.XPATH, f'//a[@href="/products/{product_id}"]')

    def item_card_locator(self, index=1):
        return (By.XPATH, f'({self.ITEM_CARD[1]})[{index}]')
