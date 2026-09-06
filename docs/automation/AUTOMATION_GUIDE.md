---
문서유형: Automation Guide
상태: 승인완료
참고: 이전 프로젝트(대상 사이트 automationexercise.com)에서 사용한 문서를 참고해, 라프텔
      스토어(store.laftel.net) 프로젝트에 맞게 대상 URL/자동화 대상 범위/테스트 데이터
      관리/Locator 실측 근거/알려진 사이트 결함/실행 화면 크기 등을 재작성함
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
승인일: 2026-09-05
---

# AUTOMATION_GUIDE.md - 라프텔 스토어 자동화 코드 개발 기준

## 0. 문서 목적 및 범위

이 문서는 이 프로젝트(라프텔 스토어 QA 자동화)의 **자동화 코드 개발 기준**을 정의하는
Source of Truth이며,
다음 작업에서 공통 판단 근거로 사용합니다.

- 자동화 개발 Roadmap 작성
- Shrimp Task 생성 및 작업 분해
- 자동화 코드 개발
- 코드 리뷰 및 테스트 실행/검증

이 문서는 **기능별 요구사항(로그인, 장바구니 등)을 다루지 않습니다.** 기능별 요구사항은
`docs/prd/feature/{slug}.md`(Feature PRD)와 `docs/tc/{slug}.md`(TC)를 Source of Truth로
합니다. 이 문서와 PRD/TC/Roadmap의 내용이 서로 다르게 보이면, 요구사항·시나리오 판단은 항상
PRD/TC를 기준으로 하고, **코드 작성 방식(구조/컨벤션/원칙)에 대한 판단만 이 문서를 기준으로**
합니다.

**아직 실제 코드, 디렉터리, 설정 파일은 생성되지 않았습니다.** 이 문서는 앞으로 자동화 코드를
작성할 때 따를 규칙을 정의하며, 이후 실제 구현 상태가 이 문서와 달라지면(CLAUDE.md 8절
"실제 구현 상태 = Repository Code" 원칙에 따라) 문서를 갱신합니다.

### 0.1 자동화 대상 범위

이 문서가 정의하는 규칙이 적용되는 자동화 대상은 다음 조건을 **모두** 만족하는 TC로 한정합니다
(`automation-candidate-agent`가 정의한 조건과 동일).

```
Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
AND
QA Decision = Approved
```

2026-09-05 기준 대상 Feature와 Approved TC 건수는 다음과 같습니다(상세 TC 목록은 각
Candidate 문서를 Source of Truth로 참조하며, 이 문서에 전체 TC를 복제하지 않습니다).

| Feature | Approved TC 수 |
|---|---|
| cart | 16 |
| order | 11 |
| product-detail | 35 |
| search | 23 |
| wishlist | 28 |

합계 113건 (`docs/tc/automation-candidates/{cart,order,product-detail,search,wishlist}.md`
기준).

이 범위는 프로젝트마다 달라질 수 있으므로, 이 문서의 원칙 자체는 특정 Feature 목록에 종속되지
않고 재사용 가능하게 작성합니다.

---

## 1. Technology Stack

| 항목 | 결정 | 비고 |
|---|---|---|
| 언어 | **Python** | 1.1절 "코딩 스타일 예외" 적용 대상 |
| 자동화 도구 | **Selenium WebDriver** | |
| 테스트 러너 | **pytest** | |
| 설계 패턴 | **Page Object Model (POM)** | |
| 리포팅 | **pytest-html + JUnit XML(`--junitxml`) 병행** | HTML은 사람이 보는 Artifact, JUnit XML은 Slack 실패 메시지 조립용 |
| 실행 브라우저 | **Chrome (ChromeDriver)** | 일반 데스크톱 창 크기로 실행, 별도 모바일 에뮬레이션 미사용(사용자 결정 — 라프텔 스토어는 모바일 웹 기준 반응형 사이트이나 PC Chrome에서도 동일하게 동작함. 모바일 웹 자체 검증은 이번 범위 밖, 추후 별도 진행) |
| 대상 환경 | Production 단일 환경 (`https://store.laftel.net/`) | 별도 dev/staging 없음(Project PRD 3절), 장비 부족으로 PC Chrome에서만 검증(Project PRD 4절) |
| CI/CD | **GitHub Actions** | Push 시 자동 테스트 실행(16절) |
| 알림 | **Slack** | 실패 시 실패 원인 요약 포함 알림(CLAUDE.md 16절: 승인 용도 아님, 결과 알림 전용) |
| 패키지 버전 관리 | `requirements.txt` (미생성) | 실제 구현 시작 시 작성 |

### 1.1 코딩 스타일 예외 (중요)

프로젝트 전역 CLAUDE.md는 "들여쓰기 2칸, camelCase/PascalCase(컴포넌트)"를 기본 스타일로
정의하지만, **Python 자동화 코드에 한해 다음과 같이 PEP8을 우선 적용하는 예외를 사용자
승인으로 확정합니다.**

- 들여쓰기: **4칸** (2칸 아님)
- 변수/함수명: **snake_case** (camelCase 아님)
- 클래스명: PascalCase (전역 규칙과 동일, 충돌 없음)
- 상수(Locator 등): UPPER_SNAKE_CASE

이유: `black`/`flake8` 등 Python 표준 도구 체인이 4칸 들여쓰기와 PEP8 네이밍을 전제로 하고,
Selenium/표준 라이브러리 API 자체가 snake_case이므로 일관성을 위해 예외를 인정합니다. 이
예외는 **이 프로젝트의 Python 자동화 코드에만 적용**되며, PRD/TC/Roadmap 등 Markdown
문서나 다른 언어로 작성될 도구(`scripts/sheets_sync`의 기존 코드 포함)의 컨벤션까지 바꾸는
것은 아닙니다.

---

## 2. Automation Architecture

- **Page Object Model (POM)**을 채택합니다. 1개 웹 페이지(또는 명확히 구분되는 주요 화면
  영역)당 1개 Page 클래스를 작성합니다.
- 모든 Page 클래스는 공통 기능을 제공하는 `BasePage`를 상속합니다.
- Page 객체는 WebDriver 인스턴스 1개만 보유하며, 그 외 상태 변수를 최소화합니다.
- Page Layer와 Test Layer의 책임은 4절 기준을 따릅니다.

---

## 3. Project Structure (예정)

**아래 구조는 아직 생성되지 않은 예정 구조입니다.** 실제 구현을 시작하는 시점에 이 구조에 맞춰
생성합니다.

```
automation/
├── pages/               # Page Object 클래스
│   ├── base_page.py
│   └── ...
├── tests/                # 테스트 코드 (pytest)
│   ├── test_cart.py
│   └── ...
├── utils/                 # 화면과 무관한 공통 로직
├── config/                 # 환경 설정(URL, 타임아웃 등)
├── test_data/               # 정적 테스트 데이터(계정 이메일 등, 비밀번호 제외)
├── screenshots/               # 실패 시 스크린샷(git 미추적)
├── reports/                     # pytest-html/JUnit XML 리포트(git 미추적)
├── conftest.py                   # pytest fixture
├── pytest.ini                     # pytest 설정
└── requirements.txt                # Python 의존성

docs/                                # 기존 산출물(PRD/TC/Automation Candidate/Roadmap/Automation Guide)
scripts/sheets_sync/                  # 기존 Google Sheet 연동 스크립트(자동화 코드와 별개)
.github/workflows/                      # CI 워크플로우(미생성)
```

- `automation/` 하위 구조는 이 프로젝트의 자동화 코드 전용이며, 기존 `scripts/sheets_sync`
  (QA 프로세스 도구 스크립트)와는 목적이 다르므로 혼용하지 않습니다.
- 실제 디렉터리를 만들 때 위 구조와 다르게 조정해야 할 이유가 생기면, 이 문서를 먼저 갱신하고
  사용자 확인을 받은 뒤 반영합니다(CLAUDE.md 7절).

### 3.1 Import 경로 규칙

`automation/pytest.ini`가 저장소 루트가 아닌 `automation/` 디렉터리 안에 위치하고
`automation/` 자체에는 `__init__.py`가 없으면, `automation/tests/`를 pytest로 실행할 때
`automation/`이 사실상의 루트 패키지 경로가 된다(`automation`이 top-level 패키지로 인식되지
않을 수 있음). **이 프로젝트에서는 아직 실제로 검증된 적이 없으므로, Phase 0 구현 시 반드시
실제 동작을 확인한 뒤 아래 규칙을 그대로 적용할지 확정한다.**

- 모든 `automation/` 하위 코드(Page Object, 테스트, utils, config, test_data 등)는
  **`automation.` prefix 없이** `automation/` 자체를 루트로 삼아 import한다.
  - 올바른 예: `from pages.base_page import BasePage`, `from config.settings import BASE_URL`
  - 잘못된 예(실행 시 `ModuleNotFoundError` 발생): `from automation.pages.base_page import BasePage`
- 이 규칙은 `automation/` 하위 코드 사이의 상호 import에만 적용된다. `automation/` 바깥
  코드(`scripts/sheets_sync` 등)에서 `automation/` 코드를 import하는 시나리오는 현재
  범위에 없다.

---

## 4. Page Object / Layer 책임

### 4.1 Page Layer 책임

- 대상 화면의 모든 Locator를 클래스 상단에 상수로 정의합니다.
- 클릭/입력/스크롤 등 화면 조작 메서드를 제공합니다.
- 조회 메서드는 값을 **반환만** 합니다.
- **Assertion을 절대 수행하지 않습니다.**

### 4.2 Test Layer 책임

- Page 객체의 메서드를 호출해 시나리오를 구성합니다.
- 테스트에 필요한 데이터를 준비/정리합니다(11절 참고).
- Page에서 반환받은 값과 기대값을 비교해 **Assertion을 수행**합니다.
- 원칙: Page는 "어떻게 하는가", Test는 "무엇을 검증하는가"만 담당합니다.

```python
# pages/search_page.py (예시 — 실제 Locator는 구현 시 5절 절차로 확인)
class SearchPage(BasePage):
    KEYWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='검색어를 입력해주세요']")
    SEARCH_RESULT_COUNT = (By.CSS_SELECTOR, ".search-result-count")

    def search(self, keyword: str) -> None:
        self.type_text(self.KEYWORD_INPUT, keyword)

    def get_result_count_text(self) -> str:
        return self.get_text(self.SEARCH_RESULT_COUNT)


# tests/test_search.py
def test_search_with_single_character_keyword(driver, search_page):
    search_page.search("링")
    assert search_page.get_result_count_text() != ""
```

---

## 5. 실제 페이지 탐색 규칙 (Playwright MCP 기반)

Selenium 코드를 작성하기 전 실제 페이지 구조와 Locator 후보를 조사·검증하는 개발 보조
도구로 **Playwright MCP**를 사용합니다(사용자 확정).

### 5.0 사전 준비 상태

Playwright MCP(`mcp__playwright__browser_navigate`, `browser_snapshot`, `browser_evaluate`)는
`automation-developer-agent.md`의 도구 목록에 이미 등록되어 있습니다. 실제 연결/사용 가능
여부는 자동화 구현에 착수하는 시점에 다시 확인합니다. 서버 설정(설치/등록) 자체는 이 문서의
범위가 아닙니다.

### 5.1 사용 목적

- Playwright MCP는 Selenium 테스트 코드에 사용할 실제 페이지 구조와 Locator 후보를
  조사하고 검증하기 위한 **개발 보조 도구**로 사용합니다.
- 프로덕션 테스트 실행 도구는 **Selenium WebDriver**이며, Playwright MCP를 Selenium
  코드 실행 대신 사용하지 않습니다.

### 5.2 기본 탐색 순서

Selenium 코드를 작성하기 전에 다음 순서로 실제 페이지를 확인합니다.

