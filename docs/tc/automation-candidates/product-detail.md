---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/product-detail.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-09-05
관련 Feature PRD: feature/prd-product-detail.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
최근 Sheet 동기화일: 2026-09-05
확정일: 2026-09-05
---

# Automation Candidate 평가 - 상품상세

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-DETAIL-001 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 메인 배너를 통한 진입, 대체 경로 다수 존재해 단독 자동화 우선순위 낮음 |
| TC-PRODUCT-DETAIL-002 | 2 | 4 | 4 | 5 | 1 | 2 | 20 | Yes | 메인 상품리스트를 통한 진입, 가장 빈번히 사용되는 핵심 경로 |
| TC-PRODUCT-DETAIL-003 | 2 | 3 | 3 | 5 | 3 | 3 | 19 | Hold | 3개 섹션(찜/최근본/추천)을 한 TC에서 확인, 준비 조건이 복합적이라 비용이 다소 있음 |
| TC-PRODUCT-DETAIL-004 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 찜 목록에서의 진입 경로, 준비 조건이 단순함 |
| TC-PRODUCT-DETAIL-005 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 장바구니 상품 클릭 진입, 준비 조건 단순 |
| TC-PRODUCT-DETAIL-006 | 2 | 4 | 5 | 5 | 1 | 1 | 22 | Yes | URL 직접 진입, 매우 안정적이고 저비용 |
| TC-PRODUCT-DETAIL-007 | 4 | 4 | 5 | 5 | 1 | 1 | 24 | Yes | 404 에러 페이지 처리 실패 시 사용자가 완전히 막힐 수 있어 영향이 크고, 자동화 비용은 낮음 |
| TC-PRODUCT-DETAIL-008 | 2 | 3 | 4 | 5 | 3 | 2 | 21 | Yes | 주문내역에서의 진입, 주문 데이터 준비가 필요하나 회귀 가치 있음 |
| TC-PRODUCT-DETAIL-009 | 1 | 3 | 5 | 5 | 1 | 1 | 20 | Hold | 상단 바 아이콘 구성 정적 확인, Business Criticality 낮음 |
| TC-PRODUCT-DETAIL-010 | 2 | 4 | 5 | 5 | 1 | 1 | 22 | Yes | 검색 아이콘 클릭 이동, 단순하고 안정적 |
| TC-PRODUCT-DETAIL-011 | 2 | 4 | 5 | 5 | 1 | 1 | 22 | Yes | 장바구니 아이콘 클릭 이동(파라미터 포함 URL), 단순하고 안정적 |
| TC-PRODUCT-DETAIL-012 | 2 | 3 | 5 | 5 | 1 | 1 | 21 | Yes | 뒤로가기 복귀, 단순 네비게이션 |
| TC-PRODUCT-DETAIL-013 | 3 | 4 | 4 | 4 | 3 | 3 | 21 | Yes | 이미지 캐러셀 순환 구조 및 페이지네이션 갱신, 구매 결정에 영향을 주는 기능으로 로직 복잡도 있어 회귀 가치 높음 |
| TC-PRODUCT-DETAIL-014 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 작품명 링크 이동, 단순 정적 네비게이션 |
| TC-PRODUCT-DETAIL-015 | 3 | 4 | 4 | 5 | 1 | 2 | 21 | Yes | 상품명/가격 노출, 가격 표시 정확성은 구매 신뢰와 연결되어 회귀 가치 있음 |
| TC-PRODUCT-DETAIL-016 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 배송정보 섹션 정적 노출 확인 |
| TC-PRODUCT-DETAIL-017 | 1 | 2 | 4 | 5 | 1 | 1 | 18 | Hold | 안내 팝업 노출, Business Criticality 낮은 부가 정보성 팝업 |
| TC-PRODUCT-DETAIL-018 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | 추천 캐러셀 카드 구성, 실패해도 핵심 구매 플로우 영향 제한적 |
| TC-PRODUCT-DETAIL-019 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 추천 캐러셀 카드 클릭 이동, 부가 기능 성격 |
| TC-PRODUCT-DETAIL-020 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 더보기 클릭 이동, 부가 기능 성격 |
| TC-PRODUCT-DETAIL-021 | 1 | 3 | 4 | 5 | 1 | 1 | 19 | Hold | 상세정보 탭 기본 노출, 정적 성격 |
| TC-PRODUCT-DETAIL-022 | 2 | 3 | 3 | 5 | 2 | 3 | 18 | Hold | 정품 안내/예약 상품 최소 수량 미충족 시 주문 취소 가능 안내/연령 제한 안내 3개 항목이 설정된 특정 상품 사례를 기준으로, 설정값과 실제 노출 내용이 일치하는지 확인하는 단순 콘텐츠 렌더링 검증(REQ-PRODUCT-DETAIL-024 재해석으로 "일반 상품" 유형 전제는 제거되었으나 검증 성격 자체는 동일해 축 점수 유지). Business Criticality가 중간 이하(정보성 안내)라 Hold로 유지 |
| TC-PRODUCT-DETAIL-023 | 4 | 3 | 4 | 5 | 2 | 4 | 20 | Yes | 교환·환불 불가라는 구매 정책과 직결된 경고성 강조 문구로 누락/왜곡 시 소비자 분쟁으로 이어질 수 있어 Business Criticality는 4로 유지. REQ-PRODUCT-DETAIL-024 재해석에 따라 상품 유형별 시스템 분기가 아닌 상품별 어드민 개별 설정으로 확인되어, 요구사항/UI 구조 자체는 단순 콘텐츠 렌더링에 가까워짐(Automation Stability 3→4). 다만 유형 기반으로 대체 가능한 테스트 데이터를 찾을 수 없고 특정 상품 1건의 어드민 설정에만 의존해야 하며, 해당 설정이 사전 통지 없이 변경/해제될 경우 테스트가 깨질 위험이 있어 Maintenance Cost를 3→4로 상향(두 축 변동이 상쇄되어 Automation Score는 20으로 동일). Business Criticality가 높아 Yes는 유지하되, 자동화 구현 시 기준 상품(테스트 픽스처) 관리가 성패를 좌우하므로 유지보수 리스크로 별도 명시 |
| TC-PRODUCT-DETAIL-024 | 1 | 3 | 4 | 5 | 1 | 1 | 19 | Hold | 상세정보 더보기 토글, 단순 UI 상호작용 |
| TC-PRODUCT-DETAIL-025 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 상품정보 제공고시 페이지 이동/내용, 법적 표시 정보 정확성 |
| TC-PRODUCT-DETAIL-026 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 교환/반품 안내, 소비자 정책 정보로 정확성 중요 |
| TC-PRODUCT-DETAIL-027 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 판매자 정보 페이지 이동, Business Criticality 낮음 |
| TC-PRODUCT-DETAIL-028 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 유의사항 페이지(배송/취소·환불 정책) 정보 정확성 |
| TC-PRODUCT-DETAIL-029 | 1 | 2 | 5 | 5 | 1 | 1 | 19 | Hold | 공통 푸터 노출, 정적이고 Business Criticality 매우 낮음 |
| TC-PRODUCT-DETAIL-030 | 2 | 3 | 4 | 4 | 1 | 2 | 18 | Hold | 하단 고정 영역 스크롤 무관 노출, 단순 레이아웃 확인 |
| TC-PRODUCT-DETAIL-031 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 비로그인 찜 클릭 시 로그인 유도, 로그인 상태 분기 로직으로 회귀 가치 있음 |
| TC-PRODUCT-DETAIL-032 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 찜 추가 처리, 개인화 데이터 정확성이 핵심인 반복 검증 대상 |
| TC-PRODUCT-DETAIL-033 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 찜 해제 토글, 찜 추가와 짝을 이루는 핵심 동작 |
| TC-PRODUCT-DETAIL-034 | 3 | 4 | 3 | 5 | 2 | 3 | 20 | Yes | 캐러셀 카드 위 찜 처리(제자리 갱신), 상세페이지 이동 없는 인터랙션이라 회귀 가치 있음 |
| TC-PRODUCT-DETAIL-035 | 4 | 5 | 4 | 5 | 2 | 3 | 23 | Yes | 구매하기 클릭 시 하단 확장 영역 노출, 구매 플로우 진입점으로 핵심 |
| TC-PRODUCT-DETAIL-036 | 4 | 5 | 4 | 5 | 3 | 3 | 24 | Yes | 옵션 드롭다운 및 품절 옵션 비활성화, 잘못된 옵션 선택 방지에 직결되는 핵심 로직 |
| TC-PRODUCT-DETAIL-037 | 4 | 5 | 4 | 5 | 3 | 3 | 24 | Yes | 옵션 선택 후 금액 갱신, 결제 정확성과 직결 |
| TC-PRODUCT-DETAIL-038 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 옵션 없는 상품의 수량선택 단계, 구매 플로우 핵심 |
| TC-PRODUCT-DETAIL-039 | 3 | 4 | 4 | 5 | 1 | 2 | 21 | Yes | 최소 수량 경계값(Boundary), 결과 판정 명확 |
| TC-PRODUCT-DETAIL-040 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 판매중 상품 버튼 상태, 4가지 상태 분기 중 하나로 회귀 가치 있음 |
| TC-PRODUCT-DETAIL-041 | 3 | 3 | 3 | 3 | 3 | 4 | 17 | Hold | 실시간 카운트다운 표시는 타이밍 의존적이라 자동화 시 Flaky 위험이 크고 유지비용이 높음 |
| TC-PRODUCT-DETAIL-042 | 3 | 4 | 4 | 5 | 3 | 3 | 22 | Yes | 품절 상태 버튼/찜아이콘 상태, 상태 분기 검증 |
| TC-PRODUCT-DETAIL-043 | 3 | 4 | 4 | 5 | 3 | 3 | 22 | Yes | 판매종료 상태 버튼/찜아이콘 상태, 상태 분기 검증 |
| TC-PRODUCT-DETAIL-044 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 비활성 버튼 무반응(Negative), 결과가 명확하고 비용 낮음 |
| TC-PRODUCT-DETAIL-045 | 2 | 3 | 3 | 4 | 3 | 3 | 18 | Hold | 최근 본 상품 자동 기록, 여러 화면을 오가야 하는 검증이라 준비/유지 비용이 다소 있고 부가 기능 성격 |
| TC-PRODUCT-DETAIL-046 | 3 | 4 | 4 | 5 | 3 | 3 | 22 | Yes | 품절 옵션 선택 차단(Negative), REQ-PRODUCT-DETAIL-036 요구사항 준수 여부를 직접 검증하는 핵심 가드 |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-PRODUCT-DETAIL-001 | Hold |  |
| TC-PRODUCT-DETAIL-002 | Approved |  |
| TC-PRODUCT-DETAIL-003 | Approved |  |
| TC-PRODUCT-DETAIL-004 | Approved |  |
| TC-PRODUCT-DETAIL-005 | Approved |  |
| TC-PRODUCT-DETAIL-006 | Approved |  |
| TC-PRODUCT-DETAIL-007 | Approved | 현재 product2의 경우에는 존재하지 않는 상품이지만,<br>추후 노출시 존재하는 상품으로 변경되어 위험 있음 |
| TC-PRODUCT-DETAIL-008 | Hold |  |
| TC-PRODUCT-DETAIL-009 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-010 | Approved |  |
| TC-PRODUCT-DETAIL-011 | Approved |  |
| TC-PRODUCT-DETAIL-012 | Approved |  |
| TC-PRODUCT-DETAIL-013 | Approved |  |
| TC-PRODUCT-DETAIL-014 | Approved |  |
| TC-PRODUCT-DETAIL-015 | Approved |  |
| TC-PRODUCT-DETAIL-016 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-017 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-018 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-019 | Approved |  |
| TC-PRODUCT-DETAIL-020 | Approved |  |
| TC-PRODUCT-DETAIL-021 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-022 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-023 | Hold | 어드민 제어 요소로 추정되어 현 단계에서는 자동화 보류 |
| TC-PRODUCT-DETAIL-024 | Approved |  |
| TC-PRODUCT-DETAIL-025 | Approved |  |
| TC-PRODUCT-DETAIL-026 | Approved |  |
| TC-PRODUCT-DETAIL-027 | Approved |  |
| TC-PRODUCT-DETAIL-028 | Approved |  |
| TC-PRODUCT-DETAIL-029 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-030 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-PRODUCT-DETAIL-031 | Approved |  |
| TC-PRODUCT-DETAIL-032 | Approved |  |
| TC-PRODUCT-DETAIL-033 | Approved |  |
| TC-PRODUCT-DETAIL-034 | Approved |  |
| TC-PRODUCT-DETAIL-035 | Approved |  |
| TC-PRODUCT-DETAIL-036 | Approved |  |
| TC-PRODUCT-DETAIL-037 | Approved |  |
| TC-PRODUCT-DETAIL-038 | Approved |  |
| TC-PRODUCT-DETAIL-039 | Approved |  |
| TC-PRODUCT-DETAIL-040 | Approved |  |
| TC-PRODUCT-DETAIL-041 | Rejected |  |
| TC-PRODUCT-DETAIL-042 | Approved |  |
| TC-PRODUCT-DETAIL-043 | Approved |  |
| TC-PRODUCT-DETAIL-044 | Approved |  |
| TC-PRODUCT-DETAIL-045 | Approved |  |
| TC-PRODUCT-DETAIL-046 | Approved |  |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다.

