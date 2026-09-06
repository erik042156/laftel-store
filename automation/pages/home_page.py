from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    LOGIN_PROMPT_HEADING = (By.XPATH, '//h2[normalize-space(.)="로그인 후 이용해 주세요."]')
    # 검색/작품 페이지에는 무한 스크롤 로딩용 빈 div[role="status"]가 먼저 렌더링되어 있어
    # 토스트 자체를 특정하는 [data-scope="toast"][data-part="root"]로 구분한다.
    WISH_TOAST = (By.CSS_SELECTOR, 'div[data-scope="toast"][data-part="root"]')
    # 메인페이지 상단의 검색창은 readonly input으로, 클릭하면 텍스트 입력 없이
    # 곧바로 /search 검색페이지로 이동한다(자체 입력 기능이 아닌 진입 버튼 역할).
    SEARCH_ENTRY = (By.CSS_SELECTOR, 'input[placeholder="굿즈 또는 작품명으로 검색해 보세요"]')

    def open(self):
        self.driver.get(BASE_URL)

    def click_search_entry(self):
        self.click(self.SEARCH_ENTRY)

    def open_search_result(self, keyword):
        self.driver.get(f"{BASE_URL}search?keyword={keyword}")

    def open_ip_page(self, ip_id):
        self.driver.get(f"{BASE_URL}ip/{ip_id}")

    def wish_icon_locator(self, index=1):
        return (
            By.XPATH,
            f'(//button[@aria-label="찜하기" or @aria-label="찜 해제"])[{index}]',
        )

    def click_wish_icon(self, index=1):
        self.click(self.wish_icon_locator(index))

    def is_wish_icon_filled(self, index=1):
        return self._wait(self.wish_icon_locator(index)).get_attribute("aria-pressed") == "true"

    def wait_for_wish_icon_state(self, index, filled):
        self.wait_for_attribute_value(self.wish_icon_locator(index), "aria-pressed", "true" if filled else "false")

    def get_login_prompt_text(self):
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def get_wish_toast_text(self):
        self.wait_for_text(self.WISH_TOAST, "찜")
        return self.get_text(self.WISH_TOAST)