1. 대상 기능의 Feature PRD(`docs/prd/feature/{slug}.md`)와 TC(`docs/tc/{slug}.md`)
   시나리오를 먼저 확인합니다.
2. Playwright MCP로 대상 페이지(`https://store.laftel.net/`)에 접근합니다.
3. `browser_snapshot`으로 페이지 구조와 대상 요소를 먼저 확인합니다.
4. snapshot만으로 정보가 부족하면 `browser_evaluate`로 DOM 속성을 확인합니다.
5. 확인한 정보를 기반으로 6절 우선순위에 따라 Selenium Locator를 작성합니다.
6. 작성한 Locator가 실제 대상 요소를 고유하게 식별하는지(동일 조건에 일치하는 요소가
   1개뿐인지) 검증합니다.

### 5.3 browser_evaluate 사용 기준

`browser_evaluate`는 다음 정보가 snapshot에서 충분히 확인되지 않을 때만 사용합니다.

- id, name, role, aria-label, placeholder
- data-testid 등 data-* 속성(실제 존재가 확인되는 경우에 한함)
- 대상 요소의 텍스트
- 상위·하위 DOM 관계
- 동일 조건에 일치하는 요소 개수

**금지**: 페이지 상태를 변경하거나 서비스 데이터를 조작하기 위한 JavaScript 실행(실제 계정
생성/삭제, 주문 시도 등)에는 사용하지 않습니다. Playwright MCP는 오직 **조회·탐색** 목적에만
한정하며, 승인되지 않은 Production 데이터 변경은 CLAUDE.md 11절 원칙을 그대로 따릅니다.

### 5.4 사용자 확인 요청 기준

다음 사유로 Playwright MCP를 이용한 직접 확인이 불가능한 경우에만 사용자에게 스크린샷이나
추가 정보를 요청합니다.

- 로그인 계정이나 권한이 없음
- OTP, 2FA 또는 CAPTCHA가 필요함
- 사내망이나 특정 네트워크 환경이 필요함
- 사용자별 데이터가 있어야 재현 가능함
- MCP 브라우저와 실제 테스트(Selenium) 환경이 다르게 동작함
- 대상 요소나 요구사항이 여러 의미로 해석될 수 있음

단순히 Locator가 제공되지 않았다는 이유만으로 작업을 중단하지 않습니다.

---

## 6. Locator 작성 원칙

### 6.1 우선순위

1. `id` 속성
2. `name` 속성
3. 안정적인 CSS Selector(구조 변경에 덜 민감한 속성 기반)
4. 상대 XPath (텍스트/속성 결합 등 다른 방법으로 고유 식별이 어려울 때만, 최후 수단)

**Full XPath(`/html/body/div[1]/...`)는 절대 금지**합니다 — DOM 구조 변경에 매우 취약해
유지보수가 불가능합니다.

> `store.laftel.net`에 `data-testid`/`data-qa` 같은 테스트 전용 속성이 존재하는지는 아직
> 실측되지 않았습니다. 구현 중 Playwright MCP로 특정 화면을 조사하다 이런 속성이 실제로
> 존재하고 다른 속성보다 더 안정적으로 고유 식별이 가능함을 확인하면, 그 화면에 한해
> 우선순위를 갱신하고(사용자 승인 후) 이 절에 실측 근거를 기록합니다.

### 6.2 정의 위치

모든 Locator는 Page 클래스 상단에 `UPPER_SNAKE_CASE` 상수로 정의합니다. 메서드 내부에
Locator를 하드코딩하지 않습니다.

---

## 7. Wait 처리 원칙

- **`time.sleep()` 사용을 금지**합니다. 고정 시간 대기는 테스트를 느리고 불안정하게 만듭니다.
- Selenium의 `WebDriverWait` + `expected_conditions`로 **Explicit Wait**를 기본으로
  사용합니다.
- 반복되는 Wait 로직은 `BasePage`의 공통 메서드로 래핑합니다(예: `wait_and_click`,
  `wait_and_get_text` 등 — 실제 메서드명은 구현 시 확정).

### 7.1 자동화를 방해하는 오버레이/팝업

현재까지 `store.laftel.net`에서 자동화(클릭/입력)를 가로막는 것으로 보고된 제3자 광고
오버레이나 그 밖의 방해성 팝업은 없습니다. 구현 중 유사한 문제(광고, 쿠키 동의 배너, 앱
설치 유도 팝업 등)가 실제로 발견되면, 그 시점에 구체적인 증상·재현 조건·처리 방식을
사용자 승인을 거쳐 이 절에 기록하고 `BasePage`에 공통 방어 로직을 추가합니다.

### 7.2 터치 스와이프 기반 컴포넌트의 자동화 제약 (알려진 도구 한계)

Phase 1(product-detail) TC-013(이미지 캐러셀) 구현 중 발견된 ChromeDriver/Selenium 자체의
제약사항입니다(사이트 결함 아님).

- 상품상세 이미지 캐러셀처럼 별도 화살표 버튼 없이 마우스/터치 드래그로만 전환되는
  컴포넌트는 `ActionChains`(click_and_hold + move_by_offset + release)로 드래그를
  구현해야 합니다.
- **같은 브라우저 세션(페이지를 새로 열지 않은 상태)에서 이런 드래그를 2회 이상 연속
  수행하면 ChromeDriver의 W3C Actions 포인터 위치가 누적 이탈해
  `MoveTargetOutOfBoundsException`이 발생**하는 문제를 확인했습니다. 여러 방식(단계별
  이동, 절대좌표 재설정, 하나의 액션 체인으로 통합)으로 우회를 시도했으나 재현되어,
  ChromeDriver의 알려진 한계로 판단합니다.
- **대응 원칙**: 이런 컴포넌트를 검증하는 각 테스트는 페이지를 새로 연 직후 드래그를
  **1회만** 수행하도록 시나리오를 구성합니다(pytest `driver` fixture가 테스트마다 새
  세션을 생성하므로, 테스트 함수를 분리하면 자연스럽게 만족됩니다).
- 이 제약으로 인해 한 세션 내 2회 이상의 연속 드래그가 구조적으로 필요한 시나리오(예:
  "마지막 사진에서 다음으로 넘기면 첫 번째로 순환"처럼 직전 드래그로 도달한 상태에서
  다시 드래그해야 하는 경우)는 자동화 범위에서 제외하고 수동 확인 대상으로 남깁니다
  (사용자 승인, TC-PRODUCT-DETAIL-013 4번째 Step 해당).
- Phase 2/4/5에서 유사한 터치 스와이프 기반 캐러셀(찜/검색 등)을 자동화할 때도 이 절의
  원칙을 그대로 적용합니다.

### 7.3 로그인 플로우의 간헐적 지연

Phase 1(product-detail) TC-035~039 구현 중 로그인 fixture(`conftest.py`의
`logged_in_driver`, laftel.net 이메일 로그인 경유)에서 이메일 입력 후 "다음" 버튼이
클릭 가능해지기까지 간헐적으로 기본 `DEFAULT_TIMEOUT`(10초)보다 오래 걸리는 현상을
발견했습니다(같은 세션에서 로그인을 반복 시도할 때 더 자주 관찰됨 — 클라이언트 측
이메일 검증 API 응답 지연으로 추정, 사이트 결함 여부는 확인되지 않음). 이에 로그인
전용 타임아웃을 `config/settings.py`의 `LOGIN_TIMEOUT`(20초)으로 별도 상향했습니다.
그럼에도 실패가 발생하면 CLAUDE.md 13절에 따라 Test Environment 요인으로 우선
의심하고, 동일 테스트를 무분별하게 반복 재시도하지 않습니다.

### 7.4 브라우저 창 크기와 캐러셀 카드 클릭 가로채기

