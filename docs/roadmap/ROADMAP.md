---
문서유형: Automation Development Roadmap
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
관련 Feature PRD: [feature/prd-product-detail.md, feature/prd-cart.md, feature/prd-order.md, feature/prd-wishlist.md, feature/prd-search.md]
관련 Automation Candidate 문서: [tc/automation-candidates/product-detail.md, tc/automation-candidates/cart.md, tc/automation-candidates/order.md, tc/automation-candidates/wishlist.md, tc/automation-candidates/search.md]
관련 Automation Guide: docs/automation/AUTOMATION_GUIDE.md
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
승인일: 2026-09-05
---

# ROADMAP - 라프텔 스토어 자동화 개발 Roadmap

## 1. 개요 및 범위

- **목적**: 자동화 대상으로 확정된 TC를 기반으로, 개발팀이 순서대로 실행할 수 있는 자동화
  코드 구현 Roadmap을 제시한다.
- **대상 정의**: 다음 조건을 모두 만족하는 TC만 이번 Roadmap의 구현 대상으로 한다.
  ```
  Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
  AND
  QA Decision = Approved
  ```
- **대상 Feature 및 확정 TC 수 총계**

  | Feature | Approved TC 수 |
  |---|---|
  | product-detail (상품상세) | 34 |
  | cart (카트) | 16 |
  | order (주문) | 11 |
  | wishlist (찜) | 28 |
  | search (검색) | 23 |
  | **합계** | **112** |

- **Out of Scope(이번 Roadmap 범위 밖)**
  - Shrimp Task 생성 및 세부 작업 분해(이후 별도 단계)
  - 실제 자동화 코드 구현(이후 별도 단계, 승인된 Roadmap을 입력으로 사용)
  - Hold/Rejected TC(아래 표 참조) — 이번 확정 범위에서 제외됨
  - **TC-PRODUCT-DETAIL-008**(내 스토어 > 주문내역에서 상품 클릭 시 상품상세 진입): Candidate
    문서상 QA Decision은 Approved이나, 자동화 테스트는 실제 결제를 완료하지 않으므로
    (AUTOMATION_GUIDE 11.2절) 고정 계정에 사전 완료된 주문 데이터를 안정적으로 준비할 수
    없어, 사용자 결정에 따라 이번 Roadmap 구현 범위에서 제외한다(8절 리스크 항목 참조 —
    단, Candidate 문서 QA Decision은 여전히 Approved로 남아 있어 별도 확인이 필요하다).

  | Feature | Hold(미확정) | Rejected |
  |---|---|---|
  | product-detail | 10건 (001,009,016,017,018,021,022,023,029,030) | 1건 (041) |
  | cart | 7건 (003,004,005,006,011,017,021) | 0건 |
  | order | 8건 (003,008,010,011,012,013,014,016) | 1건 (006) |
  | wishlist | 5건 (010,011,013,018,019) | 0건 |
  | search | 0건 | 6건 (004,005,017,018,028,029) |

## 2. 입력 문서 스냅샷

| 문서 | 상태 | 최근 변경일 |
|---|---|---|
| docs/prd/project-prd.md | 승인완료 | 2026-09-03 |
| docs/prd/Feature/prd-product-detail.md | 승인완료 | 2026-09-05 |
| docs/prd/Feature/prd-cart.md | 승인완료 | 2026-09-05 |
| docs/prd/Feature/prd-order.md | 승인완료 | 2026-09-04 |
| docs/prd/Feature/prd-wishlist.md | 승인완료 | 2026-09-05 |
| docs/prd/Feature/prd-search.md | 승인완료 | 2026-09-04 |
| docs/tc/product-detail.md | 승인완료 | 2026-09-05 |
| docs/tc/cart.md | 승인완료 | 2026-09-05 |
| docs/tc/order.md | 승인완료 | 2026-09-05 |
| docs/tc/wishlist.md | 승인완료 | 2026-09-05 |
| docs/tc/search.md | 승인완료 | 2026-09-04 |
| docs/tc/automation-candidates/product-detail.md | 자동화대상확정 | 2026-09-05 (대상 TC 문서 최근 변경일 기준과 일치 확인) |
| docs/tc/automation-candidates/cart.md | 자동화대상확정 | 2026-09-05 (일치) |
| docs/tc/automation-candidates/order.md | 자동화대상확정 | 2026-09-05 (일치) |
| docs/tc/automation-candidates/wishlist.md | 자동화대상확정 | 2026-09-05 (일치) |
| docs/tc/automation-candidates/search.md | 자동화대상확정 | 2026-09-04 (일치) |
| docs/automation/AUTOMATION_GUIDE.md | 승인완료 | 2026-09-05 |

