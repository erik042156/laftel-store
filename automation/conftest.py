import datetime
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, LOGIN_EMAIL_URL, LOGIN_LANDING_URL, LOGIN_METHOD, LOGIN_TIMEOUT, WINDOW_SIZE

load_dotenv()

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
    if driver is None:
        return

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{item.name}_failed_{timestamp}.png"
    driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, filename))


def _hide_webdriver_flag(driver):
    # 구글 로그인이 Selenium의 navigator.webdriver 플래그를 감지해
    # "브라우저 또는 앱이 안전하지 않을 수 있습니다"로 차단하는 것을 완화한다
    # (완전한 우회는 아니며, 계속 차단되면 재시도 없이 실패로 보고한다).
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    _hide_webdriver_flag(driver)
    # 기본 창 크기(약 1200x832)에서는 "같은 작품 굿즈" 캐러셀 카드가 서로 겹쳐
    # 클릭이 인접 카드에 가로채이는 문제가 있어, 일반 데스크톱 해상도로 명시한다.
    driver.set_window_size(*WINDOW_SIZE)
    yield driver
    driver.quit()


def _select_first_profile(driver):
    WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.url_contains("/profile"))

    profile_avatar = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="profile"]'))
    )
    profile_avatar.click()

    WebDriverWait(driver, LOGIN_TIMEOUT).until(lambda d: d.current_url != "https://laftel.net/profile")


def _agree_to_store_terms_if_present(driver):
    # 스토어를 처음 이용하는 계정은 "스토어 이용약관 동의" 모달이 뜬다(기존
    # 이메일 계정은 이미 동의한 상태라 겪지 않았던 신규 계정 전용 1회성 온보딩).
    driver.get(BASE_URL)
    try:
        agree_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(.)="동의하고 시작하기"]'))
        )
        agree_button.click()
    except TimeoutException:
        pass


def _login_with_email(driver):
    email = os.environ["TEST_ACCOUNT_EMAIL"]
    password = os.environ["TEST_ACCOUNT_PASSWORD"]

    driver.get(LOGIN_EMAIL_URL)

    email_input = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_input.send_keys(email)

    next_button = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(.)="다음"]'))
    )
    next_button.click()

    password_input = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(.)="로그인"]'))
    )
    login_button.click()

    _select_first_profile(driver)


def _complete_google_login(driver):
    # "구글로 시작" 버튼이 이미 화면에 보이는 상태(라프텔 로그인 랜딩 화면)에서부터
    # 로그인을 끝까지 완료한다. 찜 로그인 유도 팝업의 "로그인" 버튼도 동일한 랜딩
    # 화면(redirect_url 파라미터만 다름)으로 이동하므로 이 헬퍼를 재사용할 수 있다.
    email = os.environ["GOOGLE_ACCOUNT_EMAIL"]
    password = os.environ["GOOGLE_ACCOUNT_PASSWORD"]

    original_window = driver.current_window_handle

    google_button = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="구글로 시작"]'))
    )
    google_button.click()

    # 구글 로그인은 팝업 창(window.open)으로 열린다.
    WebDriverWait(driver, LOGIN_TIMEOUT).until(lambda d: len(d.window_handles) > 1)
    google_window = [h for h in driver.window_handles if h != original_window][0]
    driver.switch_to.window(google_window)
    _hide_webdriver_flag(driver)

    email_input = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "identifierId"))
    )
    email_input.send_keys(email)

    WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.element_to_be_clickable((By.ID, "identifierNext"))).click()

    # 비밀번호 입력란은 이메일 단계에서도 DOM에 숨겨진 채 존재하므로
    # presence가 아닌 visibility로 대기해야 한다.
    password_input = WebDriverWait(driver, LOGIN_TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_input.send_keys(password)

    WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()

    # 로그인이 성공하면 팝업 창이 자동으로 닫히고 원래 창이 laftel.net으로 리디렉션된다.
    WebDriverWait(driver, LOGIN_TIMEOUT).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(original_window)

    _select_first_profile(driver)


def _login_with_google(driver):
    driver.get(LOGIN_LANDING_URL)
    _complete_google_login(driver)


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    if LOGIN_METHOD == "google":
        _login_with_google(driver)
    else:
        _login_with_email(driver)

    _agree_to_store_terms_if_present(driver)

    yield driver
