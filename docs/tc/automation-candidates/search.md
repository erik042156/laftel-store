---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/search.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-09-04
관련 Feature PRD: feature/prd-search.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
최근 Sheet 동기화일: 2026-09-05
확정일: 2026-09-05
---

# Automation Candidate 평가 - 검색

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-SEARCH-001 | 2 | 4 | 4 | 5 | 1 | 2 | 20 | Yes | 검색 진입 경로, 반복 검증 빈도 높고 저비용 |
| TC-SEARCH-002 | 2 | 4 | 5 | 5 | 1 | 1 | 22 | Yes | URL 직접 진입, 매우 안정적이고 저비용 |
| TC-SEARCH-003 | 4 | 5 | 3 | 4 | 2 | 3 | 21 | Yes | 자동완성 노출/구성은 검색 기능의 핵심 사용성으로 회귀 가치 매우 높음 |
| TC-SEARCH-004 | 2 | 3 | 3 | 4 | 3 | 4 | 17 | Hold | 작품 20개/연관검색어 10개 이상 결과가 확인된 특정 키워드에 의존하는 Boundary 테스트로, 실제 데이터가 바뀌면 조건이 깨질 위험이 커 유지비용이 높음 |
| TC-SEARCH-005 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | 특정 키워드 쌍("원"/"dnjs")의 동일 결과 매핑에 의존, 실제 데이터/사전 변경 시 깨질 위험 |
| TC-SEARCH-006 | 3 | 4 | 4 | 5 | 2 | 3 | 21 | Yes | 자동완성 "작품" 뱃지 클릭 시 작품 페이지 이동, 검색 결과 분기의 핵심 경로 |
| TC-SEARCH-007 | 3 | 4 | 4 | 5 | 2 | 3 | 21 | Yes | 자동완성 연관 검색어 클릭 시 검색 결과 이동, TC-SEARCH-006과 짝을 이루는 분기 |
| TC-SEARCH-008 | 3 | 4 | 3 | 4 | 2 | 3 | 19 | Yes | 입력값 변경에 따른 자동완성 실시간 갱신, 검색 핵심 UX로 반복 검증 가치 있음 |
| TC-SEARCH-009 | 4 | 5 | 4 | 5 | 2 | 3 | 23 | Yes | 검색 결과 화면의 기본 구성(개수/정렬/그리드)은 검색의 최종 산출물로 신뢰성에 직접 영향 |
| TC-SEARCH-010 | 2 | 3 | 4 | 5 | 2 | 3 | 19 | Hold | 상단 작품 카드 이동, 부가 네비게이션 성격 |
| TC-SEARCH-011 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 정렬 드롭다운 옵션/선택 반영, 결과 판정 명확하고 저비용 |
| TC-SEARCH-012 | 4 | 4 | 4 | 5 | 3 | 3 | 23 | Yes | 상품종료 상품 노출 누락 시 판매 기회 손실로 이어질 수 있어 회귀 가치 높음 |
| TC-SEARCH-013 | 4 | 4 | 4 | 5 | 3 | 3 | 23 | Yes | 판매종료 상품 클릭 시 상세 진입/버튼 상태, 상태 분기 검증 |
| TC-SEARCH-014 | 4 | 4 | 4 | 5 | 3 | 3 | 23 | Yes | 품절 상품 클릭 시 상세 진입/버튼 상태, TC-SEARCH-013과 짝을 이루는 분기 |
| TC-SEARCH-015 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 결과 없음 빈 상태 확인, 저비용이고 결정적 |
| TC-SEARCH-016 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 공백만 입력 시 미실행(Negative), 저비용이고 결정적 |
| TC-SEARCH-017 | 2 | 2 | 3 | 4 | 2 | 3 | 16 | Hold | 매핑 없는 특정 키워드("테스트데이터","뷁")에 의존하는 Boundary 테스트, 검색엔진/데이터 변경 시 깨질 위험 |
| TC-SEARCH-018 | 2 | 2 | 3 | 4 | 2 | 3 | 16 | Hold | 매핑 있는 특정 키워드에 의존하는 Boundary 테스트, 동일한 데이터 의존 위험 |
| TC-SEARCH-019 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 1자 입력 검색 정상 실행(Boundary), 결과가 명확하고 저비용 |
| TC-SEARCH-020 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 검색어 삭제 시 최근 검색 영역 노출, 저비용이며 결정적 |
| TC-SEARCH-021 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 확인 팝업 없이 즉시 전체 삭제되는 데이터 조작으로 오동작 시 되돌릴 수 없어 회귀 검증 가치 있음 |
| TC-SEARCH-022 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 개별 항목 즉시 삭제, TC-SEARCH-021과 동일한 근거 |
| TC-SEARCH-023 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 최근 검색어 클릭 재검색, 저비용이고 결정적 |
| TC-SEARCH-024 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 비로그인 상태 최근 검색어 저장, 로그인 여부 분기 로직으로 회귀 가치 있음 |
| TC-SEARCH-025 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 메인에서 진입 후 뒤로가기 복귀, 진입 경로별 분기 검증 중 하나 |
| TC-SEARCH-026 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 상품상세에서 진입 후 뒤로가기 복귀, TC-SEARCH-025와 짝을 이루는 분기 |
| TC-SEARCH-027 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 취소 버튼 클릭 시 초기화, 저비용이고 결정적 |
| TC-SEARCH-028 | 2 | 2 | 4 | 5 | 1 | 2 | 18 | Hold | Hard Rule 대상 아님(Expected Result는 PRD 정상 기준을 올바르게 반영, 결함을 정상으로 고정한 것이 아님). 다만 현재 DEFECT-SEARCH-001로 인해 자동화 시 상시 Fail 상태가 예상되어, 결함 수정 전까지는 회귀 감지 실효성이 낮고 리포트 노이즈만 발생할 위험이 있어 Hold로 판정. 결함 수정 후 재검토 권장 |
| TC-SEARCH-029 | 2 | 2 | 4 | 5 | 1 | 2 | 18 | Hold | TC-SEARCH-028과 동일 근거(DEFECT-SEARCH-001, 결함 수정 전까지 상시 Fail 예상) |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-SEARCH-001 | Approved |  |
| TC-SEARCH-002 | Approved |  |
| TC-SEARCH-003 | Approved |  |
| TC-SEARCH-004 | Rejected |  |
| TC-SEARCH-005 | Rejected |  |
| TC-SEARCH-006 | Approved |  |
| TC-SEARCH-007 | Approved |  |
| TC-SEARCH-008 | Approved |  |
| TC-SEARCH-009 | Approved |  |
| TC-SEARCH-010 | Approved |  |
| TC-SEARCH-011 | Approved |  |
| TC-SEARCH-012 | Approved |  |
| TC-SEARCH-013 | Approved |  |
| TC-SEARCH-014 | Approved |  |
| TC-SEARCH-015 | Approved |  |
| TC-SEARCH-016 | Approved |  |
| TC-SEARCH-017 | Rejected |  |
| TC-SEARCH-018 | Rejected |  |
| TC-SEARCH-019 | Approved |  |
| TC-SEARCH-020 | Approved |  |
| TC-SEARCH-021 | Approved |  |
| TC-SEARCH-022 | Approved |  |
| TC-SEARCH-023 | Approved |  |
| TC-SEARCH-024 | Approved |  |
| TC-SEARCH-025 | Approved |  |
| TC-SEARCH-026 | Approved |  |
| TC-SEARCH-027 | Approved |  |
| TC-SEARCH-028 | Rejected | 결함의심 항목으로 자동화 제외 |
| TC-SEARCH-029 | Rejected | 결함의심 항목으로 자동화 제외 |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다.

