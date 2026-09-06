from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class IpPage(BasePage):
    TITLE = (By.TAG_NAME, "h1")
    # "총 N개"는 React가 "총 "/"N"/"개"를 별도 텍스트 노드로 렌더링하므로 text()가 아닌
    # 문자열 값(.) 기준으로 매칭해야 한다(실측 확인).
    TOTAL_COUNT_TEXT = (By.XPATH, '//span[contains(., "총") and contains(., "개")]')
    SORT_DROPDOWN_HEADING = (By.XPATH, '//span[normalize-space(.)="인기순" or normalize-space(.)="최신순"]')
    PRODUCT_GRID_ITEM = (By.CSS_SELECTOR, 'a[href^="/products/"]')

    def get_title(self):
        return self.get_text(self.TITLE)

    def is_banner_image_displayed(self):
        # 배너 이미지의 alt 속성이 작품명(h1 텍스트)과 동일함을 실측으로 확인했다.
        title = self.get_title()
        return len(self.driver.find_elements(By.XPATH, f'//img[@alt="{title}"]')) > 0

    def is_screen_displayed(self):
        # 진입 직후에는 상품 그리드/총개수/정렬이 비동기로 채워지므로, 그리드 항목이
        # 나타날 때까지 명시적으로 대기한 뒤 나머지 요소 존재 여부를 판정한다.
        self._wait(self.PRODUCT_GRID_ITEM)
        return (
            self.is_banner_image_displayed()
            and len(self.driver.find_elements(*self.TOTAL_COUNT_TEXT)) > 0
            and len(self.driver.find_elements(*self.SORT_DROPDOWN_HEADING)) > 0
            and len(self.driver.find_elements(*self.PRODUCT_GRID_ITEM)) > 0
        )

    def get_current_url(self):
        return self.driver.current_url
