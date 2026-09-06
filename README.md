# laftel-store QA 자동화

[라프텔 스토어](https://store.laftel.net/)(애니메이션 굿즈 커머스)를 대상으로, 요구사항
정의부터 Test Case 작성, 자동화 코드 구현, CI 실행, Slack 알림까지 QA 프로세스 전체를
Claude Code 기반 Sub Agent/Skill로 진행한 프로젝트입니다. 각 단계는 사람의 승인 지점을
유지한 채 진행됩니다. 전체 운영 원칙은 [`CLAUDE.md`](./CLAUDE.md)를 따릅니다.

## 워크플로우

```
Project/Feature PRD → Test Case → 자동화 대상 선정(승인) → Roadmap
  → 자동화 코드 구현 → 테스트 실행/검증 → 코드 리뷰
  → Git Commit(승인) → Git Push(승인) → GitHub Actions CI → Slack 알림
```

## 문서 (`docs/`)

| 구분 | 위치 | 비고 |
|---|---|---|
| Project PRD | `docs/prd/project-prd.md` | 서비스 개요, 대상 범위 |
| Feature PRD | `docs/prd/Feature/prd-*.md` | 상품상세/카트/주문/찜/검색 |
| Test Case | `docs/tc/*.md` | Feature별 TC, Google Spreadsheet와 동기화 |
| 자동화 대상 선정 | `docs/tc/automation-candidates/*.md` | QA Decision(Approved) 근거 |
| Roadmap | `docs/roadmap/ROADMAP.md` | Phase별 구현 순서, 승인됨 |
| 자동화 컨벤션 | `docs/automation/AUTOMATION_GUIDE.md` | Selenium/pytest 컨벤션, 발견된 이슈·해결 이력 |

각 문서는 상단에 `상태: 승인완료` 메타데이터와 하단 변경 이력 표를 가지며,
승인된 상위 문서는 후속 단계에서 임의로 수정하지 않습니다([`CLAUDE.md`](./CLAUDE.md) 7절).

## 자동화 코드 (`automation/`)

Selenium + pytest + Page Object Model 구조입니다.

```
automation/
├── conftest.py       # driver / logged_in_driver 등 공용 fixture
├── pytest.ini
├── requirements.txt
├── config/           # settings.py — BASE_URL, 테스트 상품 ID 등 실측 상수
├── pages/            # Page Object (화면 1개당 파일 1개)
├── tests/            # Feature별 테스트 (TC ID를 docstring에 명시)
├── scripts/          # 세션 쿠키 캡처, Slack 알림, CI 실패 로컬 재검증 스크립트
├── reports/          # pytest-html / JUnit XML 결과 (git 미포함)
└── screenshots/      # 실패 시 자동 캡처 (git 미포함)
```

### 로컬 실행

#### 사전 준비물

- Python 3.9 이상 (검증 환경: 3.9.6)
- Google Chrome — `selenium==4.15.2`가 Selenium Manager로 버전에 맞는 chromedriver를
  자동 설치하므로 chromedriver를 별도로 설치할 필요는 없습니다.
- 한국 네트워크 환경 — `store.laftel.net`이 한국 외 IP를 차단하므로 로컬 실행도
  한국에서 접속 가능한 환경이어야 합니다.

#### 설치 및 환경변수 설정

```bash
cd automation
pip install -r requirements.txt
cp .env.example .env
```

`.env`에 값을 채웁니다(`automation/.env.example` 참고, 파일은 `.gitignore`에 포함되어
커밋되지 않습니다):

| 변수 | 용도 |
|---|---|
| `GOOGLE_ACCOUNT_EMAIL` / `GOOGLE_ACCOUNT_PASSWORD` | 구글 로그인 계정. `config/settings.py`의 `LOGIN_METHOD`가 기본값 `"google"`이라 사실상 필수입니다. |
| `TEST_ACCOUNT_EMAIL` / `TEST_ACCOUNT_PASSWORD` | 이메일 로그인 계정. `LOGIN_METHOD`를 `"email"`로 바꿀 때만 사용됩니다. |

#### 실행

```bash
python3 -m pytest -v                                                            # 전체 113개
python3 -m pytest tests/test_cart.py -v                                         # 파일 단위
python3 -m pytest tests/test_cart.py::test_empty_cart_shows_empty_message -v    # 단일 테스트
python3 -m pytest -k "wish" -v                                                  # 이름 패턴 매칭
```

로컬 실행은 기본적으로 headless가 아니라 Chrome 창이 실제로 뜹니다(`conftest.py`의
`driver` fixture가 `CI` 환경변수 유무로 headless 여부를 분기하며, CI에서만 headless를
적용합니다). `@pytest.mark.requires_real_browser`가 붙은 테스트(TC-WISHLIST-031/032)는
실제 구글 로그인 화면을 그대로 통과해야 하므로 로컬 환경에서도 별도 설정 없이 동일하게
동작합니다.

#### 실행 결과 확인

위 명령 중 어떤 방식으로 실행하든(`pytest.ini`의 `addopts`가 항상 적용되므로 별도
옵션을 주지 않아도) 실행이 끝나면 아래 파일이 자동으로 생성/갱신됩니다.

- HTML 리포트: `automation/reports/report.html`
- JUnit XML 리포트: `automation/reports/results.xml` (CI의 Slack 알림이 파싱하는 것과 동일한 형식)
- 실패 시 자동 저장되는 스크린샷: `automation/screenshots/`

셋 다 `.gitignore`에 포함되어 커밋되지 않습니다. Phase별로 리포트 파일명을 따로 남기고
싶다면 `--html=reports/report_phase5.html`처럼 직접 지정하면 기본값 대신 그 이름으로
저장됩니다.

#### 문제가 생겼을 때

- `KeyError` 등 로그인 계정 관련 에러가 나면 `.env` 값 누락·오타를 먼저 확인하세요.
- 특정 테스트가 간헐적으로만 실패하면 [`AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md)
  7절(발견된 이슈)과 7.22절(전체 스위트 장시간 실행 시 타이밍 플레이키)을 참고하세요.

### 테스트 현황

| Feature | 테스트 파일 | 개수 |
|---|---|---|
| 상품상세 | `test_product_detail.py` | 35 |
| 카트 | `test_cart.py` | 16 |
| 주문 | `test_order.py` | 11 |
| 찜 | `test_wishlist.py` | 28 |
| 검색 | `test_search.py` | 23 |
| **합계** | | **113** |

## CI/CD

`.github/workflows/test.yml`이 `main` 브랜치 push마다 실행됩니다. `store.laftel.net`이
한국 외 IP를 차단하기 때문에 self-hosted 러너(한국 소재 macOS)를 사용하며, 구글 OAuth
로그인 UI는 CI에서 직접 자동화하지 않고 로컬에서 캡처한 세션 쿠키를 GitHub Secret으로
주입합니다. 실행 결과(성공/실패, 실패 시 파일·사유)는 Slack으로 통보됩니다. 세부 내용은
[`AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md) 16절을 참고하세요.

CI가 실패했을 때 실제 문제인지, 알려진 일시적 타이밍 이슈(7.22절)인지 빠르게 판별하려면:

```bash
bash automation/scripts/verify_ci_failures_locally.sh [RUN_ID]   # 생략 시 최신 실행
```

## Sub Agent / Skill

`.claude/agents/`, `.claude/skills/`에 PRD 작성·TC 작성·자동화 대상 선정·Roadmap
작성·자동화 코드 구현을 담당하는 전용 Agent/Skill이 정의되어 있으며, 각각 단일 책임만
가지고 서로의 역할을 침범하지 않습니다([`CLAUDE.md`](./CLAUDE.md) 6절).
