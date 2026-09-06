---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/order.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-09-06
관련 Feature PRD: feature/prd-order.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-09-05
최근 변경일: 2026-09-06
최근 Sheet 동기화일: 2026-09-05
확정일: 2026-09-06
---

# Automation Candidate 평가 - 주문

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-ORDER-001 | 5 | 5 | 4 | 5 | 3 | 3 | 25 | Yes | "바로구매" 통한 주문/결제 진입은 결제 자체를 여는 핵심 게이트, 매출 직결 |
| TC-ORDER-002 | 5 | 5 | 4 | 5 | 3 | 3 | 25 | Yes | 장바구니 구매하기 통한 진입 경로, TC-ORDER-001과 함께 핵심 게이트 |
| TC-ORDER-003 | 1 | 3 | 5 | 5 | 1 | 1 | 20 | Hold | 순수 정적 상단 구성(뒤로가기/타이틀) 확인, Business Criticality 매우 낮음 |
| TC-ORDER-004 | 2 | 4 | 4 | 5 | 2 | 2 | 21 | Yes | 배송지 필수 입력 UI 구성 확인, TC-ORDER-005 검증의 기반이 되는 회귀 가치 있는 노출 확인 |
| TC-ORDER-005 | 5 | 5 | 4 | 5 | 3 | 2 | 26 | Yes | 필드별 필수값 검증 실패 시 오배송으로 이어지는 핵심 방어 로직, 조건 분기 다수 |
| TC-ORDER-006 | 3 | 3 | 3 | 3 | 2 | 4 | 16 | Hold | 카카오 우편번호 검색 외부 모듈 의존으로 Maintenance Cost가 높고 결과 판정도 제한적(모달 노출까지만 자체 코드로 통제 가능) |
| TC-ORDER-007 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 필드 레벨 입력 제한, 비용 낮고 결과가 명확한 Negative 검증 |
| TC-ORDER-008 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 드롭다운 옵션 구성 정적 확인, Business Criticality 낮음 |
| TC-ORDER-009 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 직접입력 UI 노출은 TC-ORDER-020(50자 제한) 검증의 전제 조건이라 세트로 자동화 가치 있음 |
| TC-ORDER-010 | 2 | 3 | 4 | 4 | 2 | 3 | 18 | Hold | 주문상품 카드 노출, 정적 성격이며 하위 요소 다수로 판정 복잡도 다소 있음 |
| TC-ORDER-011 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Hold | 옵션명/수량 표시 형식 확인, 정적이며 Business Criticality 낮음 |
| TC-ORDER-012 | 2 | 2 | 4 | 5 | 1 | 1 | 19 | Hold | 수량변경 UI 부재 확인(Negative), 회귀 가치가 낮은 부가 확인 |
| TC-ORDER-013 | 1 | 2 | 4 | 5 | 1 | 1 | 18 | Hold | 쿠폰 없음 안내 문구, Business Criticality 매우 낮은 조건부 문구 |
| TC-ORDER-014 | 1 | 3 | 4 | 5 | 1 | 1 | 19 | Hold | 결제수단 기본 선택 상태 확인, 정적이며 옵션이 1개뿐이라 변경 가능성도 낮음 |
| TC-ORDER-015 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 결제금액 섹션은 실제 금전 정보로 오류 시 신뢰성에 직접 영향, 매 릴리즈 반복 검증 |
| TC-ORDER-016 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | 동의 영역 구성요소(문구 다수)가 많아 유지비용 존재, Business Criticality는 중간 이하 |
| TC-ORDER-017 | 5 | 5 | 4 | 5 | 2 | 3 | 24 | Yes | 필수 동의 없이 결제가 진행되면 약관/법적 리스크로 이어지는 핵심 차단 로직 |
| TC-ORDER-018 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 하단 고정 버튼 금액/개수 표시, 결제 직전 핵심 정보로 반복 검증 가치 있음 |
| TC-ORDER-019 | 5 | 5 | 3 | 3 | 4 | 4 | 22 | Yes | 정상 플로우의 최종 성공 경로(PG 결제창 진입)로 매출 직결 핵심 시나리오. 다만 PG 외부 연동 의존으로 Result Determinism이 제한적(팝업 노출까지만 판정)이고 Maintenance Cost가 높아, 자동화 시 PG 연동 안정성에 대한 별도 확인이 필요함을 사용자에게 안내 |
| TC-ORDER-020 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 50자 초과 입력 차단(Boundary), 결과가 명확하고 TC-ORDER-009와 세트로 자동화 |
| TC-ORDER-021 | 3 | 4 | 3 | 5 | 3 | 3 | 21 | Yes | 계정에 저장된 배송지 값이 정확히 자동 채워지는지 확인하는 TC로, 값이 잘못 채워질 경우 사용자가 인지하지 못한 채 오배송으로 이어질 수 있어 TC-ORDER-004(배송지 섹션 노출)/TC-ORDER-005(필수값 검증)와 함께 배송지 정합성 검증의 연장선에 있음. 필드 값 비교로 결과 판정이 명확(Result Determinism 5)하나, 배송지가 미리 저장된 계정을 준비해야 하는 테스트 데이터 의존성과 비동기 로딩 완료 대기 처리가 필요해 Manual Test Cost/Maintenance Cost를 TC-ORDER-004 대비 다소 높게(각 3점) 평가함. 실측으로 최근 발견되어 아직 요구사항이 충분히 성숙하지 않은 신규 기능이라 Automation Stability는 3으로 다소 보수적으로 평가함. Automation Score 21(자동화 후보 구간)이며 점수 구간과 최종 판단이 일치해 Candidate: Yes로 판단함 |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-ORDER-001 | Approved |  |
| TC-ORDER-002 | Approved |  |
| TC-ORDER-003 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-004 | Approved |  |
| TC-ORDER-005 | Approved |  |
| TC-ORDER-006 | Rejected | 외부 모듈 의존으로,<br>외부 모듈에서 에러시 해당케이스 동시 에러발생 가능성이 존재하므로 자동화 대상 제외 |
| TC-ORDER-007 | Approved |  |
| TC-ORDER-008 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-009 | Approved |  |
| TC-ORDER-010 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-011 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-012 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-013 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-014 | Hold | UI 확인요소 자동화 대상 보류<br>추후 결제수단 추가될 가능성존재하여 보류 |
| TC-ORDER-015 | Approved |  |
| TC-ORDER-016 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-ORDER-017 | Approved |  |
| TC-ORDER-018 | Approved |  |
| TC-ORDER-019 | Hold |  |
| TC-ORDER-020 | Approved |  |
| TC-ORDER-021 | Approved |  |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다.

