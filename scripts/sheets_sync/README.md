# sheets_sync

승인된 TC Markdown 문서(`docs/tc/{feature-slug}.md`)를 Google Spreadsheet에 반영하고,
자동화 후보 평가 결과(`docs/tc/automation-candidates/{feature-slug}.md`)를 Google Spreadsheet와
동기화하기 위한 CLI. `tc-agent`와 `automation-candidate-agent`가 Bash로 이 스크립트만
호출하며, Google Sheets를 직접 제어하지 않는다.

## 설치

```bash
pip install -r scripts/sheets_sync/requirements.txt
```

## 사전 준비 (최초 1회)

1. Google Cloud Console에서 프로젝트를 만들고 **Google Sheets API**를 활성화한다.
2. 서비스 계정(Service Account)을 생성하고 JSON 키 파일을 다운로드한다.
3. 반영 대상 Google Spreadsheet를 열어, 위 서비스 계정 이메일(`...@...iam.gserviceaccount.com`)을
   **편집자(Editor)** 권한으로 공유한다.
4. 프로젝트 루트에 `.env` 파일을 만들고 아래 값을 채운다 (`.env`는 `.gitignore`에 포함되어 있으므로
   커밋되지 않는다).

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/absolute/path/to/service-account.json
GOOGLE_SHEET_ID=스프레드시트_URL의_d와_edit_사이_값
# 선택: 기본 워크시트명은 "TC" — 다른 이름을 쓰려면 아래를 설정
# GOOGLE_SHEET_WORKSHEET=TC
```

`GOOGLE_SHEET_ID`는 스프레드시트 URL `https://docs.google.com/spreadsheets/d/{ID}/edit`에서
`{ID}` 부분이다.

## 사용법

### 기존 TC 조회

```bash
python scripts/sheets_sync/sheets_sync.py list
python scripts/sheets_sync/sheets_sync.py list --ids-only
python scripts/sheets_sync/sheets_sync.py list --worksheet Testcase_Cart
```

### TC 추가 (append-only)

```bash
# 1) 먼저 dry-run으로 반영될 내용을 미리 확인한다 (ID 충돌 여부 포함)
python scripts/sheets_sync/sheets_sync.py append --input docs/tc/cart.md --worksheet Testcase_Cart --dry-run

# 2) 문제 없으면 실제로 반영한다
python scripts/sheets_sync/sheets_sync.py append --input docs/tc/cart.md --worksheet Testcase_Cart
```

`--worksheet`를 생략하면 `GOOGLE_SHEET_WORKSHEET` 환경변수(없으면 기본값 `TC`) 하나의
워크시트에 모아서 반영한다. Feature별로 별도 시트에 반영하려면 매번 `--worksheet`로
대상 시트명을 지정한다(예: `Testcase_Search`, `Testcase_ProductDetail`, `Testcase_Order`,
`Testcase_Wishlist`, `Testcase_Cart`).

- 입력 파일 하나에 "## TC 목록", "## 결함 의심 항목" 등 여러 개의 TC 표가 있어도, 컬럼 구성이
  `tc-writing` Skill의 9개 컬럼 정의와 일치하는 표는 모두 찾아 하나로 합쳐 반영한다.
- 이 스크립트는 **append(추가)만 수행**하며, 기존 행을 수정하거나 삭제하지 않는다.
- 입력 파일의 TC ID가 Spreadsheet에 이미 존재하는 ID와 충돌하면, 아무 것도 반영하지 않고
  전체를 중단한다(부분 반영 없음). 이 경우 기존 TC를 실제로 수정해야 하는지 사용자와 함께
  결정한 뒤, 필요하면 Spreadsheet를 수동으로 수정하거나 별도 방법을 논의한다.
- 대상 워크시트(기본값 `TC`)가 아직 없으면, `append` 실행 시(실제 반영 시에만, dry-run에서는
  생성하지 않음) 9개 컬럼 헤더와 함께 새로 만든다.

