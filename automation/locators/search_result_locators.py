from selenium.webdriver.common.by import By


class SearchResultLocators:
    # "총 N개"는 React가 "총 "/"N"/"개"를 별도 텍스트 노드로 렌더링하므로 text()가 아닌
    # 문자열 값(.) 기준으로 매칭해야 한다(실측 확인, ip_page.py와 동일 이슈).
    TOTAL_COUNT_TEXT = (By.XPATH, '//span[contains(., "총") and contains(., "개")]')
    SORT_DROPDOWN_HEADING = (By.XPATH, '//span[normalize-space(.)="인기순" or normalize-space(.)="최신순"]')
    PRODUCT_GRID_ITEM = (By.CSS_SELECTOR, 'a[href^="/products/"]')
    TOP_WORK_CARD_LINK = (By.CSS_SELECTOR, 'a[href^="/ip/"]')
    SORT_TRIGGER = (By.CSS_SELECTOR, 'button[aria-label="정렬 옵션 선택"]')
    # 정렬 드롭다운은 Radix/Ark-UI 다이얼로그로 열리며, 닫힌 상태의 이전 인스턴스가 DOM에
    # 함께 남아있어(Phase1~4에서 반복 확인된 패턴) data-state="open"으로 스코핑해야 한다.
    SORT_DIALOG_OPEN = '//*[@data-scope="dialog" and @data-part="content" and @data-state="open"]'
    EMPTY_STATE_MESSAGE = (By.XPATH, '//p[normalize-space(.)="앗! 원하시는 검색 결과가 없어요."]')

    def product_card_locator(self, product_id):
        return (By.CSS_SELECTOR, f'a[href="/products/{product_id}"]')

    def sort_dialog_open_locator(self):
        return (By.XPATH, self.SORT_DIALOG_OPEN)

    def sort_option_texts_locator(self):
        return (By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[@role="option"]')

    def sort_cancel_button_locator(self):
        return (By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[normalize-space(.)="취소"]')

    def sort_option_locator(self, label):
        return (By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[@role="option" and normalize-space(.)="{label}"]')