> Validation 결과: 5개 Candidate 문서 모두 상태가 `자동화대상확정`이며, Approved TC 목록
> 건수(35/16/11/28/23, 합계 113)가 원본 TC 문서의 전체 TC 행 수(46/23/20/33/29)와 모순 없이
> 부분집합을 이룬다. Candidate 문서 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"과
> 원본 TC 문서의 "최근 변경일"이 5개 Feature 모두 정확히 일치해, 확정 이후 원본 TC가 추가로
> 변경된 정황은 발견되지 않았다. product-detail의 TC-022/023 재평가 이력도 재평가 시점
> (2026-09-05)과 원본 TC 최근 변경일(2026-09-05)이 일치해 정합성이 확인되었다(재평가 후
> 원본이 다시 바뀌지 않음).

## 3. 기술 스택 및 아키텍처 (Reference)

AUTOMATION_GUIDE.md 1~4절 요약이며, 상세 규칙은 원본 문서를 기준으로 한다.

- **언어/도구**: Python + Selenium WebDriver + pytest, 리포팅은 pytest-html + JUnit XML 병행
- **실행 환경**: Chrome(ChromeDriver), 일반 데스크톱 창 크기, 모바일 에뮬레이션 미사용,
  대상은 Production 단일 환경(`https://store.laftel.net/`)
- **아키텍처**: Page Object Model(POM) — 화면 단위 1 Page 클래스, 모든 Page는 `BasePage` 상속,
  Page는 Assertion 금지·Test에서만 Assertion 수행
- **디렉터리 구조(예정)**: `automation/{pages,locators,tests,utils,config,test_data,screenshots,reports}`,
  `conftest.py`, `pytest.ini`, `requirements.txt` (3절)
- **코딩 스타일 예외**: Python 코드에 한해 4칸 들여쓰기 + snake_case(PEP8), 전역 CLAUDE.md의
  2칸/camelCase 예외로 사용자 승인됨(1.1절)
- **테스트 데이터**: dev/staging 없이 Production 단일 환경, 로그인 필요 TC는 고정 계정 재사용
  (11.1절), 계정 비밀번호는 `.env`로만 관리
- **CI/CD**: GitHub Actions, Push 시 자동 실행 → Slack 실패 알림(16절)

## 4. 구현 순서 결정 기준

1. **기능적 의존성 우선**: 사용자 조작 시나리오(Feature PRD 3절) 기준으로 한 Feature의 진입/
   전제 조건이 다른 Feature의 완성된 기능에 의존하는지 확인한다.
   - 카트 진입은 상품상세의 "담기" 액션에서 시작된다(cart PRD REQ-CART-001, product-detail
     PRD REQ-PRODUCT-DETAIL-035~038).
   - 주문/결제 화면 진입은 상품상세의 "바로구매"(TC-ORDER-001) **또는** 카트의 "구매하기"
     (TC-ORDER-002) 두 경로 모두 Approved이므로, 주문 Phase는 상품상세·카트 Phase가 모두
     끝난 뒤에 착수해야 두 진입 경로를 온전히 자동화할 수 있다.
   - AUTOMATION_GUIDE 11.1절에 따라 카트/찜/주문 TC는 로그인 상태(고정 계정)가 전제 조건이다.
2. **우선순위/리스크 반영(의존성이 없거나 동등한 경우에 한함)**: Approved TC 건수, Business
   Criticality가 높은 TC(P0/BC 5) 비중, Automation Score를 참고용으로 반영하되 기계적으로
   순서를 정하지 않는다.
3. **결합도 고려**: 상품상세는 다른 모든 Feature(찜 토글, 구매 위젯, 상태별 버튼, 검색 결과의
   상세 진입 검증)에서 공통으로 재사용되는 Page Object를 제공하므로, 가장 먼저 구현해 이후
   Feature 구현 시 중복 구현을 방지한다(AUTOMATION_GUIDE 19절).