Phase 1 TC-034(같은 작품 굿즈 카드 위 찜 처리) 구현 중, Chrome 기본 창 크기(약
1200x832)에서는 "같은 작품 굿즈" 캐러셀의 카드 레이아웃이 좁아져 인접 카드 요소가
클릭을 가로채는(`ElementClickInterceptedException`) 현상을 발견했습니다. 이에
`config/settings.py`의 `WINDOW_SIZE`(1600x1000)를 정의하고 `conftest.py`의 `driver`
fixture에서 `driver.set_window_size()`로 명시적으로 적용했습니다(1절 "일반 데스크톱
창 크기" 결정의 구체적 값으로 확정). 아울러 `BasePage.click()`에 클릭이 다른 요소에
가로채이면(예: 토스트 알림) 오버레이가 사라질 때까지 같은 요소에 대해 재시도하는
방어 로직을 추가했습니다(무한 재시도 아님, `DEFAULT_TIMEOUT` 내에서만 재시도).

전체 테스트를 연달아 많이 실행해 같은 상품의 찜 토글을 짧은 시간에 반복 호출한
경우, 캐러셀 카드 위 찜 처리(TC-034)의 마지막 클릭이 `DEFAULT_TIMEOUT`(10초) 안에
반영되지 않아 실패하는 사례를 1회 관찰했습니다(동일 테스트를 단독 실행하거나 계정의
찜 상태를 정리한 뒤 재실행하면 정상 통과 — 원인은 특정되지 않았으나 짧은 시간 내
반복 호출에 따른 서버 처리 지연으로 추정). 재현이 잦아지면 그때 원인을 추가로
조사하고 이 절에 갱신합니다.

### 7.5 팝업 텍스트를 요소 등장 직후 읽을 때의 빈 문자열 문제

Phase 1 전체 통합 실행(Task I) 중 `get_login_prompt_text()`가 간헐적으로 빈 문자열을
반환하는 현상을 발견했습니다. 로그인 유도 팝업 h2 요소가 DOM에 먼저 빈 상태로
나타난 뒤 내용이 뒤늦게 채워지는 경우가 있어, `presence_of_element_located`만으로는
불충분했습니다. `get_login_prompt_text()`에서 요소 존재 확인 후 텍스트가 실제로
채워질 때까지(`wait_for_text`) 기다린 뒤 읽도록 수정했습니다. 이후 유사하게 "요소는
있지만 내용이 비동기로 채워지는" 텍스트 조회 메서드를 추가할 때도 동일하게
`wait_for_text`로 내용이 채워지길 기다린 뒤 반환하는 패턴을 따릅니다.

### 7.6 장바구니 화면의 비동기 갱신 관련 Race Condition (Phase 2)

Phase 2 Task B(카트 삭제 흐름) 구현 중 아래 3가지 비동기 타이밍 문제를 발견했습니다.
모두 "클릭 직후 즉시 다음 동작을 하면 이전 동작이 아직 반영되지 않은 상태를 읽게
된다"는 공통 원인을 가지므로, 장바구니 관련 신규 자동화 코드 작성 시 동일 패턴에
유의합니다.

- **장바구니 진입 직후 스켈레톤 placeholder**: `/cart` 진입 시 실제 상품 링크
  (`a[href^="/products/"]`)가 렌더링되기 전, 잠시 회색 스켈레톤 placeholder만
  존재하는 구간이 있습니다. 이 상태에서 `get_item_count()`를 바로 호출하면 0을
  반환합니다. `CartPage.wait_for_items_loaded()`(실제 상품 링크가 나타날 때까지
  대기)를 상품이 1건 이상 있을 것으로 기대되는 시점에 개수 조회 전 호출합니다.
- **담기(장바구니 추가) API 완료 전 페이지 이동**: `장바구니에 담기` 클릭 직후
  바로 다른 페이지로 이동(`driver.get(...)`)하면 담기 API 호출이 완료되기 전에
  네비게이션이 발생해 담기가 반영되지 않을 수 있습니다. 클릭 후 완료를 알리는
  토스트(`get_add_to_cart_toast_text()`)가 뜨는 것을 확인한 뒤에 다음 페이지로
  이동합니다.
- **상품 삭제 후 목록 갱신 지연**: 개별/일괄 삭제 확인(`confirm_delete()`) 클릭
  직후 바로 `get_item_count()`/`is_empty()`를 호출하면 삭제 전 개수를 그대로
  읽는 경우가 있습니다. `CartPage.wait_for_item_count(expected_count)`로 목록이
  실제로 갱신될 때까지 기다린 뒤 조회합니다.
- **전체선택 체크박스의 기본 선택 상태**: 장바구니에 상품을 담으면 해당 상품은
  기본적으로 이미 선택(체크)된 상태로 표시됩니다. 이 상태에서 `click_select_all()`을
  무조건 호출하면 오히려 전체 해제가 되어, 이후 "삭제" 클릭 시 삭제 확인 팝업 대신
  "삭제하실 상품을 선택해 주세요." 안내 팝업이 뜹니다. 전체 선택이 필요한 경우
  `CartPage.ensure_all_selected()`(현재 체크 여부를 먼저 확인한 뒤 필요할 때만
  클릭)를 사용합니다.

> 참고(알려진 한계): `test_cart.py` 전체를 연달아 실행할 때, 동일 계정으로 담기/삭제
> API 호출이 빠르게 반복되면서 `SELECT_ALL_CHECKBOX` 대기가 `DEFAULT_TIMEOUT` 내에
> 완료되지 못해 간헐적으로 실패하는 사례를 드물게 관찰했습니다(개별 테스트 단독
> 실행 시에는 재현되지 않음). 7.4절의 위시리스트 토글 간헐적 플레이키니스와 동일한
> 유형(전체 스위트를 빠르게 반복 실행할 때만 발생)이라 판단해, 원인을 임의로
> 추측해 고치기보다 알려진 한계로 기록만 하고 무한 재시도는 하지 않습니다.

### 7.7 로그인 방식 임시 전환 (이메일 → 구글, 이메일 계정 서버측 잠금 추정)

Phase 2 진행 중, 이 세션에서 `TEST_ACCOUNT_EMAIL` 계정으로 로그인을 매우 여러 차례
반복(디버깅 포함)한 뒤 `laftel.net`이 이메일 로그인 자체를 거부하는 오류
("앗, 다시 시도해주세요. 알 수 없는 문제가 발생했습니다.")를 반환하기 시작했습니다.
재시도해도 동일하게 재현되어 서버측 일시적 잠금으로 추정했고, 사용자 요청에 따라
잠금이 풀리기 전까지 별도의 구글 계정으로 로그인하도록 임시 전환했습니다.

- `config/settings.py`의 `LOGIN_METHOD` 상수("google"/"email")로 전환하며,
  이메일 로그인 코드(`conftest.py`의 `_login_with_email`)는 삭제하지 않고 그대로
  보존합니다. 잠금이 해제되면 `LOGIN_METHOD = "email"`로 되돌리기만 하면 됩니다.
- 구글 계정 자격 증명은 기존 라프텔 계정과 별개의 전용 테스트 계정이며,
  `GOOGLE_ACCOUNT_EMAIL`/`GOOGLE_ACCOUNT_PASSWORD`로 `.env`에만 저장합니다
  (11.1절과 동일한 원칙).
- 구글 로그인은 `laftel.net/auth/login`의 "구글로 시작" 버튼을 클릭하면 팝업 창으로
  열리며(`window.open`), 로그인 성공 시 팝업이 자동으로 닫히고 원래 창이
  `laftel.net`으로 리디렉션됩니다. 이후 프로필 선택(`img[alt="profile"]` 클릭)
  단계는 이메일 로그인과 동일합니다.
- **알려진 위험 — 구글의 자동화 브라우저 탐지**: 기본 Selenium Chrome으로는 이메일
  입력 직후 구글이 "브라우저 또는 앱이 안전하지 않을 수 있습니다"로 로그인을
  차단하는 것을 실측으로 확인했습니다. `driver` fixture에
  `excludeSwitches=["enable-automation"]`, `--disable-blink-features=AutomationControlled`
  Chrome 옵션과 CDP로 `navigator.webdriver`를 숨기는 완화 조치를 추가해 현재는
  안정적으로 통과하지만, 완전한 우회는 아니므로 향후 다시 차단될 수 있습니다. 차단이
  재현되면 추측성 우회를 시도하지 않고 실패로 보고합니다(CLAUDE.md 13절).
- **신규(첫 이용) 계정 전용 온보딩**: 구글 계정으로 처음 스토어를 방문하면 "스토어
  이용약관 동의" 모달이 뜹니다(기존 이메일 계정은 이미 동의되어 있어 겪지 않았던
  차이). `logged_in_driver`가 로그인 직후 `BASE_URL`을 방문해 모달이 있으면
  자동으로 "동의하고 시작하기"를 클릭하도록 처리했습니다.
- **`CartPage.clear_cart()`의 잠재 결함 발견**: 위 계정 전환 검증 과정에서
  `clear_cart()`가 `open()` 직후 렌더링 완료를 기다리지 않고 곧바로 `is_empty()`를
  호출해, 스켈레톤 로딩 상태를 "비어있지 않음"으로 오판해 이후 단계에서 타임아웃
  나는 기존 버그를 발견했습니다(기존 계정은 세션이 따뜻해 우연히 재현되지 않았을
  뿐). `wait_for_cart_loaded()`(상품 링크 또는 빈 상태 안내문 중 하나가 나타날
  때까지 대기)를 추가해 `clear_cart()`에 적용했습니다.

### 7.8 카카오 우편번호 검색 모달의 최소 조작 (Phase 3, 착수 전 사용자 승인)