## Hard Rule 적용 / Validation 특이사항

- 결함을 정상 Expected Result처럼 고정한 TC(Hard Rule 대상)는 발견되지 않았습니다.
- TC-PRODUCT-DETAIL-041(예약구매 카운트다운)은 실시간 타이머 의존으로 자동화 시 Flaky
  위험이 커 Hold로 판정했습니다.
- TC-PRODUCT-DETAIL-023: REQ-PRODUCT-DETAIL-024 재해석(상품 유형별 시스템 분기가 아닌
  상품별 어드민 개별 설정)에 따라 대체 불가능한 단일 상품(테스트 픽스처)에 의존하는
  유지보수 리스크가 있음을 별도로 기록합니다. Candidate(AI)는 Yes였으나, QA Decision은
  "어드민 제어 요소로 추정되어 현 단계에서는 자동화 보류"라는 사유로 Hold로 결정되었습니다
  (QA Decision이 AI Candidate보다 우선하므로 그대로 반영, 미확정 유지).
- 자동화 대상 확정 시점 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태,
  원본 TC 변경 여부) 결과 문제가 발견되지 않아 확정을 진행했습니다. 특히 TC-PRODUCT-DETAIL-022,
  023은 재평가 이후 원본 TC 문서가 추가로 변경되지 않았음을 확인했습니다(원본 TC 문서 최근
  변경일 2026-09-05로 이 평가 시점과 일치).
