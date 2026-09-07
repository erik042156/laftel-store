from selenium.webdriver.common.by import By


class IpLocators:
    TITLE = (By.TAG_NAME, "h1")
    # "총 N개"는 React가 "총 "/"N"/"개"를 별도 텍스트 노드로 렌더링하므로 text()가 아닌
    # 문자열 값(.) 기준으로 매칭해야 한다(실측 확인).
    TOTAL_COUNT_TEXT = (By.XPATH, '//span[contains(., "총") and contains(., "개")]')
    SORT_DROPDOWN_HEADING = (By.XPATH, '//span[normalize-space(.)="인기순" or normalize-space(.)="최신순"]')
    PRODUCT_GRID_ITEM = (By.CSS_SELECTOR, 'a[href^="/products/"]')

    def banner_image_locator(self, title):
        # 배너 이미지의 alt 속성이 작품명(h1 텍스트)과 동일함을 실측으로 확인했다.
        return (By.XPATH, f'//img[@alt="{title}"]')
