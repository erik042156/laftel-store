from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage


class WishlistPage(BasePage):
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

    def open(self):
        self.driver.get(f"{BASE_URL}my/wish")

    def click_first_item(self):
        self.click(self.FIRST_ITEM_PRODUCT_LINK)

    def click_product_tab(self):
        self.click(self.PRODUCT_TAB)

    def click_work_tab(self):
        self.click(self.WORK_TAB)

    def is_edit_link_present(self):
        return any(link.is_displayed() for link in self.driver.find_elements(*self.EDIT_LINK))

    def wait_for_edit_link_hidden(self):
        # 탭 전환 시 패널이 화면에서 사라지기까지 약간의 렌더링 지연이 있어 즉시
        # 판정하면 간헐적으로 실패할 수 있다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_edit_link_present())

    def is_product_present(self, product_id):
        links = self.driver.find_elements(*self.FIRST_ITEM_PRODUCT_LINK)
        return any(f"/products/{product_id}" in link.get_attribute("href") for link in links)

    def wait_for_product_present(self, product_id):
        # SPA 초기 진입 직후에는 상품 목록이 비동기로 채워지므로, 목록이 실제로
        # 렌더링될 때까지 기다린 뒤 판정한다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: self.is_product_present(product_id))

    def wait_for_product_absent(self, product_id):
        # "작품" 탭에서 찜 해제 후 "상품" 탭으로 전환하면 반영까지 약간의 지연이 있어
        # (실측 약 0.5초), 전환 직후 즉시 판정하면 간헐적으로 실패할 수 있다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_product_present(product_id))

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

    def click_work_section_title(self, index=1):
        self.click(self._work_section_title_link_locator(index))

    def click_work_section_heart(self, index=1):
        self.click(self._work_section_heart_locator(index))

    def click_product_wish_icon(self, product_id):
        self.click(self._product_wish_icon_locator(product_id))

    def is_product_wish_icon_filled(self, product_id):
        return self._wait(self._product_wish_icon_locator(product_id)).get_attribute("aria-pressed") == "true"

    def wait_for_product_wish_icon_state(self, product_id, filled):
        self.wait_for_attribute_value(
            self._product_wish_icon_locator(product_id), "aria-pressed", "true" if filled else "false"
        )

    def find_work_section_index(self, ip_id):
        sections = self.driver.find_elements(*self.WORK_SECTION)
        for i, section in enumerate(sections, start=1):
            if f'/ip/{ip_id}"' in section.get_attribute("innerHTML"):
                return i
        return None

    def is_work_section_present(self, ip_id):
        return self.find_work_section_index(ip_id) is not None

    def wait_for_work_section_present(self, ip_id):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: self.is_work_section_present(ip_id))

    def wait_for_work_section_absent(self, ip_id):
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: not self.is_work_section_present(ip_id))

    def get_product_status_badge_text(self, product_id):
        card = self._wait((By.XPATH, f'//a[@href="/products/{product_id}"]'))
        return self.get_status_badge_text(card)

    def click_product(self, product_id):
        self.click((By.XPATH, f'//a[@href="/products/{product_id}"]'))

    def get_login_prompt_text(self):
        self.wait_for_text(self.LOGIN_PROMPT_HEADING, "로그인")
        return self.get_text(self.LOGIN_PROMPT_HEADING)

    def click_login_prompt_cancel(self):
        self.click(self.LOGIN_PROMPT_CANCEL_BUTTON)

    def click_login_prompt_login(self):
        self.click(self.LOGIN_PROMPT_LOGIN_BUTTON)

    def click_edit_link(self):
        self.click(self.EDIT_LINK)
        # "편집하기" 클릭 시 BasePage.click()의 scrollIntoView로 스크롤 위치가 변경되어,
        # 편집 모드 헤더("전체 선택" 등)가 뷰포트 밖/다른 요소에 가려진 상태로 남아
        # element_to_be_clickable이 영구 타임아웃될 수 있다. 최상단으로 복귀시켜 해결한다.
        self.driver.execute_script("window.scrollTo(0, 0);")
        self._wait(self.SELECT_ALL_CHECKBOX)  # 편집 모드 헤더가 렌더링될 때까지 대기

    def click_cancel_edit(self):
        self.click(self.CANCEL_EDIT_LINK)
        self._wait(self.EDIT_LINK)  # 편집 모드 해제(일반 화면 복귀) 대기

    def click_delete_selected(self):
        self.click(self.DELETE_SELECTED_LINK)

    def get_delete_confirm_dialog_text(self):
        # headless 환경에서는 WebElement.text가 렌더링 가시성 판정에 실패해 빈 문자열을
        # 반환하는 경우가 있어(AUTOMATION_GUIDE 7.15절과 동일 패턴), get_attribute
        # ("textContent")로 대체한다.
        return self._wait(self.DELETE_CONFIRM_DIALOG).get_attribute("textContent")

    def confirm_delete(self):
        self.click(self.DELETE_CONFIRM_BUTTON)

    def cancel_delete(self):
        self.click(self.DELETE_CANCEL_BUTTON)

    def click_select_all(self):
        # element_to_be_clickable(가시성 요구)가 이 버튼에서는 영구 타임아웃되는
        # 현상이 있어(원인 불명, AUTOMATION_GUIDE 7.15절), 존재 확인 후 JS로 클릭한다.
        self.click_via_js(self.SELECT_ALL_CHECKBOX)

    def get_selected_count_text(self):
        # 이 span은 .text(가시성 기반) 판정이 불안정해(AUTOMATION_GUIDE 7.15절)
        # textContent를 직접 읽는다.
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: "(" in (driver.find_element(*self.SELECTED_COUNT_TEXT).get_attribute("textContent") or "")
        )
        return self._wait(self.SELECTED_COUNT_TEXT).get_attribute("textContent")

    def item_card_locator(self, index=1):
        return (By.XPATH, f'({self.ITEM_CARD[1]})[{index}]')

    def click_item_card(self, index=1):
        self.click(self.item_card_locator(index))

    def is_item_selected(self, index=1):
        return self._wait(self.item_card_locator(index)).get_attribute("aria-pressed") == "true"

    def get_item_card_count(self):
        return len(self.driver.find_elements(*self.ITEM_CARD))