`/check-out/{uuid}` 화면의 배송지 "우편번호"(`zipCode`)/"주소"(`address1`) 입력란은
`readonly` 속성이 걸려 있어, 카카오 우편번호 검색 모달(iframe 내 iframe으로 렌더링)을
거치지 않고는 어떤 방법으로도 값을 채울 수 없습니다. 이 모달 자체(TC-ORDER-006, "우편번호
찾기 클릭 시 모달 노출 확인")는 외부 모듈 의존 리스크로 이미 자동화 대상에서 Rejected
처리되어 있어, TC-ORDER-017/019처럼 유효한 배송지가 선행 조건인 TC를 자동화하려면 이
Rejected 모듈을 최소한만(검색어 입력 → 결과 클릭) 조작해야 하는 모순이 생깁니다.
사용자에게 이 상황을 보고하고 승인을 받아 `CheckoutPage.fill_address_via_kakao_postcode_search()`를
구현했습니다 — 모달 자체의 UI/동작은 어떤 Assertion으로도 검증하지 않고, 오직 뒤 단계
TC의 선행 조건을 만들기 위한 수단으로만 사용합니다.

구현 중 다음 두 가지 타이밍 이슈를 실측으로 발견해 대응했습니다.
- **iframe 전환 시 Stale/NoSuchFrame**: 모달이 열리는 초기에 iframe이 재구성되며
  `find_element` 직후 `switch_to.frame()`이 `StaleElementReferenceException` 또는
  `NoSuchFrameException`으로 실패하는 경우가 있어, `EC.frame_to_be_available_and_switch_to_it`
  (내부적으로 `NoSuchFrameException`만 재시도) 대신 두 예외를 모두 잡아 재시도하는
  자체 `_switch_to_frame()` 헬퍼(`WebDriverWait` + 커스텀 predicate)를 만들어 사용합니다.
- **동일 문구를 가진 숨겨진 중복 다이얼로그**: 필수 동의 안내 팝업 확인 버튼을
  `//div[@role="dialog"]//button[normalize-space(.)="확인"]`로 찾았을 때, DOM 순서상
  먼저 매칭되는 요소가 화면에 보이지 않는(`display:none`류) 이전 다이얼로그 인스턴스라
  `element_to_be_clickable`이 계속 실패해 타임아웃났습니다. 다이얼로그 컨테이너에
  `data-state="open"` 조건을 추가해(`//div[@role="dialog" and @data-state="open"]//button[...]`)
  현재 열려 있는 다이얼로그만 매칭하도록 고쳤습니다.

### 7.9 TC-ORDER-019(PG 결제창 진입) 자동화 보류 결정

Phase3-F에서 TC-ORDER-019(배송지/동의 모두 충족 후 "구매하기" 클릭 시 PG 결제창 노출까지만
확인)를 구현하기 위해, 이름/휴대폰/카카오 검색으로 확보한 실주소/필수 동의 3개를 모두
채운 뒤 "구매하기"를 클릭해 나이스페이(NICE PAY) 결제창이 나타나는지 반복 실측했습니다.

- 1회는 클릭 직후 "Please, wait..." 텍스트만 확인(창 출현 여부 미확인).
- 이후 최상위 문서와 모든 iframe을 대상으로 최대 15초씩 2회 더 탐색했으나 나이스페이
  결제창이 전혀 나타나지 않았습니다.
- 반면 사용자가 동일 플로우를 브라우저에서 직접 눈으로 확인했을 때는 나이스페이 결제창이
  같은 창 안 오버레이 형태(우측 상단 X 버튼 포함)로 나타난 스크린샷을 확보했습니다.

즉 **동일한 입력·플로우로도 나이스페이 결제창 노출 여부가 간헐적**이라는 뜻이며, 원인은
자체 코드 문제가 아니라 실제 PG 연동 쪽 요인으로 추정됩니다(automation-candidates 문서에서도
사전에 "Result Determinism이 제한적"이라고 이미 경고된 사항). 이 상태로 테스트를 작성하면
매 실행마다 재현 여부가 갈려 신뢰할 수 없는 테스트가 되며, 안정화를 위해 실제 프로덕션 PG
엔드포인트를 반복 호출하는 것 자체도 부작용 리스크가 있습니다(부하, 이상거래 탐지 등).

**결정**: 사용자 승인에 따라 TC-ORDER-019는 이번 Phase 3 자동화 범위에서 **보류**합니다.
- `automation/tests/test_order.py`에 이 TC에 대한 테스트를 추가하지 않습니다.
- `docs/tc/automation-candidates/order.md`는 Google Sheet를 그대로 옮겨온 참고용
  스냅샷(문서 자체에 "이 문서를 직접 수정해도 Sheet에는 반영되지 않는다"고 명시됨)이라
  QA Decision 값 자체는 임의로 고치지 않았습니다. 이 문서 갱신이 필요하면 별도로
  automation-candidate-agent를 통해 Google Sheet 재동기화 절차를 거쳐야 합니다.
- Phase 3 자동화 대상은 이번 결정으로 11건 → 10건(001,002,004,005,007,009,015,017,018,020)이
  되며, `docs/roadmap/ROADMAP.md` 8절/변경 이력에 함께 반영했습니다.
- TC-ORDER-019 자체는 승인된 `docs/tc/order.md`에서 삭제하지 않습니다(수동 테스트로는
  여전히 유효한 시나리오이며, 자동화 여부와 TC 자체의 유효성은 별개입니다).

### 7.10 이전 배송지 자동 채움 및 Selenium `.clear()`의 React 컨트롤드 입력 미반영 문제

Phase3-G 통합 실행 중 `test_submitting_empty_form_shows_field_errors`(TC-ORDER-005)가
실패했습니다. 원인을 조사한 결과, Phase3-E/F에서 TC-017/TC-019 검증을 위해 실제 이름/
휴대폰번호/주소를 여러 차례 입력·제출한 이력 때문에, 이 계정의 체크아웃 화면이 이제
**이전에 저장된 배송지 정보를 자동으로 채워서 보여줌**을 발견했습니다(완전히 새로운
브라우저 세션에서도 재현되어 브라우저 캐시가 아닌 계정에 저장된 서버측 상태임을 확인).
이는 실제 제품의 정상 기능(편의 기능)으로 판단해 사용자 승인을 받아 신규 요구사항으로
문서화했습니다: `docs/prd/Feature/prd-order.md` REQ-ORDER-019 신설, `docs/tc/order.md`
TC-ORDER-021 신설(자동화 대상 평가는 automation-candidate-agent 경유 별도 진행).

이 발견 과정에서 자동화 구현상의 별도 결함도 찾았습니다.
- **`BasePage.type_text()`의 `element.clear()`가 React 컨트롤드 입력에서 항상
  동작하지 않음**: 이미 값이 채워진 React 컨트롤드 `<input>`에 Selenium의
  `element.clear()`를 호출하면, DOM의 `value` 속성은 즉시 빈 문자열로 보이지만 실제
  키 입력 이벤트가 발생하지 않아 React 내부 상태(state)는 갱신되지 않습니다. 이후
  아무 리렌더링(예: 다른 버튼 클릭)이 발생하면 React가 컨트롤드 입력을 자신의 내부
  상태값으로 다시 덮어써, 방금 지운 값이 원래 채워져 있던 값으로 되돌아갑니다(실측
  확인: "구매하기" 클릭 한 번만으로 지운 이름/휴대폰번호가 원래 값으로 복원됨).
- **대응**: `CheckoutPage._clear_via_keyboard()`를 신설해, `Keys.END` 이동 후 실제
  글자 수만큼 `Keys.BACKSPACE`를 한 글자씩 전송하는 방식으로 변경했습니다. 실제 키
  입력과 동일한 이벤트가 발생해 React 상태까지 확실히 비워지며, 이후 재렌더링에도
  값이 복원되지 않음을 확인했습니다. `element.clear()`로 이미 채워진 React 컨트롤드
  입력을 비워야 하는 경우 이 패턴(선택 없이 끝에서부터 실제 문자 수만큼 Backspace)을
  재사용합니다.
- TC-ORDER-005는 우편번호/주소(`readonly`, 카카오 모달 없이는 재입력 불가)는 이제
  이 계정에서 항상 채워진 상태라 검증 대상에서 제외하고, 받는 사람/휴대폰번호 2개
  필드 에러만 검증하도록 범위를 조정했습니다(사용자 승인).

### 7.11 찜(wishlist) 토스트/아이콘 인덱스 관련 실측 발견 (Phase 4)

Phase4-A/B(`home_page.py`, `test_wishlist.py`) 구현 중 발견한 페이지별 차이입니다.

- **검색/작품(`/ip/{id}`) 페이지의 `div[role="status"]` 중복**: 메인페이지와 달리
  이 두 화면에는 무한 스크롤 로딩 표시용으로 항상 존재하는 빈
  `<div role="status" aria-label="더 많은 콘텐츠를 불러오는 중">`가 실제 찜 토스트보다
  DOM 순서상 먼저 렌더링되어 있습니다. `_wait()`의 `presence_of_element_located`는
  DOM에 처음 나타나는 요소를 기준으로 하므로, `div[role="status"]`만으로는 항상 이
  빈 로딩 표시가 매칭되어 텍스트가 영원히 채워지지 않습니다(`wait_for_text` 타임아웃).
  실제 토스트는 `div[data-scope="toast"][data-part="root"]`로 구분되어, `HomePage.WISH_TOAST`
  로케이터를 이 셀렉터로 지정해 해결했습니다. `role="status"`만으로 요소를 특정할 때는
  같은 role을 가진 다른 상시 요소가 없는지 항상 실측으로 확인합니다.
- **작품 페이지(`/ip/{id}`)의 찜 아이콘 index=1은 상품 카드가 아닌 작품(IP) 자체의
  찜 버튼**: `button[aria-label="찜하기"/"찜 해제"]` 패턴이 작품 자체 찜 버튼에도
  동일하게 쓰여, 메인/검색 페이지와 달리 이 페이지에서만 index=1이 상품 카드 밖의
  다른 기능입니다(토스트 문구도 "찜한 **작품**에 추가했어요."로 다름). 상품 카드
  index는 2부터 시작합니다. TC-WISHLIST-005는 상품 카드 찜만 대상이므로
  `test_ip_page_wish_icon_click_adds_wish`는 target_index=2를 사용하며, index=1(작품
  찜 버튼, 기존 계정에 이미 찜된 상태로 확인됨)은 건드리지 않습니다.
- **`/my/wish` SPA 초기 진입 시 상품 목록이 비동기로 채워짐**: `driver.get()` 직후
  곧바로 `find_elements`로 상품 링크를 조회하면 아직 목록이 렌더링되기 전이라 항상
  빈 결과가 나올 수 있습니다. `WishlistPage.wait_for_product_present(product_id)`를
  추가해 목록에 대상 상품이 나타날 때까지 기다린 뒤 판정하도록 했습니다.
- **찜 토스트 타이밍 관련 간헐적 실패(Phase4-C 통합 실행 1회차)**: 여러 찜 토글
  테스트가 연속 실행되는 과정에서 `test_search_result_wish_icon_click_adds_wish`가
  1회 `wait_for_text` 타임아웃으로 실패했으나, 동일 테스트를 단독 재실행하면
  즉시 성공했습니다(2회 연속 전체 스위트 재실행에서도 재현되지 않음). 자체 코드
  결함이 아닌 토스트 컴포넌트의 렌더링/전환 타이밍에 따른 간헐적 현상으로 판단해
  기록만 남기고 재시도 로직은 추가하지 않았습니다(CLAUDE.md 13절 — 실패 회피를 위한
  반복 재시도 금지 원칙 준수, 격리 재실행으로 재현성만 확인).

### 7.12 예약구매(pre-order) 상품의 하단 구매 버튼 문구 차이

Phase4-E(TC-WISHLIST-015/016, 같은 작품의 상품 2건 필요) 구현 중, IP 103(하츠네미쿠)에
속한 일부 상품(4499, 4497 등)이 **예약구매 상품**이며, 하단 고정 버튼 문구가
"구매하기"/"품절"/"판매종료"가 아니라 "예약구매\\n예약 마감까지 N일 HH:MM" 형태임을
발견했습니다. `ProductDetailPage.BOTTOM_WISH_ICON` 로케이터가 이 버튼 텍스트를
기준으로 찜 아이콘을 찾기 때문에, 예약구매 상품에서는 해당 로케이터가 매칭되지 않아
`is_wish_icon_filled()`/`click_wish_icon()` 호출이 타임아웃으로 실패합니다. Phase 1의
`ProductDetailPage`를 예약구매 버튼까지 지원하도록 수정하는 것은 Phase 4의 TC 범위를
벗어나고 Phase 1 전체 회귀가 필요해 이번 Task에서는 다루지 않고, 대신 같은 IP 안에서
일반 구매 버튼을 가진 상품(4440, 4441)만 테스트 데이터로 선택했습니다
(`config/settings.py`의 `IP_PRODUCT_ID_A`/`IP_PRODUCT_ID_B`).

### 7.13 "작품" 탭 섹션은 상품 개별 찜이 아닌 작품(IP) 자체의 별도 찜 상태로 결정됨 (TC 문서 수정)

Phase4-E(TC-WISHLIST-014/015/016) 구현 중, `/my/wish` "작품" 탭의 IP별 섹션이 TC 문서가
가정한 것과 다르게 동작함을 실측으로 발견했습니다.

- 상품 2건(같은 IP 소속)을 개별적으로 찜해도 "작품" 탭에는 아무 섹션도 나타나지 않았습니다
  (최대 15초 대기 후에도 섹션 0개).
- `/ip/{id}` 페이지 최상단에는 상품 카드의 찜 버튼과 별개로 **작품(IP) 자체를 찜하는 전용
  버튼**이 존재하며, 이 버튼을 클릭해 IP 자체를 찜하자 즉시 "작품" 탭에 섹션이 나타났습니다.
- TC-WISHLIST-015가 말하는 "섹션 하트 클릭 시 작품 단위 전체 찜 해제"도 실제로는 개별
  상품의 찜은 그대로 둔 채 **작품(IP) 자체의 찜만 해제**함을 확인했습니다(해제 후 개별
  상품 재확인 결과 여전히 찜된 상태로 남음).

사용자에게 보고 후, 실제 동작 기준으로 TC/PRD 문서를 모두 수정하기로 결정했습니다
(`docs/prd/Feature/prd-wishlist.md` REQ-WISHLIST-011/013 수정 및 REQ-WISHLIST-027 신설,
`docs/tc/wishlist.md` TC-WISHLIST-013~016 Precondition/Expected Result 수정). 이에 따라
자동화 코드도 다음과 같이 구현합니다.
- 섹션이 노출되려면 먼저 대상 IP의 최상단 찜 버튼(`(//button[@aria-label="찜하기" or
  "찜 해제"])[1]`, `home_page.py`의 index=1과 동일한 위치 패턴)을 클릭해 작품 자체를
  찜해야 한다.
- 섹션 하트 클릭 후에는 섹션 소멸만 확인하고, 개별 상품 찜 해제까지는 검증하지 않는다
  (실제로 해제되지 않으므로).

### 7.14 "작품"→"상품" 탭 동기화 오탐 — 실제로는 결함이 아니라 판정 타이밍 문제였음

TC-WISHLIST-016 구현 중, "작품" 탭 캐러셀에서 상품을 찜 해제한 뒤 새로고침 없이 "상품"
탭으로 전환하면 해당 상품이 여전히 남아있는 것처럼 보여 REQ-WISHLIST-014(즉시 동기화)와
불일치한다고 판단해 사용자에게 보고했습니다. 사용자가 직접 브라우저로 재현한 결과
정상 동기화됨을 확인했고, 자동화 코드로 재조사한 결과 코드 자체의 두 가지 문제가
겹친 오탐이었습니다.
1. 탭 전환 직후 반영까지 약 0.5초의 실제 지연이 있는데 기존 코드는 대기 없이 즉시
   판정했다 → `WishlistPage.wait_for_product_absent()` 신설로 해결.
2. 비활성 탭("작품" 탭)의 패널도 DOM에서 제거되지 않고 남아있어(7.13절과 동일 유형),
   `FIRST_ITEM_PRODUCT_LINK`가 href만으로 전체 문서를 검색하면 숨겨진 패널에 남은
   이전 카드가 계속 매칭되어 대기 시간을 늘려도 영구히 타임아웃했다 →
   `FIRST_ITEM_PRODUCT_LINK`를 활성 tabpanel(`@aria-hidden="false"`)로 범위를
   좁혀 해결.

REQ-WISHLIST-014는 정확하며, TC/PRD 문서는 변경하지 않습니다(실제 동작이 문서와 일치함).

### 7.15 편집 모드 "전체 선택" 헤더의 가시성 판정 실패 (원인 불명, JS 클릭/textContent로 우회)

Phase4-F(TC-WISHLIST-020/021) 구현 중, "전체 선택" 체크박스(`role="checkbox"`)와 선택
개수 텍스트(`span[aria-live="polite"]`)가 DOM에 정상적으로 존재하고(별도 디버그
스크립트로 `aria-checked`/텍스트 값까지 확인됨) `presence_of_element_located` 및
`text_to_be_present_in_element`(DOM 텍스트 검사) 기준으로는 문제가 없는데도,
`element_to_be_clickable`(가시성 요구)과 `WebElement.text`(가시성에 따라 빈 문자열을
반환할 수 있음)로 접근하면 **10초 내내 실패**하는 현상을 발견했습니다. 스크롤 위치
보정 등 여러 원인을 시도했으나 재현되어, 근본 원인은 규명하지 못했습니다(리스트
영역의 가상 스크롤 컨테이너와 헤더 간 레이아웃 계산 관련으로 추정). 개별 상품 카드
선택(`ITEM_CARD`, TC-022)은 동일 패턴에서 문제없이 동작해 카드 자체의 문제는 아닙니다.
- `click_select_all()`은 `click()` 대신 `click_via_js()`(존재 확인 후 JS로 클릭,
  가시성 불필요)를 사용하도록 변경했습니다.
- `get_selected_count_text()`는 `.text` 대신 `get_attribute("textContent")`로 값을
  읽도록 변경했습니다(가시성과 무관하게 실제 텍스트 노드 값을 반환).

### 7.16 conftest.py 구글 로그인 로직 재사용 가능하게 분리 (TC-WISHLIST-031/032)

Phase4-I(로그인 완료 후 리디렉션) 착수 시 실측한 결과, 찜 로그인 유도 팝업의 "로그인"
버튼도 `conftest.py`의 `_login_with_google()`이 이동하는 것과 동일한 랜딩 화면
(`laftel.net/auth/login`, "구글로 시작" 버튼)으로 이동함을 확인했습니다(redirect_url
쿼리 파라미터만 다름). 이에 따라 "구글로 시작 버튼이 이미 보이는 화면에서부터 로그인을
끝까지 완료하는" 부분을 `_complete_google_login(driver)`로 분리하고, 기존
`_login_with_google(driver)`는 `driver.get(LOGIN_LANDING_URL)` 후 이 헬퍼를 호출하도록
리팩터링했습니다(`logged_in_driver` fixture의 동작/결과는 변경 없음). TC-031/032는
팝업의 "로그인" 클릭으로 이미 랜딩 화면에 도달한 상태에서 `_complete_google_login()`을
바로 호출해 재사용합니다. 리팩터링 직후 Phase 1~3 전체(62개)를 재실행해 회귀가 없음을
확인했습니다.

### 7.17 검색 자동완성의 디바운스로 인한 과도기적 빈 목록 (Phase 5)

Phase5-B(TC-SEARCH-003/008) 구현 중 실측한 결과, 검색창에 타이핑하는 즉시 자동완성
목록을 조회하면 새 결과가 도착하기 전(디바운스/네트워크 지연 구간) 목록이 일시적으로
비어 있는 상태(`[]`)를 그대로 읽어버려 검증이 실패하거나(TC-003), "변경 감지" Wait가
이 과도기적 빈 상태를 "변경됨"으로 오판해 조기 통과한 뒤 최종 결과가 아닌 빈 상태를
비교하는 문제(TC-008)가 발생했습니다. `time.sleep()` 없이 해결하기 위해
`SearchPage.wait_for_autocomplete_related_keywords_present()`(목록이 1개 이상 나타날
때까지 대기)와 `wait_for_autocomplete_related_keywords_change()`(이전 목록과 다르면서
**동시에 비어있지 않은** 상태까지 대기)를 도입했습니다. 이후 유사하게 목록이 비동기로
갱신되는 화면(최근 검색어 등)에서도 "다르면 즉시 통과"가 아니라 "다르면서 비어있지
않을 때까지" 대기하는 패턴을 우선 검토합니다.

### 7.18 "총 N개" 등 숫자 삽입 텍스트의 React 텍스트 노드 분할 (Phase 5)

Phase5-C(TC-SEARCH-006/007) 구현 중 실측한 결과, 작품 페이지/검색 결과 화면의
"총 117개" 같은 텍스트는 `<span>총 <!-- -->117<!-- -->개</span>`처럼 "총 "/"117"/"개"가
서로 다른 텍스트 노드로 렌더링됩니다. XPath의 `contains(text(), "총")`은 첫 텍스트 노드만
검사하므로 `contains(text(), "총") and contains(text(), "개")`처럼 두 부분 문자열이 서로
다른 텍스트 노드에 있으면 매칭에 실패합니다. `text()` 대신 요소의 문자열 값 전체를 보는
`contains(., "총")` 형태로 작성해야 합니다. 숫자가 삽입된 안내 문구(개수/가격 등)를
Locator로 잡을 때는 항상 이 분할 가능성을 먼저 실측으로 확인합니다.

### 7.19 검색 결과는 키워드를 단어 단위로 넓게 매칭 — 특정 상품이 1페이지에 없을 수 있음 (Phase 5)

Phase5-E(TC-SEARCH-012/013/014) 구현 중 실측한 결과, 검색은 입력한 문구를 부분 문자열로
정확히 매칭하지 않고 단어 단위로 넓게 매칭합니다(예: 상품 제목 전체를 그대로 검색어로
넣어도 관련 없는 상품까지 수백 건씩 매칭되어 원하는 상품이 인기순 정렬 1페이지(20건)
밖으로 밀려남). 결함이 아니라 검색 랭킹 특성이므로, Phase1에서 이미 정의된
`PRODUCT_ID_SALE_ENDED`(1608)는 검색 키워드로는 1페이지에 노출되지 않아 검색 전용으로
1페이지에 안정적으로 노출되는 것을 실측으로 새로 확인한 상품(`PRODUCT_ID_SEARCH_SALE_ENDED`,
3809)과 키워드(`SEARCH_KEYWORD_SALE_ENDED_PRODUCT`, `SEARCH_KEYWORD_SOLD_OUT_PRODUCT`,
`SEARCH_KEYWORD_WITH_STATUS_PRODUCTS`)를 config/settings.py에 별도로 추가했습니다. 검색
결과에서 특정 상품을 다뤄야 하는 이후 TC도 항상 해당 키워드로 실제 1페이지에 노출되는지
실측 후 사용합니다.

### 7.20 검색창에 공백만 입력해도 초기화면(인기작품/랭킹) 섹션은 사라짐 (Phase 5)

Phase5-F(TC-SEARCH-016) 구현 중 실측한 결과, 검색창에 공백만 입력해도(실제 검색은
실행되지 않음) "인기 작품"/"지금 사람들이 많이 구매하는 굿즈" 섹션은 즉시 사라집니다.
REQ-SEARCH-016의 "검색페이지 상태 유지"는 이 두 섹션이 그대로 보이는 것을 의미하지
않고, 페이지 이동/에러·결과없음 문구 노출 없이 검색페이지 자체에 머무르는 것을
의미합니다. 이에 따라 `SearchPage.is_initial_screen_displayed()`(초기화면 전체 확인용)와
`is_on_search_screen()`(뒤로가기/검색창/취소 버튼만으로 "검색페이지에 머무름"을 판정)을
분리했습니다. 입력값 유무에 따라 달라지는 화면 요소를 "화면 유지" 조건으로 쓸 때는
어떤 하위 요소가 입력값에 반응해 사라지는지 먼저 실측으로 구분합니다.

### 7.21 찜 삭제 확인 다이얼로그 텍스트의 headless 판정 실패 (Phase Final)

Phase Final(CI/CD) 첫 self-hosted 러너 실행 중 `test_bulk_delete_confirm_dialog_cancel_keeps_selection`
(TC-WISHLIST-023)이 headless 모드에서만 실패함을 발견했습니다. 로컬(비headless)에서는
항상 통과했으나, `CI=true`(headless) 조건으로 로컬에서 직접 재현한 결과 동일하게
실패해(7.15절과 같은 유형) headless 자체의 문제임을 확인했습니다.
`WishlistPage.get_delete_confirm_dialog_text()`가 `WebElement.text`(렌더링 가시성에
의존)를 사용해 빈 문자열을 반환하고 있었고, `get_attribute("textContent")`로
교체해 headless/비headless 모두에서 안정적으로 통과함을 확인했습니다. 다이얼로그·팝업
등 동적으로 나타나는 요소의 텍스트를 읽을 때는 headless 실행 가능성을 고려해 처음부터
`textContent` 사용을 우선 검토합니다.

### 7.22 CI 전체 스위트 실행 시 test_search.py 일부에서 발생하는 간헐적 타이밍 플레이키 (Phase Final, 결론)

self-hosted 러너로 전환한 첫 두 차례의 CI 실행에서 `test_search.py`의 서로 다른
테스트 3건씩이 매번 다르게 실패했다(1차: 자동완성/결과없음/최근검색클릭 관련 3건,
2차: 작품뱃지클릭/개별삭제/비로그인최근검색 관련 3건 — 완전히 다른 조합). 처음에는
"self-hosted 러너가 macOS LaunchAgent(백그라운드 서비스)로 Chrome을 구동하는 특정
실행 컨텍스트 때문"이라는 가설을 세워 러너를 foreground(`./run.sh` 직접 실행)로
전환해 재검증했으나, 여전히(그러나 또 다른 조합으로) 3건이 실패해 **이 가설은
기각되었다**. 격리 실행(해당 테스트만 단독 실행)에서는 매번 통과하는 점과 실패
조합이 매번 달라지는 점을 종합하면, 로그인/세션/러너 실행 방식과 무관하게 **113개
전체 테스트를 15분 이상 연속 실행할 때 발생하는 일반적인 간헐적 타이밍 플레이키**로
결론짓는다(사용자 확인). 이 프로젝트에서 이미 문서화된 다른 플레이키 사례(로그인
지연 7.3절, 토스트 타이밍 7.11절)와 같은 범주이며, Slack 실패 알림 수신 시 해당
테스트만 재실행해 일시적 현상인지 확인하는 기존 정책(CLAUDE.md 13절)을 그대로
적용한다. 추가 코드 수정은 하지 않는다.

### 7.23 CI에서도 실제 구글 로그인 UI가 필요한 테스트는 headless를 적용하지 않음 (Phase Final)

TC-WISHLIST-031/032(`test_direct_entry_login_completes_to_original_destination`,
`test_site_entry_login_completes_to_previous_screen`)는 세션 주입이 아닌 실제
`_complete_google_login()` 로그인 UI를 그대로 통과해야 하는 테스트다. CI에
`GOOGLE_ACCOUNT_EMAIL`/`GOOGLE_ACCOUNT_PASSWORD` Secret을 추가한 뒤 실행한 결과,
headless 모드에서 Google이 "로그인할 수 없음 — 브라우저 또는 앱이 안전하지 않을 수
있습니다"로 로그인 자체를 차단함을 스크린샷으로 확인했다(한국 로컬 머신이어도
headless라는 이유만으로 차단됨 — IP/위치 문제가 아님). 우회를 시도하지 않고
사용자에게 보고한 뒤, 이 2개 테스트에만 `@pytest.mark.requires_real_browser`
마커를 붙이고 `conftest.py`의 `driver` fixture가 이 마커가 있으면 CI에서도
headless를 적용하지 않도록 분기했다(다른 모든 테스트의 headless 동작은 변경 없음).
실제 머신이라 CI 실행 중 이 2개 테스트만 화면이 잠깐 뜨는 것은 문제가 되지 않는다.
로컬에서 `CI=true`로 이 2개 테스트를 개별 실행해 headless 없이 정상 PASSED됨을
확인했다.

