# Development Guidelines - laftel-store QA Automation

이 문서는 이 저장소에서 작업하는 AI Agent(Claude Code 및 모든 Sub Agent/Skill)를 위한
**프로젝트 고유 운영 규칙**이다. 일반적인 개발 지식이나 CLAUDE.md에 이미 정의된 승인/추적성
원칙의 재설명은 포함하지 않는다. `CLAUDE.md`와 내용이 충돌하면 `CLAUDE.md`가 우선한다.

## 1. Project Overview

- Claude Code + MCP(Shrimp Task Manager, Playwright)를 이용해 `store.laftel.net`(라프텔
  스토어)의 QA 프로세스(PRD → TC → 자동화 대상 선정 → Roadmap → 자동화 코드 → CI → Slack
  알림)를 사람 승인 지점을 유지한 채 자동화하는 프로젝트다.
- 2026-09-05 기준 실제 산출물 상태: Project/Feature PRD, TC, Automation Candidate 평가,
  ROADMAP.md, AUTOMATION_GUIDE.md가 모두 `승인완료`/`자동화대상확정` 상태로 확정되어 있다.
  **자동화 코드(`automation/`)와 CI 워크플로우(`.github/workflows/`)는 아직 생성되지
  않았다.**
- 기술 스택 결정: Python + Selenium + pytest + POM (`docs/automation/AUTOMATION_GUIDE.md`
  1~4절이 Source of Truth). Roadmap/TC/PRD 세부 판단 우선순위는 `CLAUDE.md` 8절 표를
  그대로 따른다.

## 2. Directory & File Map (실제 존재 여부 기준)

| 경로 | 상태 | 용도 |
|---|---|---|
| `CLAUDE.md` | 존재 | 최상위 원칙 (모든 Agent/Skill보다 우선) |
| `shrimp-rules.md` | 존재(이 문서) | AI Agent 운영 규칙 |
| `docs/prd/project-prd.md` | 존재, 승인완료 | Project PRD |
| `docs/prd/Feature/prd-{slug}.md` | 존재, 승인완료 (cart/order/product-detail/search/wishlist) | Feature PRD |
| `docs/tc/{slug}.md` | 존재, 승인완료 | 원본 TC |
| `docs/tc/automation-candidates/{slug}.md` | 존재, 자동화대상확정 | 자동화 후보 평가 + Approved TC 목록 |
| `docs/roadmap/ROADMAP.md` | 존재, 승인완료 | Phase별 구현 Roadmap |
| `docs/automation/AUTOMATION_GUIDE.md` | 존재, 승인완료 | Python 자동화 코드 작성 규칙 (Source of Truth) |
| `scripts/sheets_sync/sheets_sync.py` | 존재 | Google Sheets 연동 CLI (TC/Candidate 전용) |
| `.claude/agents/*.md`, `.claude/agents/dev/*.md` | 존재 | Sub Agent 정의 |
| `.claude/skills/*/SKILL.md` | 존재 (`tc-writing`, `automation-candidate`) | 평가/작성 규칙 Skill |
| `automation/` (pages/tests/utils/config/test_data/screenshots/reports, conftest.py, pytest.ini, requirements.txt) | **미생성** | AUTOMATION_GUIDE 3절 예정 구조. 생성 시 그 구조를 그대로 따른다 |
| `.github/workflows/` | **미생성** | CI/CD, AUTOMATION_GUIDE 16절 |
| `.env` | 존재, `.gitignore`에 포함됨 | Google 서비스 계정 경로/Sheet ID, (향후) 테스트 계정 비밀번호 |

- `docs/`, `.claude/agents/`, `.claude/skills/`, `scripts/sheets_sync/` 하위 기존 파일을
  새 파일 생성 전에 항상 먼저 확인한다 — 동일 역할의 파일을 중복 생성하지 않는다.
- `automation/` 하위 코드를 처음 생성할 때는 AUTOMATION_GUIDE 3.1절의 import 경로 규칙
  (`automation.` prefix 없이 `automation/`을 루트로 import)이 실제로 동작하는지 더미
  테스트로 먼저 검증한 뒤 확정한다.

## 3. Document State Machine (문서별 상태 필드)

모든 산출물 Markdown은 frontmatter에 `상태` 필드를 가지며, 아래 전이만 허용된다. **하위
단계 Agent는 상태가 요구 조건에 미달한 상위 문서를 입력으로 사용하지 않는다.**