4. **Phase 0(공통 기반)은 항상 최우선**이며, Phase Final(CI/CD·Slack)은 전체 Feature Phase
   완료 후 마지막에 배치한다.

## 5. Phase별 Roadmap

### Phase 0: 공통 기반 구축 (Foundation)

- **산출물**
  - `automation/` 디렉터리 구조 생성(`pages/`, `tests/`, `utils/`, `config/`, `test_data/`,
    `screenshots/`, `reports/`)
  - `pages/base_page.py`(BasePage — 공통 Wait/클릭/입력/텍스트 조회 래핑 메서드)
  - `conftest.py`(WebDriver fixture, `function` scope, 로그인 상태 fixture 등)
  - `config/` 환경 설정(BASE_URL=`https://store.laftel.net/`, 타임아웃 등)
  - `test_data/accounts.json` 템플릿(계정 이메일 자리만 우선 정의 — 실제 값은 사용자가
    구현 착수 시점에 별도 전달 예정, AUTOMATION_GUIDE 11.1절)
  - `.env` 템플릿(비밀번호 등 민감정보 환경변수용, `.gitignore` 반영 확인)
  - `pytest.ini`, `requirements.txt`
  - AUTOMATION_GUIDE 3.1절 Import 경로 규칙의 실제 동작 검증(더미 테스트로 1회 확인)
- **근거**: AUTOMATION_GUIDE 3, 9, 11, 12절 — 모든 Feature Phase 구현의 전제 조건
- **Definition of Done**: 위 골격을 생성한 뒤, 더미 Page/테스트 1개로 `pytest`가 정상
  실행되어 PASSED가 확인되어야 한다.
- **착수 전 확인 필요**: 로그인 필요 TC(Phase 1부터 존재)가 있으므로, 고정 계정 정보
  (이메일/개수, 비밀번호)를 이 Phase 완료 시점까지 사용자로부터 전달받아야 한다.

### Phase 1: 상품상세(product-detail) 자동화 구현

- **대상 TC**: 34건 — TC-PRODUCT-DETAIL-002, 003, 004, 005, 006, 007, 010, 011, 012,
  013, 014, 015, 019, 020, 024, 025, 026, 027, 028, 031, 032, 033, 034, 035, 036, 037, 038,
  039, 040, 042, 043, 044, 045, 046
  (TC-PRODUCT-DETAIL-008은 사용자 결정에 따라 이번 구현 범위에서 제외 — 1절 Out of Scope,
  8절 참고)
- **필요 Page Object**
  - `ProductDetailPage`(상단 바, 이미지 캐러셀, 작품명/가격, 배송정보, "같은 작품 굿즈"
    캐러셀, 상세정보 탭/더보기, 하단 고정 찜·구매 영역, 옵션/수량 선택, 상태별 버튼)
  - `ProductInfoPage`(`/products/{id}/product-info`), `ExchangeReturnInfoPage`
    (`/products/{id}/exchange-return-info`), `SellerInfoPage`(`/products/{id}/seller-info`),
    `NoticePage`(`/products/{id}/notice`) — 아코디언 4개 항목
  - `RelatedProductsPage`(`/products/{id}/related`, "더보기" 목록)
  - `NotFoundPage`(커스텀 404 에러 페이지, TC-007)
  - 진입 경로 전제 조건 확보용 **최소** Page Object: `MyStorePage`(`/my`, TC-003 진입용),
    카트/찜 화면으로의 **최소 내비게이션**(TC-004/005 진입용 — 전체 카트/찜 기능이 아닌
    "상품 1개 추가 후 진입"까지만). 전체 기능은 Phase 2(카트)/Phase 4(찜)에서 완성한다.
- **선행 조건(의존 Feature)**: 없음(Phase 0만 전제). 단, 찜 관련 TC(031~034, 042~046 일부)는
  로그인 상태(고정 계정)가 필요하다.
- **우선순위 근거**
  - 검색(TC-013/014 상태별 버튼 검증)·카트(담기 액션)·주문(바로구매 진입)·찜(토글 개념)이
    모두 상품상세 화면 또는 그 구성요소를 공유하거나 재사용하므로, 다른 Feature보다 먼저
    구현해야 이후 Phase에서 중복 구현 없이 재사용할 수 있다.
  - Approved TC 건수가 35건으로 가장 많고, 대부분 URL 직접 진입(`/products/{id}`)으로
    독립적인 테스트가 가능해 다른 Feature의 완성을 기다릴 필요가 없다.