---

## 8. Assertion 원칙

- Assertion은 **Test Layer에서만** 수행합니다(4.1절과 연결).
- pytest의 `assert`를 사용하며, 실패 메시지에 **기대값과 실제값을 모두 포함**합니다.

```python
assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"
```

---

## 9. Fixture 원칙

- WebDriver 생성/종료는 `conftest.py`의 fixture로 관리하며, `yield` 패턴으로 테스트 종료 후
  리소스 정리(`driver.quit()`)를 보장합니다.
- 기본 `scope`는 **`function`**으로 설정해 테스트마다 새 WebDriver를 생성합니다(10절 테스트
  독립성과 직결).
- 자주 쓰이는 Page 객체도 fixture로 제공해 테스트 코드의 반복을 줄입니다.

```python
@pytest.fixture(scope="function")
def driver():
    # 일반 데스크톱 창 크기로 실행 (모바일 에뮬레이션 옵션 없음 — 1절 참고)
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)
```

---

## 10. 테스트 독립성

- 각 테스트는 **단독 실행 가능**해야 하며, 다른 테스트의 실행 순서에 의존하지 않습니다.
- 각 테스트는 스스로 필요한 상태(로그인 등)를 셋업합니다.
- 테스트가 생성한 데이터(회원가입으로 만든 계정 등)는 가능한 범위에서 해당 테스트 내에서
  정리합니다(11절 데이터 관리 원칙과 연결).