| 문서 | 상태 값 및 순서 | 다음 단계 입력 조건 |
|---|---|---|
| `docs/prd/project-prd.md`, `docs/prd/Feature/prd-{slug}.md` | `초안` → `승인완료` | `상태: 승인완료`만 TC 생성 근거로 사용 가능 |
| `docs/tc/{slug}.md` | `초안` → `승인완료` | `상태: 승인완료`만 자동화 후보 평가 근거로 사용 가능 |
| `docs/tc/automation-candidates/{slug}.md` | `평가중` → `사용자검토완료` → `자동화대상확정` | Roadmap/자동화 코드는 문서 전체가 `자동화대상확정`이고 그 안에서 `QA Decision: Approved`인 TC만 사용 가능 (`Hold`/`Rejected`/미검토 제외) |
| `docs/roadmap/ROADMAP.md` | `초안` → `승인완료` | 자동화 코드 구현은 `상태: 승인완료`만 입력으로 사용 |
| `docs/automation/AUTOMATION_GUIDE.md` | `초안` → `승인완료` | Roadmap/구현 모두 `상태: 승인완료`가 아니면 진행 금지 |

- 단계를 건너뛰어 임의로 최종 상태로 전환하지 않는다(예: Candidate 문서를 `평가중`에서
  바로 `자동화대상확정`으로 바꾸지 않음).
- 이미 최종 상태인 문서를 재수정해야 할 때는 각 Agent 정의 파일의 "승인완료(또는
  자동화대상확정) 문서 재수정 시 처리" 절차를 그대로 따른다(임의 직접 수정 금지).

## 4. Coding Convention (문서 vs 코드 구분)

- **Markdown 산출물(`docs/`, `.claude/agents/`, `.claude/skills/`)**: 전역
  `~/.claude/CLAUDE.md` 규칙 적용 — 한국어 서술, 변경 이력에 날짜/사유 기록.
- **Python 자동화 코드(`automation/` 하위, 향후 생성)**: 전역 CLAUDE.md의
  "2칸 들여쓰기/camelCase" 규칙이 아니라 `AUTOMATION_GUIDE.md` 1.1절 예외를 적용한다.
  - 들여쓰기 4칸, 변수/함수명 snake_case, 클래스명 PascalCase, 상수 UPPER_SNAKE_CASE.
  - 주석은 한국어(전역 CLAUDE.md 유지), 변수/함수명은 영어.
  - 이 예외는 `automation/` 하위 Python 코드에만 적용되며, `scripts/sheets_sync`(기존
    Python 도구 스크립트)의 기존 컨벤션을 바꾸지 않는다. `scripts/sheets_sync` 신규
    코드도 기존 스크립트 스타일을 따른다(임의로 4칸/2칸을 뒤섞지 않음).
- Page Object 클래스는 `~Page` 접미사 필수, 모든 Page 클래스는 `BasePage` 상속,
  Locator는 클래스 상단 `UPPER_SNAKE_CASE` 상수, Full XPath와 `time.sleep()` 금지 —
  상세는 AUTOMATION_GUIDE 4~7·18절.

## 5. Agent/Skill 책임 경계 (임의로 침범 금지)

| Agent | 유일한 책임 | 반드시 로드하는 Skill | 하지 않는 것 |
|---|---|---|---|
| `prd-agent` | Project/Feature PRD 작성 | 없음 | TC/Roadmap/코드 생성, Git 작업 |
| `tc-agent` | TC 작성 + Google Sheet 반영 | `tc-writing` | PRD 판단 기준 자체 정의, Sheet 직접 API 호출(스크립트 경유만) |
| `automation-candidate-agent` | 자동화 후보 평가 + QA Decision 검증/확정 | `automation-candidate` | TC/PRD 수정, 자동화 코드/Roadmap 생성, QA Decision 임의 변경 |
| `roadmap-agent` | Phase별 Roadmap 작성 | 없음(AUTOMATION_GUIDE를 Source of Truth로 참조) | Shrimp Task 생성, 코드 작성, PRD/TC/Candidate 문서 수정 |
| `automation-developer-agent` | 자동화 코드 구현 + pytest 실행 | 없음(AUTOMATION_GUIDE 참조) | 코드 리뷰, Git Commit/Push, 상위 산출물 임의 수정, CI/Slack 연동 |

- 새 Agent/Skill이 필요하면 기존 Agent를 확장하지 말고 책임이 분리된 새 파일을 만든다
  (`CLAUDE.md` 6절).
