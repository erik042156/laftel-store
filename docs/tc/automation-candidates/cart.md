---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/cart.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-09-05
관련 Feature PRD: feature/prd-cart.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
최근 Sheet 동기화일: 2026-09-05
확정일: 2026-09-05
---

# Automation Candidate 평가 - 카트

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-CART-001 | 3 | 5 | 4 | 5 | 2 | 2 | 23 | Yes | 담기 시 토스트/뱃지는 매 릴리즈 반복 검증되는 핵심 피드백이며 DOM/텍스트로 결정적 판정 가능, 유지비용 낮음 |
| TC-CART-002 | 2 | 4 | 5 | 5 | 1 | 1 | 22 | Yes | 단순하고 안정적인 진입 경로 2개(아이콘/URL), 수행·유지 비용 매우 낮음 |
| TC-CART-003 | 1 | 3 | 5 | 5 | 1 | 1 | 20 | Hold | 순수 정적 UI(타이틀/뒤로가기) 노출 확인으로 Business Criticality가 낮음(4.2절 단순 UI 노출 후순위 신호). 단독 자동화보다 다른 E2E Flow에 포함 검토 권장 |
| TC-CART-004 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 전체선택/삭제 버튼 노출 확인으로 정적 성격, Business Criticality 낮아 단독 자동화 ROI 낮음 |
| TC-CART-005 | 2 | 3 | 4 | 4 | 2 | 3 | 18 | Hold | 판매자 그룹 나열 노출 확인, 정적 성격이며 그룹 구조 변경 시 유지비용 소폭 발생 |
| TC-CART-006 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | 카드 내 다수 하위요소(이미지/옵션텍스트 형식 등)를 모두 검증해야 해 Result Determinism과 안정성이 상대적으로 낮고 유지비용 존재 |
| TC-CART-007 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 선택 건수에 따른 배송비 문구 조건 분기, 결제 신뢰성과 연결되어 회귀 가치 높음 |
| TC-CART-008 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | TC-CART-007과 짝을 이루는 조건 분기(1건 vs 2건 이상), 동일 근거로 자동화 대상 |
| TC-CART-009 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 결제금액 섹션(합산 금액)은 사용자 신뢰와 직결되는 핵심 정보, 매 릴리즈 반복 검증 필요 |
| TC-CART-010 | 3 | 5 | 4 | 5 | 2 | 2 | 23 | Yes | 하단 고정 구매 버튼 금액/개수 표시는 결제 진입 직전 핵심 정보로 반복 검증 가치 높음 |
| TC-CART-011 | 2 | 3 | 4 | 5 | 1 | 1 | 20 | Yes | Negative 확인이나 검증 비용이 매우 낮고 결정적이라 낮은 비용 대비 자동화 편입 가치 있음 |
| TC-CART-012 | 4 | 5 | 4 | 5 | 2 | 3 | 23 | Yes | 개별 체크 시 상단/하단 즉시 갱신은 결제금액 계산에 직접 영향을 주는 핵심 상태 연동 로직 |
| TC-CART-013 | 3 | 4 | 4 | 5 | 2 | 3 | 21 | Yes | 판매자 그룹 단위 토글은 3단계 선택 상태 연동 로직의 일부로 결함 가능성 있는 핵심 동작 |
| TC-CART-014 | 3 | 5 | 4 | 5 | 2 | 3 | 22 | Yes | 전체선택 토글도 동일한 3단계 선택 연동 로직의 핵심 축 |
| TC-CART-015 | 5 | 5 | 4 | 5 | 3 | 3 | 25 | Yes | 수량 변경에 따른 실시간 금액 갱신은 결제 정확성과 직결되는 최우선 자동화 대상 |
| TC-CART-016 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 최소 수량 경계값(Boundary) 처리, 결과가 명확해 자동 판정 용이 |
| TC-CART-017 | 3 | 3 | 3 | 4 | 4 | 4 | 19 | Hold | 특정 상품(products=1929/742)의 실제 재고 상한값에 강하게 의존하는 테스트 데이터라, 상품 데이터가 변경되면 테스트가 깨질 위험이 커 유지보수 비용이 높음. 안정적인 테스트 전용 재고 데이터 확보 후 재검토 권장 |
| TC-CART-018 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 확인 팝업을 거치는 개별 삭제 흐름, 결과 판정이 명확하고 반복 검증 가치 있음 |
| TC-CART-019 | 2 | 3 | 4 | 5 | 1 | 1 | 20 | Yes | 삭제 취소 시 미삭제 확인, 비용이 매우 낮고 TC-CART-018과 짝을 이루는 보완 케이스 |
| TC-CART-020 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 상단 일괄 삭제, 확인 팝업을 거치는 안전한 데이터 변경 흐름으로 자동 판정 용이 |
| TC-CART-021 | 2 | 2 | 4 | 5 | 1 | 1 | 19 | Hold | 검증 범위가 팝업 노출까지로 제한적(PRD상 삭제 이후 동작 미확인)이라 실질 회귀 커버리지가 낮음 |
| TC-CART-022 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 빈 장바구니 상태 확인, 준비 비용 낮고 결정적으로 판정 가능한 경계 상태 |
| TC-CART-023 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 선택 0건 상태에서의 구매 진행 차단 가드, 결제 오진입 방지 로직으로 회귀 가치 있음 |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-CART-001 | Approved |  |
| TC-CART-002 | Approved |  |
| TC-CART-003 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-CART-004 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-CART-005 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-CART-006 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-CART-007 | Approved | UI 확인요소이긴 하나,<br>배송비 문구 및 결제 신뢰성과 연결되어 승인 |
| TC-CART-008 | Approved | 위와 동일 이유 |
| TC-CART-009 | Approved |  |
| TC-CART-010 | Approved |  |
| TC-CART-011 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-CART-012 | Approved | UI 확인요소이긴 하나,<br>배송비 문구 및 결제 신뢰성과 연결되어 승인 |
| TC-CART-013 | Approved |  |
| TC-CART-014 | Approved |  |
| TC-CART-015 | Approved |  |
| TC-CART-016 | Approved |  |
| TC-CART-017 | Hold | 어드민에서 상품 재고 수량에 관하여 셋팅 후 확인 필요하기 때문에,<br>현재 어드민 관련 요건이 완벽하게 적용되지 않은 상태이므로 보류 |
| TC-CART-018 | Approved |  |
| TC-CART-019 | Approved |  |
| TC-CART-020 | Approved |  |
| TC-CART-021 | Hold |  |
| TC-CART-022 | Approved |  |
| TC-CART-023 | Approved |  |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다.