### 자동화 후보 평가 동기화

`automation-candidate-agent`가 사용하는 명령이다. Candidate 문서의 "AI 평가 결과" 표(TC ID +
6개 평가 축 + Automation Score + Candidate(AI) + 선정/제외 사유, 총 10개 컬럼)만 Spreadsheet에
반영하며, 사용자가 Sheet에 직접 입력하는 `QA Decision` / `QA Comment` 컬럼은 어떤 경우에도
쓰지 않는다.

```bash
# 1) 최초 1회: 자동화 후보 워크시트 생성 (이미 있으면 오류 — 정상 동작)
python scripts/sheets_sync/sheets_sync.py candidate-create-worksheet

# 2) Candidate 문서를 dry-run으로 미리 확인
python scripts/sheets_sync/sheets_sync.py candidate-sync --input docs/tc/automation-candidates/cart.md --dry-run

# 3) 문제 없으면 실제로 반영 (신규 TC는 새 행 추가, 기존 TC는 AI 영역만 갱신)
python scripts/sheets_sync/sheets_sync.py candidate-sync --input docs/tc/automation-candidates/cart.md

# 4) Sheet에 입력된 QA Decision/QA Comment를 포함해 전체 조회
python scripts/sheets_sync/sheets_sync.py candidate-list
```

- 기본 워크시트명은 `Automation Candidates`(모든 Feature가 하나의 워크시트를 공유하며, TC ID로
  구분한다). 다른 이름을 쓰려면 `--worksheet` 또는 `GOOGLE_SHEET_CANDIDATE_WORKSHEET` 환경변수를
  사용한다.
- `candidate-sync`는 입력 파일 안의 TC ID가 이미 Sheet에 존재하면 AI 작성 영역(A~J열)만
  덮어쓰고, `QA Decision`/`QA Comment`(K~L열)는 건드리지 않는다. 신규 TC ID는 새 행으로
  추가되며 이때 `QA Decision`/`QA Comment`는 빈 값으로 시작한다.
- 워크시트 헤더가 Candidate 컬럼 정의와 다르면(예: 사용자가 임의로 컬럼을 바꾼 경우) 안전을
  위해 아무 것도 반영하지 않고 중단한다.

## 환경변수 요약

| 변수 | 필수 | 설명 |
|---|---|---|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | 예 | 서비스 계정 JSON 키 파일의 로컬 경로 |
| `GOOGLE_SHEET_ID` | 예 | 대상 Google Spreadsheet ID |
| `GOOGLE_SHEET_WORKSHEET` | 아니오 (기본값 `TC`) | `list`/`append`의 대상 워크시트(탭) 이름 |
| `GOOGLE_SHEET_CANDIDATE_WORKSHEET` | 아니오 (기본값 `Automation Candidates`) | `candidate-*` 명령의 대상 워크시트(탭) 이름 |

## 제한 사항

- `list`/`append`(TC 원본 동기화)는 행 수정(update)/삭제(delete) 기능을 의도적으로 제공하지
  않는다. 승인완료된 TC를 재수정해야 하는 경우는 `tc-agent`의 "승인완료 문서 재수정 시 처리"
  절차를 따르며, Spreadsheet 반영 방법은 그때 사용자와 함께 결정한다.
- `candidate-sync`만 예외적으로 기존 행의 AI 작성 영역(A~J열)을 갱신할 수 있다. 이는 재평가된
  TC의 점수를 반영하기 위한 것이며, 컬럼 범위가 AI 작성 영역으로 고정되어 있어 사용자 작성 영역
  (`QA Decision`/`QA Comment`)은 어떤 경우에도 덮어쓰지 않는다. 삭제 기능은 여전히 제공하지
  않는다.
- 이 스크립트는 인증/네트워크 오류를 그대로 사용자에게 보고하며, 임의로 재시도하거나 오류를
  숨기지 않는다.
