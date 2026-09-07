import logging

from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from locators.base_locators import BaseLocators

logger = logging.getLogger(__name__)

# 상품 카드에 표시되는 상태 뱃지 라벨 집합(여러 Page Object의 뱃지 판정 로직이
# 공유한다, get_status_badge_text 참고).
STATUS_BADGE_LABELS = {"품절", "판매종료", "예약구매", "NEW"}


class BasePage(BaseLocators):
    def __init__(self, driver):
        self.driver = driver

    def _wait(self, locator, condition=EC.presence_of_element_located):
        try:
            return WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(condition(locator))
        except TimeoutException:
            logger.error("요소 대기 시간 초과: %s", locator)
            raise
        except NoSuchElementException:
            logger.error("요소를 찾을 수 없음: %s", locator)
            raise

    def click(self, locator):
        element = self._wait(locator, EC.element_to_be_clickable)
        # 화면 가장자리 근처 요소가 인접 컴포넌트에 클릭을 가로채이는 것을 방지하기 위해
        # 클릭 전 요소를 화면 중앙으로 스크롤한다(ElementClickInterceptedException 대응).
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"});', element)
        try:
            # 토스트 알림 등 일시적 오버레이가 사라질 때까지 클릭을 재시도한다
            # (오버레이가 사라지지 않아 계속 가로채이면 DEFAULT_TIMEOUT 후 실패).
            WebDriverWait(
                self.driver, DEFAULT_TIMEOUT, ignored_exceptions=[ElementClickInterceptedException]
            ).until(lambda driver: element.click() or True)
        except TimeoutException:
            logger.error("클릭이 계속 다른 요소에 가로채여 시간 초과: %s", locator)
            raise

    def click_via_js(self, locator):
        # 시각적으로 숨겨진 네이티브 입력(예: 커스텀 스타일 체크박스)처럼 항상 장식용
        # 형제 요소가 덮고 있어 일반 클릭이 상시 가로채이는 요소에 사용한다.
        element = self._wait(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        element = self._wait(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        # presence만으로는 headless 환경에서 요소가 논리적으로는 렌더링되었지만
        # 아직 화면에 표시되지 않은 상태의 빈 텍스트를 읽어버릴 수 있어(7.15/7.21절과
        # 동일 유형 재발 방지), 가시성까지 보장한 뒤 읽는다.
        return self._wait(locator, EC.visibility_of_element_located).text

    def get_current_url(self):
        return self.driver.current_url

    def get_status_badge_text(self, card):
        for span in card.find_elements(*self.STATUS_BADGE_SPAN):
            if span.text in STATUS_BADGE_LABELS:
                return span.text
        return None

    def wait_for_url_contains(self, text):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(EC.url_contains(text))
        except TimeoutException:
            logger.error("URL 변경 대기 시간 초과: 기대 문자열 '%s', 실제 URL '%s'", text, self.driver.current_url)
            raise

    def wait_for_url_to_be(self, url):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(EC.url_to_be(url))
        except TimeoutException:
            logger.error("URL 일치 대기 시간 초과: 기대 URL '%s', 실제 URL '%s'", url, self.driver.current_url)
            raise

    def wait_for_text(self, locator, text):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            logger.error("텍스트 변경 대기 시간 초과: 기대 문자열 '%s', locator %s", text, locator)
            raise

    def wait_for_url_change(self, previous_url):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(lambda driver: driver.current_url != previous_url)
        except TimeoutException:
            logger.error("URL 변경 대기 시간 초과: 이전 URL '%s'에서 변경되지 않음", previous_url)
            raise

    def wait_for_attribute_value(self, locator, attribute, value):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                lambda driver: driver.find_element(*locator).get_attribute(attribute) == value
            )
        except TimeoutException:
            logger.error("속성 변경 대기 시간 초과: %s의 '%s' 속성이 '%s'가 되지 않음", locator, attribute, value)
            raise