### Phase 2: 카트(cart) 자동화 구현

- **대상 TC**: 16건 — TC-CART-001, 002, 007, 008, 009, 010, 012, 013, 014, 015, 016, 018,
  019, 020, 022, 023
- **필요 Page Object**: `CartPage`(전체선택/판매자 그룹/개별 체크박스, 수량 조절(-/+),
  개별·일괄·품절 삭제 확인 팝업, 배송비 안내 문구, 결제금액 요약, 하단 고정
  "{총 결제금액}원 구매하기 (N)" 버튼)
- **선행 조건(의존 Feature)**: Phase 1 `ProductDetailPage`의 "구매하기 > 장바구니 담기"
  액션(테스트 데이터 준비용, REQ-CART-001), 로그인(고정 계정)
- **우선순위 근거**: 카트 화면 진입 자체가 상품상세의 담기 액션에서 시작되는 기능적 의존
  관계이며(cart PRD 1절), 상품상세 → 카트 → 주문으로 이어지는 구매 퍼널의 두 번째 단계다.

### Phase 3: 주문(order) 자동화 구현

- **대상 TC**: 11건 — TC-ORDER-001, 002, 004, 005, 007, 009, 015, 017, 018, 020, 021
  (구현 완료 시점 실측으로 TC-ORDER-006/019가 자동화 불가로 확인되어 Hold로 전환되고,
  대신 신규 발견된 TC-ORDER-021이 Approved로 확정됨 — 8절 리스크 항목 참고)
- **필요 Page Object**: `CheckoutPage`(`/check-out/{uuid}` — 배송지 입력 필드 및 필수값
  검증, "우편번호 찾기" 버튼 클릭까지의 진입 확인, 배송 요청사항 드롭다운/직접입력, 주문상품
  목록, 쿠폰 섹션, 결제수단 섹션, 결제금액 요약, 필수 동의 체크, 하단 고정 구매하기 버튼)
- **선행 조건(의존 Feature)**: Phase 1(상품상세 "바로구매" 진입, TC-ORDER-001)과 Phase 2
  (카트 "구매하기" 진입, TC-ORDER-002) **둘 다** 필요, 로그인(고정 계정)
- **우선순위 근거**: 승인된 주문/결제 화면 진입 경로 2건이 각각 상품상세와 카트에 의존하므로,
  두 Phase가 모두 완료되어야 전체 시나리오를 온전히 자동화할 수 있다. 구매 퍼널의 최종
  단계이자 결제 직전 핵심 방어 로직(필수값 검증·필수 동의)을 포함한다.
- **리스크**: TC-ORDER-019는 PG 결제창 진입까지만 확인하며, 실제 결제(PG 결제 완료)는 어떤
  테스트에서도 수행하지 않는다(AUTOMATION_GUIDE 11.2절). 우편번호 찾기(카카오 외부 모듈)
  자체 노출 검증(TC-ORDER-006)은 Rejected로 이미 제외되어 있어 Approved 범위에는 포함되지
  않는다.

### Phase 4: 찜(wishlist) 자동화 구현

- **대상 TC**: 28건 — TC-WISHLIST-001, 002, 003, 004, 005, 006, 007, 008, 009, 012, 014,
  015, 016, 017, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 030, 031, 032, 033
- **필요 Page Object**
  - `WishlistPage`(`/my/wish` — "상품"/"작품" 탭, 무한 스크롤, "작품" 탭 작품 단위/개별
    찜 해제, "상품" 탭 편집 모드(전체선택/개별선택/선택삭제 확인 팝업/편집취소))
  - `MyStorePage`(`/my` — 찜 메뉴 뱃지, "찜한 상품"/"최근 본 상품" 섹션 찜 상태 동기화;
    Phase 1에서 만든 최소 버전을 이 Phase에서 완성)
  - 진입점 최소 Page Object: 메인페이지 상품 카드의 찜 아이콘(TC-002/003), 로그인 유도
    팝업 및 라프텔 로그인 페이지 진입 확인(비로그인 분기, TC-021~032)
- **선행 조건(의존 Feature)**: Phase 1(찜 토글 UI/API 동작 개념 재사용), 로그인(고정 계정).
  카트/주문(Phase 2, 3)과는 기능적으로 독립적이다.