## Hard Rule 적용 / Validation 특이사항

- **TC-SEARCH-028, TC-SEARCH-029 관련 확인**: docs/tc/search.md의 "결함 의심 항목"에 포함된
  TC이나, Expected Result는 실제 관찰된 버그 동작이 아니라 PRD(REQ-SEARCH-017) 기준 정상
  동작(결과 없음 화면)으로 올바르게 작성되어 있어 Skill 5절 Hard Rule("결함을 정상처럼 고정")에
  해당하지 않습니다. 관찰된 실제 버그(DEFECT-SEARCH-001)는 별도 노트로만 기록되어 있습니다.
  다만 결함이 해결되기 전까지는 자동화해도 상시 Fail이 예상되어 두 TC 모두 Hold로 판정했습니다.
- 그 외 결함을 정상 Expected Result처럼 고정한 TC는 발견되지 않았습니다.
- TC-SEARCH-004/005/017/018은 특정 키워드의 실제 검색 결과 개수·매핑에 의존하는 Boundary
  테스트로, 운영 데이터 변경 시 테스트가 깨질 위험이 있어 Hold로 판정했으며, QA Decision도
  4건 모두 Rejected로 확정되었습니다.
- TC-SEARCH-028, 029는 QA Decision에서도 "결함의심 항목으로 자동화 제외" 사유로 Rejected
  결정되었습니다(AI Candidate: Hold와 방향은 다르나 결함 미해결 상태에서 자동화 대상에서
  제외한다는 취지는 일치).
- 자동화 대상 확정 시점 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태,
  원본 TC 변경 여부) 결과 문제가 발견되지 않아 확정을 진행했습니다.

## Approved TC 목록 (자동화 대상 확정)

- 확정일: 2026-09-05
- Approved 23건: TC-SEARCH-001, 002, 003, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015,
  016, 019, 020, 021, 022, 023, 024, 025, 026, 027
- Hold(미확정) 0건
- Rejected 6건: TC-SEARCH-004, 005, 017, 018, 028, 029

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 승인완료 TC 문서(docs/tc/search.md, 29건) 기반 최초 자동화 후보 평가 | 평가중 |
| 2026-09-05 | Google Sheet QA Decision/QA Comment 재조회 및 반영 | 사용자검토완료 |
| 2026-09-05 | 사용자의 자동화 대상 확정 요청에 따라 Validation 수행(문제 없음), Approved 23건/Hold 0건/Rejected 6건 확정 | 자동화대상확정 |
