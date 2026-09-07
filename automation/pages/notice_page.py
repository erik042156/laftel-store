from locators.notice_locators import NoticeLocators
from pages.base_page import BasePage


class NoticePage(NoticeLocators, BasePage):
    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_content_text(self):
        return self.get_text(self.DIALOG_CONTENT)