- **우선순위 근거**: Product Detail 이후 착수 가능한 Feature 중 Approved TC 건수(28건)와
  Business Criticality가 높은(BC 5) TC 비중(TC-WISHLIST-009/024/031/032)이 검색(다음
  Phase, BC 최대 4)보다 많아 우선 배치했다. **다만 찜과 검색 사이에는 강제적인 기능
  의존관계가 없으므로, 이 순서는 우선순위 판단이며 사용자가 다른 순서를 원하면 조정
  가능하다.**
- **리스크**: TC-WISHLIST-031/032는 실제 라프텔 로그인 완료 처리가 필요한 리디렉션
  검증으로, Candidate 문서에서 이미 외부 인증 연동에 따른 Maintenance Cost 리스크로
  안내되었다 — 구현 전 안정적인 로그인 자동화 방식(고정 계정 이메일 로그인) 확보가
  필요하다.

### Phase 5: 검색(search) 자동화 구현

- **대상 TC**: 23건 — TC-SEARCH-001, 002, 003, 006, 007, 008, 009, 010, 011, 012, 013, 014,
  015, 016, 019, 020, 021, 022, 023, 024, 025, 026, 027
- **필요 Page Object**
  - `SearchPage`(`/search` 초기 화면, 자동완성/추천 검색어, 최근 검색어 조회/개별·전체 삭제,
    "취소"/"뒤로가기")
  - `SearchResultPage`(검색 결과 화면 — 상단 작품 카드, "총 N개", 정렬 드롭다운, 2열 그리드)
  - `IpPage`(`/ip/{id}` 작품 페이지, TC-006/010 진입 확인용)
- **선행 조건(의존 Feature)**: Phase 1 `ProductDetailPage` — TC-SEARCH-013/014는 "판매종료"/
  "품절" 상품 클릭 후 상품상세 진입 및 상태별 버튼을 검증하므로, Phase 1에서 구현한
  `ProductDetailPage`의 상태별 버튼 로직을 재사용한다.
- **우선순위 근거**: 검색 자체는 대부분 `/search` 직접 진입으로 독립적으로 테스트 가능해
  다른 Feature와의 의존성이 낮지만, 위 2개 TC가 상품상세 Page Object를 재사용하므로
  Phase 1 이후로 배치해 순방향 의존성만 갖도록 했다(카트/주문/찜과는 의존관계 없음).

### Phase Final: CI/CD 및 Slack 알림 연동

- **산출물**: `.github/workflows/` 자동화 테스트 실행 워크플로우(Push 트리거), 실패 시
  Slack 알림 스크립트(JUnit XML 파싱 → 실패 테스트명/사유 요약 포함)
- **근거**: AUTOMATION_GUIDE 16절
- **착수 직전 조건**: AUTOMATION_GUIDE 20.1절에 따라, 모든 Feature Phase(1~5) 코드 작성이
  끝난 뒤 전체 통합테스트(Full Regression)를 1회 수행하고 결과를 확인한 다음 착수한다.

## 6. Feature별 상세 매핑표

| Feature | 확정 TC 수 | 대상 TC ID | 필요 Page Object | 의존 Feature | Phase |
|---|---|---|---|---|---|
| product-detail | 34 (TC-PRODUCT-DETAIL-008 제외) | TC-PRODUCT-DETAIL-002,003,004,005,006,007,010,011,012,013,014,015,019,020,024,025,026,027,028,031,032,033,034,035,036,037,038,039,040,042,043,044,045,046 | ProductDetailPage, ProductInfoPage, ExchangeReturnInfoPage, SellerInfoPage, NoticePage, RelatedProductsPage, NotFoundPage, (최소)MyStorePage, (최소)카트/찜 내비게이션 | 없음(로그인만 필요) | Phase 1 |
| cart | 16 | TC-CART-001,002,007,008,009,010,012,013,014,015,016,018,019,020,022,023 | CartPage | product-detail(담기 액션) | Phase 2 |
| order | 11 | TC-ORDER-001,002,004,005,007,009,015,017,018,019,020 | CheckoutPage | product-detail(바로구매) + cart(구매하기) | Phase 3 |
| wishlist | 28 | TC-WISHLIST-001,002,003,004,005,006,007,008,009,012,014,015,016,017,020,021,022,023,024,025,026,027,028,029,030,031,032,033 | WishlistPage, MyStorePage(완성), 메인 진입점 최소 Page Object, 로그인 유도 팝업 컴포넌트 | product-detail(찜 토글 개념) | Phase 4 |
| search | 23 | TC-SEARCH-001,002,003,006,007,008,009,010,011,012,013,014,015,016,019,020,021,022,023,024,025,026,027 | SearchPage, SearchResultPage, IpPage | product-detail(상태별 버튼 검증 재사용, 2건) | Phase 5 |