## Hard Rule 적용 / Validation 특이사항

- 결함을 정상 Expected Result처럼 고정한 TC(Hard Rule 대상)는 발견되지 않았습니다.
- TC-CART-017은 Hard Rule 대상은 아니지만, 실제 상품(products=1929/742)의 재고 상한값에
  의존하는 테스트 데이터 특성상 Maintenance Cost가 높아 Hold로 판정했으며, QA Decision도
  동일하게 Hold로 확인되었습니다.
- 자동화 대상 확정 시점 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태,
  원본 TC 변경 여부) 결과 문제가 발견되지 않아 확정을 진행했습니다.

## Approved TC 목록 (자동화 대상 확정)

- 확정일: 2026-09-05
- Approved 16건: TC-CART-001, TC-CART-002, TC-CART-007, TC-CART-008, TC-CART-009,
  TC-CART-010, TC-CART-012, TC-CART-013, TC-CART-014, TC-CART-015, TC-CART-016,
  TC-CART-018, TC-CART-019, TC-CART-020, TC-CART-022, TC-CART-023
- Hold(미확정) 7건: TC-CART-003, TC-CART-004, TC-CART-005, TC-CART-006, TC-CART-011,
  TC-CART-017, TC-CART-021
- Rejected 0건

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 승인완료 TC 문서(docs/tc/cart.md, 23건) 기반 최초 자동화 후보 평가 | 평가중 |
| 2026-09-05 | Google Sheet QA Decision/QA Comment 재조회 및 반영 | 사용자검토완료 |
| 2026-09-05 | 사용자의 자동화 대상 확정 요청에 따라 Validation 수행(문제 없음), Approved 16건/Hold 7건/Rejected 0건 확정 | 자동화대상확정 |