## Hard Rule 적용 / Validation 특이사항

- 결함을 정상 Expected Result처럼 고정한 TC(Hard Rule 대상)는 발견되지 않았습니다.
- TC-ORDER-006(카카오 우편번호 검색)과 TC-ORDER-019(PG 결제창 진입)는 외부 서비스 연동에
  의존하는 TC로, 자동화 시 외부 시스템 가용성/변경에 따른 Flaky 위험이 있어 각각 Hold/Yes(주의
  필요)로 구분해 표시했습니다. QA Decision 결과 TC-ORDER-006은 외부 모듈 장애 시 동반 오류
  가능성을 이유로 Rejected로, TC-ORDER-019는 Approved로 확정되었습니다.
- 자동화 대상 확정 시점 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태,
  원본 TC 변경 여부) 결과 문제가 발견되지 않아 확정을 진행했습니다.
- 2026-09-06 추가: TC-ORDER-021(REQ-ORDER-019, 이전 저장 배송지 자동 채움)에 대한 Hard Rule
  적용 대상은 발견되지 않았습니다. 현재 정상 동작으로 승인된 신규 요구사항을 검증하는 TC이며,
  결함을 정상처럼 고정한 사례가 아닙니다. 다만 (1) 사전에 배송지가 저장된 계정이라는 테스트 데이터
  준비가 필요하고 (2) 값이 비동기로 채워지므로 자동화 시 로딩 완료 대기 처리가 필요하다는 점을
  구현 단계 참고사항으로 남깁니다.
- **2026-09-06 재조회 중 발견된 QA Decision 변경사항**: TC-ORDER-019(PG 결제창 진입)의 QA
  Decision이 Sheet에서 2026-09-05 확정 시점의 `Approved`에서 현재 `Hold`(QA Comment 비어
  있음)로 변경되어 있음을 확인했습니다. 이는 TC-ORDER-021 평가와 무관하게 사용자가 Sheet에서
  직접 변경한 것으로 보이며, 가공/재해석 없이 위 QA Decision 스냅샷에 그대로 반영했습니다.