## 7. Definition of Done

- AUTOMATION_GUIDE 20절(테스트 실행/검증) 기준: Phase 내부 코드 작성 단위마다 즉시 실행,
  Phase 완료 시 해당 Phase 테스트 파일 전체 실행(PASSED/FAILED/ERROR 확인), 전체 Feature
  Phase 완료 후 Phase Final 착수 직전 1회 전체 통합테스트 수행
- AUTOMATION_GUIDE 21절 Self Review 체크리스트 충족(Wait 처리, Locator 규칙, Page/Test
  책임 분리, 계정 정보 비하드코딩, 로깅, 예외 처리, 네이밍 컨벤션 등)
- 코드 리뷰 완료(CLAUDE.md 3절 워크플로우 7단계)
- 각 Phase 착수 전, 해당 Phase가 의존하는 이전 Phase의 Page Object가 실제로 구현·검증
  완료되어 있는지 확인

## 8. 리스크 및 확인 필요 사항

| 구분 | 내용 |
|---|---|
| 해결됨 — TC-PRODUCT-DETAIL-008 제외 | TC-PRODUCT-DETAIL-008(주문내역에서 진입)은 "내 스토어 > 주문내역(`/orders`)"에 완료된 주문이 존재해야 하는데, AUTOMATION_GUIDE 11.2절 및 Order Feature PRD 범위상 자동화 테스트가 실제 결제를 완료하는 일은 없어 고정 계정에 데이터를 안정적으로 준비할 수 없었다. **사용자 결정에 따라 이번 Roadmap의 자동화 구현 범위에서 제외**(1절 Out of Scope 반영, Phase 1 대상 TC 35건 → 34건). |
| 해결됨 — Candidate 문서 재확정 완료 | Candidate 문서/Google Sheet 재확정 완료(TC-PRODUCT-DETAIL-008 QA Decision: Approved → Hold 반영됨, `docs/tc/automation-candidates/product-detail.md` 2026-09-05 갱신). Candidate 문서의 Approved TC 목록(34건)이 이 Roadmap의 Phase 1 대상 TC 목록과 정확히 일치함을 확인했다. |
| 구현 순서 참고 | TC-PRODUCT-DETAIL-004(찜 목록에서 진입), TC-PRODUCT-DETAIL-005(카트에서 진입)는 Phase 1 시점에 Cart/Wishlist 전체 기능이 아직 없으므로, 전제 조건(상품 1개 담기/찜하기)을 위한 최소 동작만 Phase 1에서 임시 구현한다. Phase 2/4 착수 시 이 임시 코드를 재사용하거나 정리해 중복 구현(CLAUDE.md 12절)이 발생하지 않도록 해야 한다. |
| 외부 인증 연동 리스크 | TC-WISHLIST-031/032는 실제 라프텔 로그인 완료 처리가 필요한 리디렉션 검증이다(Candidate 문서에서 이미 Maintenance Cost 리스크로 안내됨). 안정적인 로그인 자동화 방안이 Phase 4 착수 전 준비되어야 한다. |
| 테스트 데이터 미확정 | 로그인 필요 TC(Phase 1부터 존재)를 위한 고정 계정 정보(이메일 개수, 비밀번호)가 아직 확정되지 않았다. AUTOMATION_GUIDE 11.1절에 따라 구현 착수 시점(Phase 0~1 사이)에 사용자로부터 전달받아야 한다. |
| 순서 판단(강제 아님) | Phase 4(찜)를 Phase 5(검색)보다 먼저 배치한 것은 기능적 의존관계가 아니라 Approved TC 건수/Business Criticality 비교에 따른 우선순위 판단이다. 사용자가 다른 순서(예: 검색을 찜보다 먼저)를 선호하면 의존관계를 해치지 않는 범위에서 조정 가능하다. |
| 해결됨(자동화 보류로 확정) — PG 결제 관련 | TC-ORDER-019(PG 결제창 진입까지만 확인, 실제 결제 미수행)를 Phase 3 구현 시점에 실측한 결과, 나이스페이 결제창이 동일 입력에도 간헐적으로만 노출되어(반복 재현 시도 중 매번 나타나지 않음) 안정적인 자동화가 불가능함을 확인했다. 실제 PG(나이스페이) 엔드포인트를 반복 호출하는 것 자체도 프로덕션 결제 게이트웨이에 대한 부작용 리스크가 있어, **사용자 결정에 따라 TC-ORDER-019는 자동화 보류로 확정**(AUTOMATION_GUIDE 7.9절 참고). Phase 3 자동화 대상은 10건(001,002,004,005,007,009,015,017,018,020)으로 조정. 이후 구현 중 계정에 저장된 배송지가 자동으로 채워지는 정상 기능을 신규 발견해 REQ-ORDER-019/TC-ORDER-021로 문서화·승인·자동화 대상 확정(Approved)까지 완료해 Phase 3 자동화 대상은 최종 11건(001,002,004,005,007,009,015,017,018,020,021)이 되었다(AUTOMATION_GUIDE 7.10절 참고). |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 최초 작성 — product-detail/cart/order/wishlist/search 5개 Feature의 Approved TC(합계 113건)를 대상으로 Phase 0(공통 기반) → Phase 1(상품상세) → Phase 2(카트) → Phase 3(주문) → Phase 4(찜) → Phase 5(검색) → Phase Final(CI/CD) 순서의 초안 작성 | 초안 |
| 2026-09-05 | 사용자 결정에 따라 TC-PRODUCT-DETAIL-008(주문내역에서 상품상세 진입)을 검증 범위에서 제외 — Phase 1 대상 TC 35건→34건, 합계 113건→112건으로 갱신, 1절 Out of Scope 추가, 8절 리스크 항목을 "해결됨"으로 갱신하고 Candidate 문서 QA Decision 불일치를 별도 미해결 항목으로 추가 | 초안 |
| 2026-09-05 | 사용자 최종 승인("네, 승인") — TC-PRODUCT-DETAIL-008 제외 반영 버전을 최종 확정 | 승인완료 |
| 2026-09-05 | 8절 TC-PRODUCT-DETAIL-008 관련 리스크 항목을 Candidate 문서 재확정 완료 상태에 맞게 갱신 (재승인) | 승인완료 |
| 2026-09-05 | Phase 3(order) 구현 중 TC-ORDER-019(PG 결제창 진입)가 나이스페이 결제창의 간헐적 노출로 안정적 자동화가 불가능함을 실측 확인. 사용자 결정에 따라 자동화 보류로 확정하고 8절 리스크 항목을 갱신, Phase 3 자동화 대상을 11건→10건으로 조정 (사용자 승인) | 승인완료 |
| 2026-09-06 | Phase 3(order) 구현 중 계정에 저장된 배송지가 자동으로 채워지는 신규 기능을 발견, REQ-ORDER-019/TC-ORDER-021로 문서화 및 자동화 대상 확정(Approved)까지 완료. Phase 3 자동화 대상을 10건→11건(TC-ORDER-021 추가)으로 갱신 (사용자 승인) | 승인완료 |
| 2026-09-06 | Phase Final(CI/CD 및 Slack 알림 연동) 구현 완료. GitHub 호스팅 러너가 store.laftel.net의 한국 IP 제한으로 접근 불가함을 실측 확인해 한국 소재 self-hosted 러너로 전환. 4회의 실제 CI 검증을 통해 headless 다이얼로그 버그, Google 헤드리스 로그인 차단, 일반 타이밍 플레이키를 발견·수정·문서화함. 최종 110/113 통과, Slack 성공/실패 알림 다회 실증 확인 (사용자 승인) | 승인완료 |
| 2026-09-07 | 로케이터를 Page 클래스에서 전용 Locators 클래스로 분리하는 리팩토링(AUTOMATION_GUIDE.md 2/3/4.1/6.2/18/21절 개정)에 맞춰 3절 디렉터리 구조 목록에 `locators` 추가 (사용자 승인) | 승인완료 |