- 각 Agent 정의 파일(`.claude/agents/**/*.md`)의 "공통 원칙/가드레일"·"Workflow" 절이
  해당 Agent의 상세 실행 규칙이다. 이 문서(`shrimp-rules.md`)와 개별 Agent 정의가 절차
  세부사항에서 다르게 보이면, 그 Agent의 작업에 한해서는 해당 Agent 정의 파일을 따른다.

## 6. 외부 도구 사용 규칙

### 6.1 `scripts/sheets_sync/sheets_sync.py` (Google Sheets 연동)

- **Google Sheets 접근은 반드시 이 CLI를 Bash로 호출하는 방식만 사용한다.** 별도 API
  호출 코드를 즉석에서 작성하지 않는다.
- 주요 명령: `list`, `append --input <path> [--worksheet <name>] [--dry-run]`,
  `candidate-create-worksheet`, `candidate-sync --input <path> [--dry-run]`,
  `candidate-list`.
- `append`/`candidate-sync`는 실제 반영 전 항상 `--dry-run`으로 먼저 확인한다.
- `append`는 append-only이며 기존 행을 수정/삭제하지 않는다. ID 충돌 시 전체 반영을
  중단한다 — `--force` 같은 우회 옵션은 없으며 만들지 않는다.
- `candidate-sync`는 AI 작성 영역(TC ID + 6개 평가 축 + Automation Score +
  Candidate(AI) + 선정/제외 사유, 10개 컬럼)만 갱신한다. `QA Decision`/`QA Comment`
  컬럼은 어떤 방법으로도 쓰지 않는다(읽기는 `candidate-list`로만).
- 환경변수는 `.env`(`GOOGLE_SERVICE_ACCOUNT_FILE`, `GOOGLE_SHEET_ID`,
  `GOOGLE_SHEET_WORKSHEET`, `GOOGLE_SHEET_CANDIDATE_WORKSHEET`)로만 관리하며 코드/문서에
  하드코딩하지 않는다.

### 6.2 Playwright MCP (`mcp__playwright__browser_*`)

- 용도는 **Selenium 코드 작성 전 실제 페이지 구조/Locator 조사**로 한정한다
  (`automation-developer-agent` 전용, AUTOMATION_GUIDE 5절).
- 프로덕션 테스트 실행 도구는 Selenium이며, Playwright MCP로 Selenium 실행을 대체하지
  않는다.
- 조회·탐색 목적에만 사용하고, 페이지 상태나 서비스 데이터를 변경하는 `browser_evaluate`
  실행(계정 생성/삭제, 주문 시도 등)은 금지한다.

### 6.3 Shrimp Task Manager MCP

- Shrimp Task(작업 분해)는 승인된 `docs/roadmap/ROADMAP.md`(상태: 승인완료)를 입력으로만
  생성한다. Roadmap이 초안이거나 없으면 Task를 생성하지 않는다.
- `DATA_DIR`는 `.mcp.json`에 `shrimp_data/`로 고정되어 있다 — 임의로 다른 경로를
  지정하지 않는다.

## 7. Key File Interaction (동시 갱신 필요 지점)

- **TC 표 컬럼(9개: ID/Requirement ID/Feature/Test Scenario/Preconditions/Test
  Steps/Expected Result/Priority/Result)의 순서나 개수를 바꾸려면** 반드시
  `.claude/skills/tc-writing/SKILL.md` 2절과 `scripts/sheets_sync/sheets_sync.py`의
  파싱 로직을 **함께** 수정한다. 한쪽만 바꾸면 `append`/`candidate-sync` 파싱이 깨진다.
- **Candidate AI 평가 표 컬럼(10개: TC ID + 6개 축 + Automation Score +
  Candidate(AI) + 선정/제외 사유)을 바꾸려면** `.claude/skills/automation-candidate/
  SKILL.md` 8절과 `sheets_sync.py`의 `CANDIDATE_AI_COLUMNS`를 **함께** 수정한다.
- **`docs/tc/{slug}.md`(원본 TC)가 재승인으로 변경되면**, 해당 Feature의
  `docs/tc/automation-candidates/{slug}.md`가 무효화될 수 있다 — Candidate 문서
  프런트매터의 "대상 TC 문서 최근 변경일"과 비교해 재평가 필요 여부를 확인한다
  (`automation-candidate-agent` 워크플로우 3번).