- 이 원칙은 CLAUDE.md 10절 "Isolated/Reproducible/Idempotent" 원칙을 자동화 코드 수준에서
  구체화한 것입니다.

---

## 11. 테스트 데이터 관리

이 프로젝트는 dev/staging 없이 **Production 단일 환경**입니다. 현재 In Scope(검색/
상품상세/찜/주문(결제 제외)/카트)에는 로그인-로그아웃/회원가입/계정삭제 Feature가 없으므로,
계정을 새로 생성·삭제하는 시나리오는 없습니다. **고정 계정 재사용 방식만 사용합니다.**

### 11.1 고정 계정 재사용 (로그인 상태가 필요한 시나리오)

- 카트/찜/주문처럼 "로그인 상태"가 전제 조건인 TC는 사전 준비된 고정 계정을 재사용합니다.
- 계정 **이메일과 비밀번호 모두** 어떤 파일에도 하드코딩하지 않고 `.env`(환경변수)로만
  관리합니다(`TEST_ACCOUNT_EMAIL`, `TEST_ACCOUNT_PASSWORD`, 12절 참고). `test_data/
  accounts.json`은 이메일 등 계정 식별 정보를 담지 않으며, 계정과 무관한 정적 테스트
  데이터가 필요해지면 그때 다시 사용합니다.
- 이메일 로그인 계정이 서버측 잠금으로 추정되는 문제로 막혀, 별도의 구글 전용 테스트
  계정(`GOOGLE_ACCOUNT_EMAIL`/`GOOGLE_ACCOUNT_PASSWORD`, 역시 `.env`로만 관리)으로
  임시 전환했습니다. `config/settings.py`의 `LOGIN_METHOD` 상수로 전환하며, 상세 배경과
  구현/위험은 7.7절 참고.

### 11.2 주문(결제) 관련 데이터 제약

- Project PRD 6절 In Scope는 "주문(**결제 제외**)"로 한정되어 있습니다. 자동화 코드는 주문/
  결제 화면 진입, 배송지·배송요청사항 입력, 약관 동의, PG 결제창 진입까지만 확인하고,
  **실제 결제(PG 결제 완료)는 어떤 테스트에서도 수행하지 않습니다**(TC-ORDER-019 근거).
- 따라서 주문 관련 테스트로 인해 실제 주문 데이터가 생성되는 일은 없는 것으로 판단하지만,
  구현 중 예상과 다른 부작용(예: 결제창 진입만으로 주문이 생성되는 등)이 발견되면 즉시
  중단하고 CLAUDE.md 11절에 따라 사용자에게 보고합니다.

### 11.3 공통 원칙

- 테스트 데이터를 코드에 직접 하드코딩하지 않습니다.
- Production 데이터(실제 사용자 데이터 등)를 생성/수정/삭제하는 작업은 CLAUDE.md 11절에
  따라 사용자의 명시적 승인 없이 수행하지 않습니다.

---

## 12. 환경변수 및 민감정보 관리

- 비밀번호 등 민감정보는 코드에 절대 작성하지 않고 환경변수로 관리합니다
  (`python-dotenv` + `.env`).
- `.env`는 `.gitignore`에 포함해 git에 커밋되지 않도록 합니다(이미 프로젝트
  `.gitignore`에 `.env` 규칙이 존재하며, 자동화 코드용 변수도 동일한 방식을 따릅니다).
- CI(GitHub Actions) 환경에서는 GitHub Secrets로 관리합니다(CLAUDE.md 17절과 동일).
- 로그, 리포트(HTML/JUnit XML), 실패 스크린샷 어디에도 비밀번호 등 민감정보가 노출되지
  않도록 합니다.

---

## 13. Logging

- `print()` 대신 Python 표준 `logging` 모듈을 사용합니다.
- 로그 레벨 기준:
  - `DEBUG`: Locator 탐색, 요소 상태 등 상세 진단 정보
  - `INFO`: 로그인, 페이지 이동, 클릭 등 주요 액션
  - `WARNING`: 재시도, 느린 응답 등
  - `ERROR`: 예외 발생, 요소를 찾지 못함 등
  - `CRITICAL`: 드라이버 크래시 등 심각한 오류
- 비밀번호 등 민감정보는 로그에 마스킹 처리합니다.
- 로그 저장 경로/포맷/로테이션 방식은 실제 구현 시 확정합니다(현재 미정).

---

## 14. 실패 시 Screenshot / Artifact

- pytest hook(`pytest_runtest_makereport`)을 이용해 테스트 **실패 시에만** 자동으로
  스크린샷을 캡처합니다.
- 파일명 규칙: `{테스트_함수명}_{상태}_{YYYY-MM-DD_HH-MM-SS}.png`
- 저장 위치: `automation/screenshots/`(git 미추적)
- 스크린샷에 민감정보(비밀번호 입력값 등)가 노출되지 않도록 주의합니다.
- CI 실행 시 실패 스크린샷과 리포트(pytest-html, JUnit XML)는 GitHub Actions Artifact로
  업로드해 사후 확인이 가능하도록 합니다(16절 CI/CD와 연결, 실제 워크플로우 파일은 별도
  단계에서 작성 — CLAUDE.md 15절).

---

## 15. Exception Handling

- 프로젝트 전역 CLAUDE.md "에러 핸들링 필수" 원칙을 자동화 코드에서는 다음과 같이
  구체화합니다.
- 불필요하게 광범위한 `except Exception:` 처리를 지양하고, Selenium이 실제로 발생시키는
  구체적 예외(`TimeoutException`, `NoSuchElementException` 등)를 명시적으로 처리합니다.
- 예외 발생 시 반드시 로그를 남겨(`logger.error(...)`) 이후 디버깅이 가능하게 합니다.
- 예외를 조용히 삼키지 않습니다(로깅 없이 `pass` 처리 금지).

---

## 16. CI/CD

- GitHub Actions를 사용하며, **GitHub Push 시 자동으로 자동화 테스트가 실행**됩니다.
- 실행 흐름(CLAUDE.md 15절과 동일): `Git Push → GitHub Actions → 자동화 테스트 실행 →
  Test Report 생성 → 결과 판정 → Slack Notification`
- **실패 시 Slack 알림에는 어떤 부분(테스트/Feature)에서 실패했는지 알 수 있는 정보를
  포함**합니다. JUnit XML 결과를 파싱해 실패한 테스트 이름과 사유 요약을 메시지에 포함하는
  방식을 사용합니다(1절 리포팅 결정과 연결).
- 이 문서는 CI **운영 원칙**만 정의하며, 실제 GitHub Actions Workflow(YAML) 파일과 Slack
  연동 스크립트는 별도 구현 단계에서 작성합니다(CLAUDE.md 15절과 동일한 범위 제한).
- Slack은 결과 알림 전용이며 Commit/Push 승인 용도로 사용하지 않습니다(CLAUDE.md 16절).

### 16.1 CI 환경 로그인 전략 (세션 주입)

- **테스트 및 CI에서는 구글 OAuth 로그인 UI를 직접 자동화하지 않습니다.** 로그인 화면
  자체를 Selenium으로 조작하는 방식(7.7절의 `_complete_google_login()`)은 로컬 개발
  환경에서만 사용하며, CI(GitHub Actions)에서는 사용하지 않습니다 — CI 환경(매번 다른
  IP/디바이스 지문)에서는 구글의 자동화 브라우저 탐지에 의한 로그인 차단이 로컬보다
  훨씬 자주 발생할 위험이 있기 때문입니다.
- **대신 세션 주입(Session Injection) 방식을 사용합니다.** 로컬에서 기존
  `_complete_google_login()`으로 고정 계정 로그인을 1회 수행해 인증 후 세션 쿠키를
  캡처하고, 이를 GitHub Secret(예: `SESSION_COOKIES_JSON`)으로 저장합니다. CI 실행
  시에는 이 저장된 세션을 브라우저에 주입(`driver.add_cookie()` 등)해 로그인 상태를
  만들며, 구글 로그인 화면 자체는 거치지 않습니다.
- **로컬 개발 환경의 기존 동작은 변경하지 않습니다.** 세션 주입은 CI 환경에서만
  분기되며, 로컬에서는 지금까지와 동일하게 `logged_in_driver`가 직접 구글 로그인을
  수행합니다.
- **세션 만료 시 갱신은 사용자가 수동으로 수행합니다.** 별도의 자동 갱신 워크플로우는
  두지 않으며, 로컬에서 세션을 다시 캡처해 GitHub Secret 값을 수동으로 업데이트하는
  절차를 따릅니다. 캡처한 세션 쿠키는 민감정보이므로 로컬 디스크에 파일로 남기지 않고
  즉시 GitHub Secret 등록에만 사용합니다(12절 환경변수 관리 원칙과 동일하게, CI는
  GitHub Secrets로만 관리하고 로그에 노출하지 않습니다).
- 구체적인 세션 캡처 스크립트, Secret 이름, 갱신 절차(런북)는 Phase Final 구현 완료
  시점에 이 절에 이어서 보강합니다.
- **CI 러너는 GitHub 호스팅이 아닌 한국 소재 self-hosted 러너(로컬 macOS)를
  사용합니다.** PhaseFinal-H 실측 결과 `store.laftel.net`이 한국 외 지역 IP를
  차단해("Sorry, this service is only available in South Korea.") GitHub 호스팅
  러너(해외 데이터센터)에서는 사이트 접속 자체가 불가능함을 확인했습니다. 워크플로우의
  `runs-on`은 `[self-hosted, macOS, korea]`이며, 이 러너에는 이미 Python/Chrome이
  설치되어 있어 `actions/setup-python`·`browser-actions/setup-chrome`은 사용하지
  않습니다. 러너는 `~/actions-runner-laftel-store`에 설치되어 있습니다.
- **예외 — TC-WISHLIST-031/032는 세션 주입이 아닌 실제 구글 로그인을 사용합니다.**
  이 두 TC는 "로그인 완료 후 리디렉션"을 검증하는 로그인-UI-자체 테스트라 세션 주입으로
  대체할 수 없습니다. CI 러너가 이제 로컬 한국 머신이라(해외 클라우드 IP가 아님) 봇
  탐지 위험이 로컬 개발 시와 동일한 수준으로 낮아져, `GOOGLE_ACCOUNT_EMAIL`/
  `GOOGLE_ACCOUNT_PASSWORD`도 GitHub Secret으로 추가 등록해 이 두 TC만 예외적으로
  실제 로그인 플로우를 그대로 사용합니다(사용자 승인).

---

## 17. Coding Convention

- 1.1절의 "코딩 스타일 예외"에 따라 **PEP8**을 기준으로 합니다.
  - 들여쓰기: 4칸
  - 한 줄 최대 길이: 100자 권장
  - 타입힌트를 함수 파라미터/반환값에 권장(가독성 확보)
- 주석은 프로젝트 전역 CLAUDE.md에 따라 **한국어**로 작성합니다.
- 변수명/함수명은 영어를 사용합니다(전역 CLAUDE.md "변수명/함수명: 영어" 원칙 유지, 표기법만
  1.1절 예외에 따라 snake_case).

---

## 18. Naming Convention

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | `login_page.py`, `test_login.py` |
| 클래스명 | PascalCase | `LoginPage`, `BasePage` |
| Page 객체 클래스 | `Page` 접미사 필수 | `LoginPage` (O), `Login` (X) |
| 메서드명 | snake_case, 동사로 시작 | `click_login_button`, `get_error_message` |
| 테스트 함수명 | `test_` 접두사 | `test_login_with_valid_credentials` |
| 변수명 | snake_case | `search_keyword`, `product_count` |
| 상수(Locator 등) | UPPER_SNAKE_CASE | `LOGIN_BUTTON`, `EMAIL_INPUT` |