- TC-PRODUCT-DETAIL-008: 사용자가 Google Sheet에서 QA Decision을 Approved에서 Hold로
  직접 변경함에 따라 재조회 및 Validation을 다시 수행했습니다(TC ID 유효성/중복 없음, 46건
  QA Decision 모두 Approved/Hold/Rejected 중 하나로 정상값이며 미검토(빈 값) 없음, 원본 TC
  문서 상태 승인완료 유지, 원본 TC 문서 최근 변경일 2026-09-05로 이 평가 시점과 일치해 변경
  없음 확인). Candidate(AI)는 Yes였으나, "내 스토어 > 주문내역에서 상품상세 진입" 시나리오는
  자동화가 실제 결제를 완료하지 않는 정책상 고정 계정에 사전 완료된 주문 데이터를 안정적으로
  준비할 수 없어 사용자가 검증 범위에서 제외하기로 결정했습니다(QA Decision이 AI Candidate
  보다 우선하므로 그대로 반영, 미확정 유지).

## Approved TC 목록 (자동화 대상 확정)

- 확정일: 2026-09-05 (최초 확정) / 2026-09-05 (Sheet QA Decision 변경 반영 갱신)
- Approved 34건: TC-PRODUCT-DETAIL-002, 003, 004, 005, 006, 007, 010, 011, 012, 013,
  014, 015, 019, 020, 024, 025, 026, 027, 028, 031, 032, 033, 034, 035, 036, 037, 038, 039,
  040, 042, 043, 044, 045, 046