- **Candidate 문서의 Approved TC 목록이 바뀌면**, `docs/roadmap/ROADMAP.md`의 대상
  TC 수·Phase 매핑표가 최신 상태와 어긋날 수 있다 — Roadmap을 그대로 재사용하지 말고
  Candidate 문서를 직접 재확인한다(`roadmap-agent` 가드레일).
- **`docs/automation/AUTOMATION_GUIDE.md`가 변경되면**, 이미 작성된 `automation/` 코드
  중 변경된 절(Locator 우선순위, 디렉터리 구조 등)에 해당하는 부분의 재검토가 필요하다.
- **`.mcp.json`을 수정할 때**(서버 추가/경로 변경 등)는 `DATA_DIR`가 여전히 이 저장소의
  `shrimp_data/`를 가리키는지 확인한다 — 다른 프로젝트의 Shrimp 데이터와 섞이지 않도록
  한다.

## 8. AI Decision-making Standards

- **상위 산출물 상태가 요구 조건에 못 미치면(초안 상태 등) 즉시 중단하고 사용자에게
  안내한다.** 부족한 정보를 추정해서 다음 단계를 진행하지 않는다.
- **문서 간 내용이 충돌하면**(예: Candidate 문서의 TC ID가 원본 TC에 없음, Roadmap
  대상 TC 수가 Candidate 문서와 다름) 임의로 하나를 선택하지 않고 충돌 내용을 그대로
  사용자에게 보고한 뒤 확인을 받는다(`CLAUDE.md` 8절).
- **QA Decision 값 판단**: 정확히 `Approved`/`Rejected`/`Hold`(대소문자·공백까지 일치)만
  유효하다. 빈 값은 "미검토"로, 그 외 모든 값(`approved`, `승인`, 오탈자 등)은 Validation
  Error로 처리하며 임의 보정하지 않는다.
- **자동화 대상 판단 조건은 항상 다음 두 조건의 AND다** — 어느 한쪽만으로 판단하지
  않는다.
  ```
  Candidate 문서 상태 = 자동화대상확정  AND  QA Decision = Approved
  ```
- **Git Commit/Push, Production 데이터 변경(계정 생성/삭제 등), Google Sheet 실제 반영
  (dry-run 아님)** 앞에서는 항상 실행 직전 결과를 사용자에게 보여주고 명시적 승인을
  받는다. "괜찮아 보인다" 같은 모호한 응답은 승인으로 간주하지 않는다.
- 코드/문서 작성을 완료로 보고하기 전에 관련 테스트(자동화 코드는 pytest, TC/Candidate
  문서는 각 스크립트의 `--dry-run`)를 실제로 실행해 결과를 확인한다. 실행하지 않고
  "완료"로 보고하지 않는다.

## 9. Prohibited Actions

- 승인된 상위 산출물(PRD/TC/Candidate/Roadmap/AUTOMATION_GUIDE)을 재승인 절차 없이
  직접 수정하는 것.
- `sheets_sync.py`의 사용자 작성 영역(`QA Decision`/`QA Comment`)을 어떤 명령으로도
  쓰는 것.
- `sheets_sync.py`가 제공하지 않는 행 수정/삭제 기능을 즉석 스크립트로 대체 구현하는 것.
- Playwright MCP로 Production 데이터를 변경(계정 생성/삭제, 주문 시도 등)하는 것.
- `automation/` 코드에서 Full XPath 사용, `time.sleep()` 사용, Page Layer에서
  Assertion 수행, 비밀번호 등 민감정보를 코드/로그/리포트/스크린샷에 노출하는 것.
- 사용자 승인 없이 Git Commit/Push를 수행하는 것.
- 현재 요청받은 단계의 다음 단계 산출물을 임의로 선행 생성하는 것(예: TC 작성 중
  Roadmap이나 자동화 코드를 미리 만드는 것).
- 다른 프로젝트에서 재사용 가능하도록 설계된 Skill(`tc-writing`,
  `automation-candidate`)에 이 프로젝트 전용 정보(URL, 계정 등)를 하드코딩하는 것.

## 변경 이력

| 날짜 | 변경 사유 |
|---|---|
| 2026-09-05 | 최초 생성 — 기존 CLAUDE.md/Agent 정의/Skill/AUTOMATION_GUIDE/ROADMAP/sheets_sync 문서를 근거로 AI Agent 운영 규칙 초안 작성 |
