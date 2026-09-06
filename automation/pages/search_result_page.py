import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage


class SearchResultPage(BasePage):
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

    def is_screen_displayed(self):
        # 진입 직후에는 상품 그리드/총개수/정렬이 비동기로 채워지므로, 그리드 항목이
        # 나타날 때까지 명시적으로 대기한 뒤 나머지 요소 존재 여부를 판정한다.
        self._wait(self.PRODUCT_GRID_ITEM)
        return (
            len(self.driver.find_elements(*self.TOTAL_COUNT_TEXT)) > 0
            and len(self.driver.find_elements(*self.SORT_DROPDOWN_HEADING)) > 0
            and len(self.driver.find_elements(*self.PRODUCT_GRID_ITEM)) > 0
        )

    def get_total_count(self):
        text = self.get_text(self.TOTAL_COUNT_TEXT)
        return int(re.sub(r"\D", "", text))

    def get_grid_item_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_GRID_ITEM))

    def get_grid_item_texts(self):
        return [e.text for e in self.driver.find_elements(*self.PRODUCT_GRID_ITEM)]

    def click_product_card(self, product_id):
        self.click((By.CSS_SELECTOR, f'a[href="/products/{product_id}"]'))

    def is_empty_state_displayed(self):
        self._wait(self.EMPTY_STATE_MESSAGE)
        return len(self.driver.find_elements(*self.EMPTY_STATE_MESSAGE)) > 0

    def load_all_grid_items(self, total_count, max_scrolls=20):
        # 2열 그리드는 무한 스크롤로 로드되므로, "총 N개"와 비교하려면 스크롤을 반복해
        # 실제 로드된 카드 수가 총 개수에 도달할 때까지 채운다(각 시도는 짧은 타임아웃으로
        # 더 이상 늘어나지 않으면 중단해 무한 루프를 방지한다).
        for _ in range(max_scrolls):
            current_count = self.get_grid_item_count()
            if current_count >= total_count:
                break
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, 3).until(
                    lambda driver: len(driver.find_elements(*self.PRODUCT_GRID_ITEM)) > current_count
                )
            except TimeoutException:
                break
        return self.get_grid_item_count()

    def click_top_work_card(self):
        self.click(self.TOP_WORK_CARD_LINK)

    def click_sort_trigger(self):
        self.click(self.SORT_TRIGGER)

    def get_sort_trigger_text(self):
        return self.get_text(self.SORT_TRIGGER)

    def is_sort_dialog_open(self):
        return len(self.driver.find_elements(By.XPATH, self.SORT_DIALOG_OPEN)) > 0

    def get_sort_option_texts(self):
        options = self.driver.find_elements(By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[@role="option"]')
        return [o.text for o in options]

    def is_sort_cancel_button_present(self):
        return len(self.driver.find_elements(By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[normalize-space(.)="취소"]')) > 0

    def is_sort_option_selected(self, label):
        option = self._wait(
            (By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[@role="option" and normalize-space(.)="{label}"]')
        )
        return option.get_attribute("aria-selected") == "true"

    def click_sort_option(self, label):
        self.click((By.XPATH, f'{self.SORT_DIALOG_OPEN}//button[@role="option" and normalize-space(.)="{label}"]'))

    def wait_for_sort_dialog_closed(self):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(By.XPATH, self.SORT_DIALOG_OPEN)) == 0
        )
