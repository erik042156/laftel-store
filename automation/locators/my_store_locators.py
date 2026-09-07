from selenium.webdriver.common.by import By


class MyStoreLocators:
    WISH_MENU_BADGE_COUNT = (By.XPATH, '//span[starts-with(normalize-space(.), "찜")]/span')
    WISH_MENU_LINK = (By.XPATH, '//button[.//span[normalize-space(.)="찜"]]')
    LOGIN_PROMPT_HEADING = (By.XPATH, '//h2[normalize-space(.)="로그인 후 이용해 주세요."]')
    LOGIN_PROMPT_CANCEL_BUTTON = (By.XPATH, '//button[normalize-space(.)="취소"]')
    LOGIN_PROMPT_LOGIN_BUTTON = (By.XPATH, '//button[normalize-space(.)="로그인"]')

    def _section_locator_prefix(self, heading_text):
        # 각 섹션은 h2 제목과 상품 카드들을 하나의 <section>으로 함께 감싸고 있음을
        # 실측으로 확인했다(wishlist_page.py의 WORK_SECTION과 동일 패턴). following::
        # 축을 문서 전체에 쓰면 대상 섹션이 비어 있을 때 다른 섹션의 카드가 잘못
        # 매칭될 수 있어, 해당 섹션 컨테이너로 범위를 좁힌다.
        return f'//section[.//h2[normalize-space(.)="{heading_text}"]]'

    def _first_product_link_after_heading(self, heading_text):
        return (
            By.XPATH,
            f'{self._section_locator_prefix(heading_text)}//a[starts-with(@href, "/products/")][1]',
        )

    def _section_card_locator(self, heading_text, index=1):
        return (
            By.XPATH,
            f'{self._section_locator_prefix(heading_text)}//a[starts-with(@href, "/products/")][{index}]',
        )

    def _section_card_wish_icon_locator(self, heading_text, index=1):
        return (
            By.XPATH,
            f'{self._section_locator_prefix(heading_text)}//a[starts-with(@href, "/products/")]'
            f'[{index}]//button[@aria-label="찜하기" or @aria-label="찜 해제"]',
        )

    def section_product_links_locator(self, heading_text):
        return (By.XPATH, f'{self._section_locator_prefix(heading_text)}//a[starts-with(@href, "/products/")]')