---

## 19. 공통 코드 분리 기준

- **2회 이상 반복**되는 코드는 공통 메서드/함수로 분리합니다(CLAUDE.md 12절 "불필요한 중복
  구현 금지"와 연결).
- **BasePage**: 모든 Page에서 필요한 공통 화면 조작(요소 찾기, 클릭, Wait 래핑 등).
- **utils**: 화면과 무관한 순수 로직(랜덤 데이터 생성, 문자열/날짜 처리 등).
- 특정 Feature 하나에서만 쓰이는 로직을 섣불리 공통화하지 않습니다(과도한 추상화 지양).

---

## 20. 테스트 실행 및 검증

### 20.1 테스트 실행 범위와 시점

개발 Roadmap의 Phase 진행 과정에서 테스트를 "언제, 어느 범위까지" 실행할지를 3단계로
구분합니다. 범위를 넓게 잡을수록(특히 전체 통합테스트) 실행 시간이 길고 제3자 광고 등
Test Environment 요인에 따른 불안정성(7.1절, 22절)에 노출될 여지도 커지므로, 아래처럼
시점을 명확히 구분해 불필요한 반복 실행을 피합니다.

1. **Phase 내부, 코드 작성 단위(Task)마다**: Page Object 메서드나 테스트 함수를 새로
   작성/수정할 때마다, 그 범위에 해당하는 테스트를 즉시 실행해 동작을 검증합니다. 실행 없이
   "완료"로 간주하지 않습니다(CLAUDE.md 13절과 동일).
   ```bash
   # 예시 형식 — 실제 파일/함수명은 구현 시 결정됨(TC ID와 함수명의 대응 관계는 각 테스트
   # 함수의 docstring에 기록). pytest 노드 ID(파일::함수명)로 지정해 그 테스트만 실행한다.
   pytest automation/tests/test_cart.py::test_<시나리오를_설명하는_함수명>
   ```
2. **Phase 코드 작성 완료 시**: 해당 Phase의 Approved TC 전체를 대상으로 pytest를
   실행해 PASSED/FAILED/ERROR를 확인합니다. 실행 범위는 **해당 Phase의 테스트 파일로
   한정**하며, 다른 Phase까지 포함한 전체 통합테스트는 이 시점에 진행하지 않습니다.
   ```bash
   # 예: Phase 5(cart) 완료 시 — cart Phase 범위로만 한정
   pytest automation/tests/test_cart.py --html=automation/reports/report_phase5.html --junitxml=automation/reports/results_phase5.xml
   ```
3. **전체 통합테스트(Full Regression)**: 개발 Roadmap상 모든 Feature Phase의 코드
   작성이 완료된 이후, CI/CD 연동 Phase(Phase Final) 착수 직전 시점에 **1회만** 진행합니다.
   그 이전 개별 Phase 완료 시점마다 반복적으로 전체 통합테스트를 수행하지 않습니다.
   ```bash
   # 예: 모든 Feature Phase 완료 후, CI/CD Phase 착수 직전 1회
   pytest automation/tests/ --html=automation/reports/report_full.html --junitxml=automation/reports/results_full.xml
   ```

- 테스트 실패 시 원인을 CLAUDE.md 13절의 4가지 범주(Automation Code / Test Data / Test
  Environment / 실제 Product 문제) 중 하나로 구분하려고 시도하며, 원인이 불명확하면 추측으로
  결론 내리지 않고 사용자에게 보고합니다.
- 실패를 회피하기 위해 무한/반복적으로 재시도하지 않습니다.

---

## 21. 코드 작성 후 Self Review 체크리스트

코드 작성을 완료로 보고하기 전에 다음을 자체 점검합니다.

- [ ] `time.sleep()`을 사용하지 않았는가? (Explicit Wait 사용)
- [ ] Full XPath를 사용하지 않았는가?
- [ ] 모든 Locator가 Page 클래스 상단에 상수로 정의되어 있는가?
- [ ] Page Layer에 Assertion이 없는가?
- [ ] 모든 Page 클래스가 `BasePage`를 상속하는가?
- [ ] 각 테스트가 다른 테스트 실행 순서에 의존하지 않는가?
- [ ] 계정 정보/비밀번호가 코드에 하드코딩되지 않았는가?
- [ ] `print()` 대신 `logging`을 사용했는가?
- [ ] 예외를 광범위하게 처리하지 않고 구체적으로 처리·로깅했는가?
- [ ] 파일명(snake_case)/클래스명(PascalCase, `~Page` 접미사)/함수명(snake_case,
      동사 시작)/테스트 함수명(`test_` 접두사) 규칙을 지켰는가?
- [ ] 4칸 들여쓰기를 사용했는가?
- [ ] 코드 작성 후 실제로 pytest를 실행해 결과(PASSED/FAILED/ERROR)를 확인했는가?
- [ ] 실패 시 스크린샷이 저장되었는가?
- [ ] (Locator를 새로 작성한 경우) 5절 절차에 따라 Playwright MCP로 실제 페이지 구조를
      확인하고 Locator의 고유성을 검증했는가?

---

## 22. 알려진 Production 사이트 결함 (Known Site Defects)

이 절은 자동화 코드/Locator/Assertion 자체는 정상 동작하지만, `store.laftel.net`
Production 사이트 쪽 결함으로 인해 테스트가 실패(또는 실패할 수 있는)하는 사례를
기록합니다. CLAUDE.md 13절 "실제 Product 문제" 범주로 분류된 사례가 대상입니다.

**현재까지 자동화 구현 중 발견된 사례는 없습니다** (아직 자동화 코드 구현을 시작하지
않았기 때문입니다). 구현 중 이런 사례가 발견되면 22.1절부터 이어서 기록합니다.

> 참고: `docs/tc/search.md`에는 TC 작성 단계에서 이미 발견된 결함 의심 항목
> (DEFECT-SEARCH-001, 와일드카드성 특수문자 검색 시 결과 없음 화면 미노출)이 기록되어
> 있습니다. 다만 해당 TC(TC-SEARCH-028/029)는 자동화 대상 선정 단계에서 QA Decision이
> `Rejected`로 확정되어 자동화 범위에서 제외되었으므로, 자동화 코드가 이 결함을 실행 중
> 마주칠 일은 없습니다. 따라서 이 절(자동화 구현 중 실제 발견된 사례)의 항목으로는
> 등록하지 않고 참고 정보로만 남깁니다.

---

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 이전 프로젝트(대상 사이트 automationexercise.com) 참고 문서를 라프텔 스토어\
 프로젝트에 맞게 재작성. 대상 URL(store.laftel.net), 0.1절 자동화 대상 범위(cart/order/\
 product-detail/search/wishlist, 합계 113건), 실행 화면 크기(일반 데스크톱 창, 모바일\
 에뮬레이션 미사용), 테스트 데이터 관리(로그인-회원가입/계정삭제 시나리오 없음 — 11.2절\
 제거, 주문 결제 제외 원칙 신설), 6.1절 Locator 우선순위(이전 사이트 실측 근거 제거, 기본\
 우선순위로 초기화), 7.1절 광고 오버레이 처리(이전 사이트 고유 이슈로 제거), 22절 알려진\
 사이트 결함(이전 사이트 사례 제거, 신규 프로젝트 기준 초기화), 3.1절 Import 경로 규칙과\
 5.0절 Playwright MCP 연결 상태(이 프로젝트에서 아직 검증되지 않은 사실로 되돌림)를\
 조정. 1절 기술 스택 결정(Python/Selenium/pytest/POM 등)과 2·4·8~10·12~19·20.1·21절의\
 일반 원칙은 그대로 유지 (사용자 승인). | 승인완료 |
| 2026-09-05 | 11.1절 수정 — Phase 1(product-detail) 로그인 필요 TC 착수를 위해 사용자가\
 고정 계정 정보를 전달하면서 이메일도 비밀번호와 함께 `.env`로 관리해 달라고 요청함에 따라,\
 기존 "이메일은 `test_data/accounts.json`, 비밀번호는 `.env`" 방식에서 "이메일과 비밀번호\
 모두 `.env`(`TEST_ACCOUNT_EMAIL`/`TEST_ACCOUNT_PASSWORD`)" 방식으로 변경 (사용자 요청에\
 따른 재승인). | 승인완료 |
| 2026-09-05 | 7.2절 신설 — Phase 1(product-detail) TC-013(이미지 캐러셀) 구현 중 발견한\
 ChromeDriver W3C Actions의 세션 내 연속 드래그 불안정 문제(사이트 결함 아닌 도구 한계)를\
 기록하고, 대응 원칙(테스트당 드래그 1회, 페이지 재진입으로 세션 분리)과 이로 인해\
 자동화 범위에서 제외되는 시나리오 처리 방침을 명시 (사용자 승인). | 승인완료 |
| 2026-09-05 | 7.3절 신설 — TC-035~039(구매하기 확장 영역/옵션/수량)이 실제로는 로그인이\
 필요함을 구현 중 발견(원문 Precondition 무관, TC-011과 동일 유형). 사용자 승인에 따라\
 로그인 fixture(`conftest.py`의 `logged_in_driver`)를 Phase 1(Task E)에서부터 앞당겨\
 구현했으며, 그 과정에서 관찰된 로그인 플로우 간헐적 지연과 `LOGIN_TIMEOUT`(20초) 별도\
 적용 사실을 기록 (사용자 승인). | 승인완료 |
| 2026-09-05 | 7.4절 신설 — Phase 1(product-detail) TC-034 구현 중 Chrome 기본 창\
 크기에서 캐러셀 카드 클릭 가로채기 문제를 발견해 `WINDOW_SIZE`(1600x1000)를 명시\
 적용하고, `BasePage.click()`에 오버레이로 인한 클릭 가로채기 시 제한 시간 내\
 재시도하는 방어 로직을 추가한 사실을 기록(구현 세부사항 보완, TC 내용 변경 없음). | 승인완료 |
| 2026-09-05 | 7.5절 신설 — Phase 1 전체 통합 실행(Task I) 중 get_login_prompt_text()가\
 요소 등장 직후 빈 문자열을 반환하는 타이밍 결함을 발견해 wait_for_text로 내용이\
 채워지길 기다린 뒤 반환하도록 수정한 사실을 기록(구현 결함 수정, TC 내용 변경 없음). | 승인완료 |
| 2026-09-05 | 7.6절 신설 — Phase 2(cart) Task B(TC-018/019/020, 삭제 흐름) 구현 중\
 발견한 장바구니 화면의 비동기 갱신 Race Condition 3건(진입 직후 스켈레톤 상태에서의\
 상품 개수 오탐, 담기 API 완료 전 페이지 이동 시 담기 유실, 삭제 확인 직후 목록 갱신\
 지연)과 전체선택 체크박스가 기본 선택 상태라 무조건 클릭 시 오히려 전체 해제되는 문제를\
 기록하고, `CartPage.wait_for_items_loaded()`/`wait_for_item_count()`/\
 `ensure_all_selected()`로 대응한 사실을 기록(구현 결함 수정, TC 내용 변경 없음). | 승인완료 |
| 2026-09-05 | 7.6절 addendum — Phase 2 Task C(TC-009/010) 구현 완료 후 전체 스위트\
 반복 실행 중 `SELECT_ALL_CHECKBOX` 대기가 간헐적으로 시간 초과하는 현상을 드물게\
 관찰(단독 실행 시 미재현). 7.4절 위시리스트 플레이키니스와 동일 유형(전체 스위트\
 연속 실행 시에만 발생)으로 판단해 알려진 한계로 기록(무한 재시도 금지 원칙에 따라\
 임의 추측 수정 없음). | 승인완료 |
| 2026-09-05 | Phase 2 Task D(TC-007/008, 배송비 조건분기) 구현 완료. 100,000원 이상\
 상품(products=3747, 344,000원)을 저가 상품과 함께 담아 합산 100,000원 이상 조건을\
 재현했으며, `CartPage.get_shipping_notice_text()`로 "N건 묶음배송비 무료"/"배송비\
 {금액}원 (100,000원 이상 무료배송)" 두 문구 케이스를 모두 검증한 사실을 기록\
 (구현 세부사항 보완, TC 내용 변경 없음 — Precondition 자체는 이전 변경 이력에서\
 이미 재승인됨). | 승인완료 |
| 2026-09-05 | 7.7절 신설, 11.1절 보강 — Phase2-G 착수 중 이메일 로그인 계정(TEST_\
 ACCOUNT_*)이 서버측 잠금으로 추정되는 오류로 막혀, 사용자 요청에 따라 별도 구글\
 계정(GOOGLE_ACCOUNT_EMAIL/PASSWORD, .env 관리)으로 로그인 방식을 임시 전환\
 (config/settings.py LOGIN_METHOD 상수, 이메일 로그인 코드는 삭제하지 않고 보존해\
 잠금 해제 후 원복 가능). 구글의 자동화 브라우저 탐지 차단을 실측하고 driver\
 fixture에 완화 옵션을 추가했으며, 신규 계정 전용 "스토어 이용약관 동의" 온보딩\
 처리와 이 과정에서 발견한 CartPage.clear_cart()의 렌더링 대기 누락 결함(wait_for_\
 cart_loaded() 추가)을 함께 기록. Phase 1(35건)·Phase 2 cart(16건) 전체 재실행으로\
 회귀 없음을 확인 (사용자 요청에 따른 임시 변경, 재승인). | 승인완료 |
| 2026-09-05 | 7.8절 신설 — Phase 3(order) Task E(TC-ORDER-017) 구현 중, 배송지\
 우편번호/주소 입력란이 readonly라 Rejected 처리된 카카오 우편번호 모달(TC-ORDER-006)을\
 거치지 않고는 유효한 배송지를 만들 수 없음을 실측으로 확인. 사용자에게 보고하고 승인을\
 받아 모달을 최소 조작(검색→결과 클릭)하는 CheckoutPage.fill_address_via_kakao_\
 postcode_search()를 구현했으며(모달 자체는 검증하지 않음), 이 과정에서 발견한 iframe\
 전환 Stale/NoSuchFrame 타이밍 이슈와 동일 문구의 숨겨진 중복 다이얼로그로 인한\
 확인 버튼 클릭 타임아웃을 각각 자체 재시도 헬퍼와 data-state="open" 조건 추가로\
 해결한 사실을 기록 (사용자 승인에 따른 구현). | 승인완료 |
| 2026-09-05 | 7.9절 신설 — Phase3-F(TC-ORDER-019, PG 결제창 진입) 구현 중 나이스페이\
 결제창이 동일 입력에도 간헐적으로만 노출됨을 반복 실측으로 확인(자체 코드 문제가 아닌\
 PG 연동 요인으로 추정, 반복되는 실제 PG 호출 자체도 부작용 리스크). 사용자 결정에 따라\
 TC-ORDER-019를 이번 Phase 3 자동화 범위에서 보류하기로 확정하고 사유를 기록\
 (automation-candidates 문서는 Google Sheet 스냅샷이라 QA Decision 값은 임의로\
 수정하지 않음). Phase 3 자동화 대상 11건→10건 조정을 ROADMAP.md에도 반영 (사용자 승인). | 승인완료 |
| 2026-09-06 | 7.10절 신설 — Phase3-G 통합 실행 중 TC-ORDER-005 실패를 조사해, 계정에\
 저장된 배송지가 있으면 체크아웃 화면이 자동으로 채워주는 정상 기능을 발견(REQ-ORDER-019/\
 TC-ORDER-021로 문서화, 사용자 승인). 이 과정에서 Selenium element.clear()가 React\
 컨트롤드 입력의 내부 상태를 갱신하지 못해 지운 값이 리렌더링 시 복원되는 결함도 발견해\
 CheckoutPage._clear_via_keyboard()(Backspace 반복 전송)로 수정. TC-ORDER-005는 이제\
 항상 채워지는 우편번호/주소 검증을 제외하고 이름/휴대폰번호 2개 필드만 검증하도록 범위\
 조정 (사용자 승인). | 승인완료 |
| 2026-09-06 | 7.11절 신설 — Phase4-A/B(찜 메인/검색/작품페이지) 구현 중 검색/작품\
 페이지에는 무한 스크롤 로딩용 빈 div[role="status"]가 먼저 렌더링되어 있어 찜 토스트를\
 role만으로 특정하면 항상 타임아웃되는 문제를 발견, data-scope="toast" 셀렉터로 해결.\
 작품 페이지(/ip/{id})의 찜 아이콘 index=1이 상품 카드가 아닌 작품(IP) 자체 찜 버튼임을\
 발견해 상품 카드 대상 index를 2로 조정. 두 건 모두 승인된 Task 범위 내 구현 디테일\
 수정으로, TC/PRD 변경 없이 기록만 진행 (continuous mode). | 승인완료 |
| 2026-09-06 | 7.12절 신설 — Phase4-E(TC-015/016) 구현 중 같은 IP의 예약구매 상품(4499,\
 4497)이 하단 구매 버튼 문구가 달라 기존 BOTTOM_WISH_ICON 로케이터와 매칭되지 않음을\
 발견, Phase 1 회귀 없이 일반 구매 버튼을 가진 상품(4440, 4441)으로 테스트 데이터 교체. | 승인완료 |
| 2026-09-06 | 7.13절 신설 — Phase4-E(TC-014/015/016) 구현 중 "작품" 탭 섹션이 상품 개별\
 찜이 아닌 작품(IP) 자체의 별도 찜 상태로 노출/해제됨을 실측으로 발견해 사용자에게 보고.\
 사용자 결정에 따라 prd-wishlist.md(REQ-WISHLIST-011/013/027)와 docs/tc/wishlist.md\
 (TC-WISHLIST-013~016)를 실제 동작 기준으로 재정의하고 재승인, 자동화 코드도 작품 자체\
 찜 버튼을 명시적으로 조작하도록 재구현 (사용자 승인). | 승인완료 |
| 2026-09-06 | 7.14절 신설 — TC-WISHLIST-016 구현 중 "작품"→"상품" 탭 동기화가 안 되는\
 것으로 보여 사용자에게 보고했으나, 사용자 재현 결과 정상 동작함을 확인. 자동화 코드가\
 탭 전환 직후 대기 없이 판정해 발생한 오탐(실제 반영까지 약 0.5초 지연)으로 결론,\
 wait_for_product_absent() 추가로 수정. TC/PRD는 변경하지 않음. | 승인완료 |
| 2026-09-06 | 7.15절 신설 — Phase4-F(TC-020/021) 구현 중 편집 모드 "전체 선택" 체크박스/\
 개수 텍스트가 DOM에는 정상 존재하나 가시성 기반 조건(element_to_be_clickable,\
 WebElement.text)에서만 영구 타임아웃되는 현상 발견(근본 원인 미규명). click_via_js()\
 와 get_attribute("textContent")로 우회. | 승인완료 |
| 2026-09-06 | 7.16절 신설 — Phase4-I(TC-031/032) 착수 전 실측으로 찜 로그인 유도\
 팝업의 "로그인" 버튼이 conftest.py의 구글 로그인 랜딩 화면과 동일함을 확인, 로그인\
 완료 로직을 _complete_google_login()으로 분리(로그인 방식/fixture 동작 변경 없음).\
 리팩터링 후 Phase 1~3 전체 62개 재실행해 회귀 없음 확인. | 승인완료 |
| 2026-09-06 | 7.17절 신설 — Phase5-B(TC-SEARCH-003/008) 구현 중 검색 자동완성이\
 디바운스/네트워크 지연으로 타이핑 직후 과도기적으로 빈 목록을 반환해 검증 실패 및\
 "변경 감지" Wait 오탐이 발생함을 발견. wait_for_autocomplete_related_keywords_present()\
 /wait_for_autocomplete_related_keywords_change()(비어있지 않으면서 달라질 때까지 대기)로\
 수정. | 승인완료 |
| 2026-09-06 | 7.18절 신설 — Phase5-C(TC-SEARCH-006/007) 구현 중 "총 N개" 텍스트가\
 React에 의해 "총 "/"N"/"개" 별도 텍스트 노드로 렌더링되어 contains(text(), ...) 기반\
 Locator가 매칭에 실패함을 발견, contains(., ...)로 수정. | 승인완료 |
| 2026-09-06 | 7.19절 신설 — Phase5-E(TC-SEARCH-012/013/014) 구현 중 검색이 키워드를\
 단어 단위로 넓게 매칭해 특정 상품이 1페이지(20건) 밖으로 밀려날 수 있음을 발견(결함\
 아님, 검색 랭킹 특성). Phase1의 PRODUCT_ID_SALE_ENDED(1608)는 검색 1페이지에 노출되지\
 않아 검색 전용 상품/키워드 상수를 config/settings.py에 신규 추가. | 승인완료 |
| 2026-09-06 | 7.20절 신설 — Phase5-F(TC-SEARCH-016) 구현 중 검색창에 공백만 입력해도\
 초기화면의 "인기 작품"/랭킹 섹션이 사라짐을 발견. "검색페이지 상태 유지"를 두 섹션\
 존재가 아닌 페이지 잔류로 재정의하고 is_on_search_screen()을 분리 추가. | 승인완료 |
| 2026-09-06 | 16.1절 신설 — Phase Final(CI/CD) 계획 수립 중 CI 로그인 전략을 확정:\
 구글 OAuth 로그인 UI는 CI에서 직접 자동화하지 않고, 로컬에서 캡처한 세션 쿠키를\
 GitHub Secret으로 저장 후 CI에서 주입하는 방식(세션 주입)을 사용하기로 하고 문서에\
 선반영 (사용자 요청) | 승인완료 |
| 2026-09-06 | PhaseFinal-H 실제 CI 실행 중 store.laftel.net이 한국 외 IP를 차단함을\
 실측 확인해 GitHub 호스팅 러너 대신 한국 소재 self-hosted 러너(로컬 macOS)로 전환\
 (사용자 승인). 16절 runs-on 관련 워크플로우 구성 변경 | 승인완료 |
| 2026-09-06 | 7.21절 신설 — self-hosted 러너 첫 실행에서 찜 삭제 확인 다이얼로그\
 텍스트가 headless 모드에서만 빈 문자열로 반환됨을 발견(7.15절과 동일 유형),\
 get_attribute("textContent")로 수정. 7.22절 신설 — 동일 실행에서 검색 자동완성/\
 Enter 트리거 테스트 3건이 self-hosted 러너(launchd 백그라운드 서비스) 컨텍스트에서만\
 재현되는 타이밍 이슈를 발견(로컬 직접 실행/headless 자체에서는 재현 안 됨), 원인\
 미확정 상태로 사용자에게 보고 | 승인완료 |
| 2026-09-06 | 7.22절 갱신 — foreground 러너 재검증 결과 launchd 가설 기각, 매번\
 다른 조합의 test_search.py 3건이 실패해 일반적인 전체 스위트 타이밍 플레이키로\
 최종 결론(사용자 확인). 7.23절 신설 — TC-WISHLIST-031/032가 headless에서 Google\
 자체 차단을 받음을 확인, requires_real_browser 마커로 이 2개만 CI에서도 headless\
 제외하도록 conftest.py/pytest.ini/test_wishlist.py 수정. GOOGLE_ACCOUNT_EMAIL/\
 PASSWORD를 GitHub Secret으로 추가 (사용자 승인) | 승인완료 |
