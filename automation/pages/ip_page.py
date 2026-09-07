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
