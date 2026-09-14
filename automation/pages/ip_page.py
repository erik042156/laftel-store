import re

from locators.ip_locators import IpLocators
from pages.base_page import BasePage


class IpPage(IpLocators, BasePage):
    def get_title(self):
        return self.get_text(self.TITLE)

    def is_banner_image_displayed(self):
        title = self.get_title()
        return len(self.driver.find_elements(*self.banner_image_locator(title))) > 0

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

    def get_product_ids(self):
        self._wait(self.PRODUCT_GRID_ITEM)
        links = self.driver.find_elements(*self.PRODUCT_GRID_ITEM)
        product_ids = []
        for link in links:
            # 예약구매 상품은 구매 버튼 문구가 달라 ProductDetailPage.BOTTOM_WISH_ICON
            # 로케이터가 매칭되지 않으므로 제외한다(AUTOMATION_GUIDE 7.12절과 동일 유형).
            if self.get_status_badge_text(link) == "예약구매":
                continue
            match = re.search(r"/products/(\d+)", link.get_attribute("href"))
            if match and match.group(1) not in product_ids:
                product_ids.append(match.group(1))
        return product_ids