- **2026-09-06 사용자 QA Decision 입력 완료 및 자동화 대상 확정 요청에 따른 재조회 및
  Validation**: 사용자가 Google Sheet(워크시트: Automation Candidates)에 TC-ORDER-021의 QA
  Decision을 입력 완료했다고 알려와 `candidate-list`로 재조회한 결과, TC-ORDER-021의 QA
  Decision은 `Approved`(QA Comment 없음)로 확인되었습니다. 이를 기반으로 확정 시점 Validation을
  수행한 결과는 다음과 같습니다.
  1. TC ID 유효성/중복: Sheet상 TC-ORDER-001~021 21건 모두 `docs/tc/order.md`에 실제로 존재하는
     TC ID이며, Sheet 안에서도 각 TC ID가 정확히 1회씩만 존재해 중복이 없음을 확인했습니다.
  2. QA Decision 값 검증: 21건 전체가 `Approved`/`Rejected`/`Hold` 세 값 중 하나로 정확히
     기재되어 있으며, 잘못된 값(오탈자/대소문자 변형/한글 표기 등)이나 미검토(빈 값)로 남은 TC는
     하나도 발견되지 않았습니다.
  3. 원본 TC 승인완료 상태: `docs/tc/order.md`의 `상태`는 여전히 `승인완료`입니다.
  4. TC 변경 여부: 이 문서 프런트매터에 기록된 "대상 TC 문서 최근 변경일(평가 시점 기준)"
     (2026-09-06)이 `docs/tc/order.md`의 최신 변경 이력(2026-09-06, TC-ORDER-021 신설 건)과
     일치해, 평가 시점 이후 원본 TC 문서가 추가로 변경된 사실이 없음을 확인했습니다.

  네 항목 모두 문제가 발견되지 않아 Validation을 통과했으며, 이에 따라 문서 상태를
  `자동화대상확정`으로 전환하고 아래 "Approved TC 목록"을 최종 확정했습니다. TC-ORDER-019는
  QA Decision이 `Hold`이므로 이번 확정에서 Approved 목록에 포함되지 않고 미확정(Hold) 상태로
  유지됩니다(2026-09-05 확정본 대비 Approved에서 Hold로 이동). 기존 TC-ORDER-001~020의 나머지
  19건에 대한 QA Decision/판정은 재확인 결과 변경 없이 그대로 유지되었습니다.

## Approved TC 목록 (자동화 대상 확정)

- 확정일(TC-ORDER-021 포함 총 21건 기준): 2026-09-06
- Approved 11건(자동화 대상 확정): TC-ORDER-001, TC-ORDER-002, TC-ORDER-004, TC-ORDER-005,
  TC-ORDER-007, TC-ORDER-009, TC-ORDER-015, TC-ORDER-017, TC-ORDER-018, TC-ORDER-020,
  TC-ORDER-021
- Hold(미확정) 9건: TC-ORDER-003, TC-ORDER-008, TC-ORDER-010, TC-ORDER-011, TC-ORDER-012,
  TC-ORDER-013, TC-ORDER-014, TC-ORDER-016, TC-ORDER-019
- Rejected 1건: TC-ORDER-006

> 참고: TC-ORDER-019는 2026-09-05 확정 시점에는 Approved였으나, 이후 사용자가 Sheet에서 QA
> Decision을 Hold로 변경함에 따라 이번 확정에서는 미확정(Hold) 상태로 전환되었습니다. 이후
> 사용자가 Sheet에서 QA Decision을 Approved 또는 Rejected로 변경하면, 다음 확정 요청 시 이
> 목록에 반영됩니다. TC-ORDER-021은 이번에 신규로 Approved 확정되어 목록에 추가되었습니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 승인완료 TC 문서(docs/tc/order.md, 20건) 기반 최초 자동화 후보 평가 | 평가중 |
| 2026-09-05 | Google Sheet QA Decision/QA Comment 재조회 및 반영 | 사용자검토완료 |
| 2026-09-05 | 사용자의 자동화 대상 확정 요청에 따라 Validation 수행(문제 없음), Approved 11건/Hold 8건/Rejected 1건 확정 | 자동화대상확정 |
| 2026-09-06 | Phase 3 자동화 구현 중 실측으로 발견된 신규 요구사항(REQ-ORDER-019, 저장된 배송지 자동 채움) 반영해 원본 TC 문서(docs/tc/order.md)에 TC-ORDER-021이 신설(승인완료)됨에 따라 신규 TC 1건 평가 추가(6개 축 평가, Automation Score 21, Candidate: Yes). 기존 20건 평가 결과는 변경하지 않음. 신규 TC는 QA Decision을 다시 받아야 하므로 문서 상태를 `자동화대상확정` → `사용자검토완료`로 되돌림(기존 Approved 11건/Hold 8건/Rejected 1건 판정 자체는 유지되며, 다음 확정 요청 시 재검증됨) | 사용자검토완료 |
| 2026-09-06 | Google Sheet 재조회(candidate-list) 결과 QA Decision 스냅샷 갱신. TC-ORDER-019가 2026-09-05 확정 시점의 `Approved`에서 현재 `Hold`로 변경되어 있음을 확인해 반영(TC-ORDER-021 평가와 별개 사항, 사용자 보고 필요). 그 외 기존 19건의 QA Decision/QA Comment는 변경 없음 | 사용자검토완료 |
| 2026-09-06 | 사용자가 TC-ORDER-021의 QA Decision 입력 완료를 알려와 Google Sheet 재조회(candidate-list) 및 자동화 대상 확정 요청에 따른 Validation 수행. TC-ORDER-021의 QA Decision은 `Approved`로 확인됨. Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, 원본 TC 변경 여부) 4개 항목 모두 문제 없음. 총 21건 기준 Approved 11건(TC-ORDER-021 신규 포함)/Hold(미확정) 9건(TC-ORDER-019 포함)/Rejected 1건으로 확정. 기존 19건(TC-ORDER-019 제외)의 QA Decision/판정은 변경 없이 그대로 유지 | 자동화대상확정 |
