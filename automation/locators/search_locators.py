from selenium.webdriver.common.by import By


class SearchLocators:
    BACK_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="뒤로가기"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[placeholder="굿즈 또는 작품명으로 검색해 보세요"]')
    CANCEL_BUTTON = (By.XPATH, '//button[normalize-space(.)="취소"]')
    POPULAR_WORKS_HEADING = (By.XPATH, '//span[normalize-space(.)="인기 작품"]')
    RANKING_HEADING = (By.XPATH, '//span[normalize-space(.)="지금 사람들이 많이 구매하는 굿즈"]')
    # 자동완성의 "작품" 뱃지 항목은 /ip/{id}로 연결되는 <a>이며, 뱃지 없는 연관 검색어
    # 항목은 <ul><li><button>...으로 구성됨을 실측으로 확인했다(둘은 서로 다른 컨테이너).
    AUTOCOMPLETE_WORK_ITEM = (
        By.XPATH,
        '//a[starts-with(@href, "/ip/")][.//span[normalize-space(.)="작품"]]',
    )
    AUTOCOMPLETE_RELATED_KEYWORD_ITEM = (By.XPATH, "//ul/li/button")
    RECENT_SEARCH_HEADING = (By.XPATH, '//span[normalize-space(.)="최근 검색"]')
    RECENT_SEARCH_CLEAR_ALL_BUTTON = (By.XPATH, '//button[normalize-space(.)="모두 삭제"]')
    # 최근 검색어 영역도 자동완성과 동일한 <ul><li> 목록으로 구성되며, 항목 텍스트 버튼(
    # aria-label 없음)과 개별 삭제 버튼(aria-label="{키워드} 삭제")으로 구분됨을 실측했다.
    RECENT_SEARCH_ITEM_KEYWORD_BUTTON = (By.XPATH, "//ul/li/button[not(@aria-label)]")

    def autocomplete_work_item_locator(self, index=1):
        return (By.XPATH, f"({self.AUTOCOMPLETE_WORK_ITEM[1]})[{index}]")

    def autocomplete_related_keyword_item_locator(self, index=1):
        return (By.XPATH, f"({self.AUTOCOMPLETE_RELATED_KEYWORD_ITEM[1]})[{index}]")

    def recent_search_item_locator(self, keyword):
        return (By.XPATH, f'//ul/li/button[not(@aria-label) and normalize-space(.)="{keyword}"]')

    def recent_search_delete_locator(self, keyword):
        return (By.XPATH, f'//button[@aria-label="{keyword} 삭제"]')
