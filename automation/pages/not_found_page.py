from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class NotFoundPage(BasePage):
    MESSAGE_HEADING = (By.XPATH, '//h1[normalize-space(.)="이런, 이미 사라진 페이지군요."]')
    HOME_BUTTON = (By.XPATH, '//button[normalize-space()="홈으로 이동"]')
    FIND_CULPRIT_BUTTON = (By.XPATH, '//button[normalize-space()="범인 찾아보기"]')

    def get_message_text(self):
        return self.get_text(self.MESSAGE_HEADING)