- Hold(미확정) 11건: TC-PRODUCT-DETAIL-001, 008, 009, 016, 017, 018, 021, 022, 023, 029, 030
- Rejected 1건: TC-PRODUCT-DETAIL-041

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 승인완료 TC 문서(docs/tc/product-detail.md, 46건) 기반 최초 자동화 후보 평가 | 평가중 |
| 2026-09-05 | 원본 TC 재승인(TC-PRODUCT-DETAIL-022, 023의 Precondition/Expected Result를 "상품 유형" 기준에서 "특정 상품 사례" 기준으로 수정, REQ-PRODUCT-DETAIL-024 재해석 반영)에 따라 TC-PRODUCT-DETAIL-022, 023만 재평가. 022는 사유 문구만 재작성(축 점수 변동 없음). 023은 "유형별 시스템 분기 없음"이 확인됨에 따라 Automation Stability 3→4, Maintenance Cost 3→4(단일 상품 픽스처 의존 리스크)로 조정, 두 축이 상쇄되어 Automation Score는 20으로 동일, Candidate(AI)는 Yes 유지. 다른 TC(001~021, 024~046)는 원본 미변경으로 재평가 대상에서 제외 | 평가중 |
| 2026-09-05 | Google Sheet QA Decision/QA Comment 재조회 및 반영 | 사용자검토완료 |
| 2026-09-05 | 사용자의 자동화 대상 확정 요청에 따라 Validation 수행(문제 없음), Approved 35건/Hold 10건/Rejected 1건 확정 | 자동화대상확정 |
| 2026-09-05 | Google Sheet QA Decision 변경 반영: TC-PRODUCT-DETAIL-008 Approved→Hold(주문내역 진입 데이터 준비 제약으로 사용자가 검증 범위에서 제외 결정) | 자동화대상확정 |
