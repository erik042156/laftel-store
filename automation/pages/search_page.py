from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from locators.search_locators import SearchLocators
from pages.base_page import BasePage


class SearchPage(SearchLocators, BasePage):
    def open(self):
        self.driver.get(f"{BASE_URL}search")

    def is_initial_screen_displayed(self):
        return (
            self.is_on_search_screen()
            and len(self.driver.find_elements(*self.POPULAR_WORKS_HEADING)) > 0
            and len(self.driver.find_elements(*self.RANKING_HEADING)) > 0
        )

    def is_on_search_screen(self):
        # 검색창에 값이 입력되면(공백만 입력해도) "인기 작품"/랭킹 섹션은 사라지므로,
        # 검색페이지 자체에 머물러 있는지(뒤로가기/검색창/취소 버튼 존재)만 판정한다.
        return (
            len(self.driver.find_elements(*self.BACK_BUTTON)) > 0
            and len(self.driver.find_elements(*self.SEARCH_INPUT)) > 0
            and len(self.driver.find_elements(*self.CANCEL_BUTTON)) > 0
        )

    def click_back(self):
        self.click(self.BACK_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def type_keyword(self, text):
        self.type_text(self.SEARCH_INPUT, text)

    def append_to_keyword(self, text):
        self._wait(self.SEARCH_INPUT).send_keys(text)

    def backspace_keyword(self, count=1):
        element = self._wait(self.SEARCH_INPUT)
        for _ in range(count):
            element.send_keys(Keys.BACK_SPACE)

    def submit_search(self):
        self._wait(self.SEARCH_INPUT).send_keys(Keys.ENTER)

    def clear_keyword(self):
        # 이미 값이 채워진 React 컨트롤드 입력은 element.clear()가 내부 상태를 갱신하지
        # 못하므로(AUTOMATION_GUIDE 7.10절), 실제 키 입력과 동일한 Backspace로 지운다.
        element = self._wait(self.SEARCH_INPUT)
        current_value = element.get_attribute("value")
        element.send_keys(Keys.END)
        for _ in range(len(current_value)):
            element.send_keys(Keys.BACK_SPACE)

    def get_autocomplete_work_item_texts(self):
        return [e.text for e in self.driver.find_elements(*self.AUTOCOMPLETE_WORK_ITEM)]

    def get_autocomplete_related_keyword_texts(self):
        return [e.text for e in self.driver.find_elements(*self.AUTOCOMPLETE_RELATED_KEYWORD_ITEM)]

    def click_autocomplete_work_item(self, index=1):
        self.click(self.autocomplete_work_item_locator(index))

    def click_autocomplete_related_keyword_item(self, index=1):
        self.click(self.autocomplete_related_keyword_item_locator(index))

    def wait_for_autocomplete_related_keywords_present(self):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(*self.AUTOCOMPLETE_RELATED_KEYWORD_ITEM)) > 0
        )

    def wait_for_autocomplete_related_keywords_change(self, previous_texts):
        # 입력 직후 목록이 잠시 비었다가(디바운스/네트워크 지연) 새 결과로 채워지므로,
        # 그 과도기의 빈 목록을 "변경됨"으로 오판하지 않도록 비어있지 않은 상태까지 기다린다.
        def _changed_and_not_empty(driver):
            current_texts = [e.text for e in driver.find_elements(*self.AUTOCOMPLETE_RELATED_KEYWORD_ITEM)]
            return current_texts if current_texts and current_texts != previous_texts else False

        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(_changed_and_not_empty)

    def is_recent_search_heading_present(self):
        return len(self.driver.find_elements(*self.RECENT_SEARCH_HEADING)) > 0

    def is_recent_search_clear_all_present(self):
        return len(self.driver.find_elements(*self.RECENT_SEARCH_CLEAR_ALL_BUTTON)) > 0

    def get_recent_search_keywords(self):
        return [e.text for e in self.driver.find_elements(*self.RECENT_SEARCH_ITEM_KEYWORD_BUTTON)]

    def click_recent_search_clear_all(self):
        self.click(self.RECENT_SEARCH_CLEAR_ALL_BUTTON)

    def click_recent_search_item(self, keyword):
        self.click(self.recent_search_item_locator(keyword))

    def click_recent_search_delete(self, keyword):
        self.click(self.recent_search_delete_locator(keyword))

    def wait_for_recent_search_keyword_present(self, keyword):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: keyword in self.get_recent_search_keywords())

    def wait_for_recent_search_keyword_absent(self, keyword):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: keyword not in self.get_recent_search_keywords()
        )

    def wait_for_recent_search_cleared(self):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(*self.RECENT_SEARCH_HEADING)) == 0
        )
