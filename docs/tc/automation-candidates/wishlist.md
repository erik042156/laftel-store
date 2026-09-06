---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/wishlist.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-09-05
관련 Feature PRD: feature/prd-wishlist.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-09-05
최근 변경일: 2026-09-05
최근 Sheet 동기화일: 2026-09-05
확정일: 2026-09-05
---

# Automation Candidate 평가 - 찜

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-WISHLIST-001 | 3 | 4 | 4 | 5 | 2 | 2 | 22 | Yes | 비로그인 상태 찜 클릭 시 로그인 유도, 로그인 분기 로직으로 회귀 가치 있음 |
| TC-WISHLIST-002 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 메인페이지 찜 추가는 여러 화면에서 공통으로 쓰이는 핵심 로직 |
| TC-WISHLIST-003 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 찜 해제 토글, 찜 추가와 짝을 이루는 핵심 동작 |
| TC-WISHLIST-004 | 2 | 3 | 4 | 5 | 2 | 3 | 19 | Hold | 검색페이지에서의 동일 찜 동작 재확인 — 핵심 로직 자체는 TC-WISHLIST-001~003에서 이미 검증되어(별도 Risk Coverage가 제한적) 자동화 우선순위가 낮음 |
| TC-WISHLIST-005 | 2 | 3 | 4 | 5 | 2 | 3 | 19 | Hold | 작품페이지에서의 동일 찜 동작 재확인, TC-WISHLIST-004와 동일 근거 |
| TC-WISHLIST-006 | 3 | 4 | 4 | 5 | 2 | 3 | 21 | Yes | 찜 메뉴 뱃지 개수의 실시간 동기화, 결함 시 사용자가 찜 상태를 오인할 수 있어 회귀 가치 있음 |
| TC-WISHLIST-007 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 찜한 상품 섹션 카드/하트 노출, 저비용이고 결정적 |
| TC-WISHLIST-008 | 4 | 4 | 3 | 4 | 3 | 3 | 21 | Yes | 찜 여부와 상품 상태 뱃지가 결합된 표시 로직, 오표시 시 찜 상태 오인 위험 있어 회귀 가치 높음 |
| TC-WISHLIST-009 | 5 | 5 | 3 | 4 | 3 | 3 | 23 | Yes | "최근 본 상품"/"찜한 상품"/`/my/wish` 3화면 간 실시간 동기화, 데이터 정합성이 요구되는 핵심 로직(P0) |
| TC-WISHLIST-010 | 1 | 3 | 5 | 5 | 1 | 1 | 20 | Hold | 상단 탭 구성 정적 확인, Business Criticality 매우 낮음 |
| TC-WISHLIST-011 | 3 | 4 | 3 | 4 | 3 | 4 | 19 | Hold | 무한 스크롤 확인에는 스크롤 로드가 가능한 대량의 찜 데이터 준비가 필요해 테스트 데이터 준비/유지 비용이 높음 |
| TC-WISHLIST-012 | 1 | 3 | 4 | 5 | 1 | 1 | 19 | Hold | 편집하기 링크 노출 유무 확인, Business Criticality 낮은 정적 확인 |
| TC-WISHLIST-013 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | IP별 섹션 구성 확인, 정적이며 구조 변경 시 유지비용 존재 |
| TC-WISHLIST-014 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 작품 섹션 제목 클릭 이동, 저비용이고 결정적 |
| TC-WISHLIST-015 | 4 | 3 | 3 | 5 | 2 | 3 | 20 | Yes | 작품 단위 전체 찜 해제는 되돌리기 어려운 대량 데이터 변경이라 회귀 검증 가치 있음 |
| TC-WISHLIST-016 | 4 | 3 | 3 | 5 | 2 | 3 | 20 | Yes | 개별 찜 해제 및 다른 탭과의 동기화, 데이터 정합성 검증 필요 |
| TC-WISHLIST-017 | 3 | 3 | 4 | 5 | 3 | 3 | 21 | Yes | 판매종료/품절 상태 뱃지와 상세 진입, 상태 분기 검증 |
| TC-WISHLIST-018 | 1 | 2 | 4 | 5 | 1 | 1 | 18 | Hold | 상품 탭 빈 상태 문구, Business Criticality 매우 낮음 |
| TC-WISHLIST-019 | 1 | 2 | 4 | 5 | 1 | 1 | 18 | Hold | 작품 탭 빈 상태 문구, TC-WISHLIST-018과 동일 근거 |
| TC-WISHLIST-020 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 편집 모드 진입은 이후 선택/삭제 관련 TC들의 전제 조건이라 세트로 자동화 가치 있음 |
| TC-WISHLIST-021 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 전체 선택 체크박스, 저비용이고 결정적 |
| TC-WISHLIST-022 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 개별 카드 선택/해제, TC-WISHLIST-021과 짝을 이루는 로직 |
| TC-WISHLIST-023 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 선택삭제 확인 팝업 및 취소, 데이터 변경 전 안전장치 검증 |
| TC-WISHLIST-024 | 5 | 4 | 4 | 5 | 2 | 2 | 24 | Yes | 선택삭제 확정은 되돌릴 수 없는 데이터 삭제 동작으로 핵심 자동화 대상 |
| TC-WISHLIST-025 | 2 | 3 | 4 | 5 | 1 | 2 | 19 | Yes | 편집취소 클릭 시 편집 모드 해제, 저비용이고 결정적 |
| TC-WISHLIST-026 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 비로그인 `/my` 진입 및 찜 메뉴 클릭 시 로그인 유도, 진입 자체와 메뉴 클릭 분기를 함께 검증 |
| TC-WISHLIST-027 | 3 | 3 | 4 | 5 | 1 | 2 | 20 | Yes | 비로그인 `/my/wish` URL 직접 진입 시 로그인 유도, 접근 제어 검증 |
| TC-WISHLIST-028 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | URL 직접 진입 경로에서 팝업 취소 시 메인 이동, 진입 경로별 분기 |
| TC-WISHLIST-029 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 사이트 내 진입 경로에서 팝업 취소 시 화면 유지, TC-WISHLIST-028과 짝을 이루는 분기 |
| TC-WISHLIST-030 | 2 | 3 | 3 | 4 | 2 | 3 | 17 | Hold | 로그인 페이지 이동 확인, 외부 로그인 도메인(laftel.net) 연동 성격이라 유지비용 다소 있음 |
| TC-WISHLIST-031 | 5 | 4 | 3 | 4 | 4 | 4 | 22 | Yes | URL 직접 진입 후 로그인 완료 시 원래 목적지로 이동하는 핵심 리디렉션 로직(P0). 다만 실제 로그인 완료 처리가 필요해 외부 인증 연동에 따른 Maintenance Cost가 높으므로, 자동화 시 안정적인 테스트 계정/로그인 자동화 방안을 함께 준비할 필요가 있음을 별도 안내 |
| TC-WISHLIST-032 | 5 | 4 | 3 | 4 | 4 | 4 | 22 | Yes | 사이트 내 진입 경로 로그인 완료 후 리디렉션, TC-WISHLIST-031과 동일 근거(외부 인증 연동 유지비용 주의) |
| TC-WISHLIST-033 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 선택 0건 상태에서 선택삭제 클릭 무반응 가드(Negative), 결과가 명확하고 저비용 |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-WISHLIST-001 | Approved |  |
| TC-WISHLIST-002 | Approved |  |
| TC-WISHLIST-003 | Approved |  |
| TC-WISHLIST-004 | Approved |  |
| TC-WISHLIST-005 | Approved |  |
| TC-WISHLIST-006 | Approved |  |
| TC-WISHLIST-007 | Approved |  |
| TC-WISHLIST-008 | Approved |  |
| TC-WISHLIST-009 | Approved |  |
| TC-WISHLIST-010 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-WISHLIST-011 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-WISHLIST-012 | Approved |  |
| TC-WISHLIST-013 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-WISHLIST-014 | Approved |  |
| TC-WISHLIST-015 | Approved |  |
| TC-WISHLIST-016 | Approved |  |
| TC-WISHLIST-017 | Approved |  |
| TC-WISHLIST-018 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-WISHLIST-019 | Hold | UI 확인요소 자동화 대상 보류 |
| TC-WISHLIST-020 | Approved |  |
| TC-WISHLIST-021 | Approved |  |
| TC-WISHLIST-022 | Approved |  |
| TC-WISHLIST-023 | Approved |  |
| TC-WISHLIST-024 | Approved |  |
| TC-WISHLIST-025 | Approved |  |
| TC-WISHLIST-026 | Approved |  |
| TC-WISHLIST-027 | Approved |  |
| TC-WISHLIST-028 | Approved |  |
| TC-WISHLIST-029 | Approved |  |
| TC-WISHLIST-030 | Approved |  |
| TC-WISHLIST-031 | Approved |  |
| TC-WISHLIST-032 | Approved |  |
| TC-WISHLIST-033 | Approved |  |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다.

## Hard Rule 적용 / Validation 특이사항

- 결함을 정상 Expected Result처럼 고정한 TC(Hard Rule 대상)는 발견되지 않았습니다.
- TC-WISHLIST-004, 005는 4.3절 "TC 중복 여부" 검토 결과 핵심 찜 로직이 TC-WISHLIST-001~003에서
  이미 검증되고 별도 Risk Coverage가 제한적이라 판단해 Hold로 표시했습니다.
- TC-WISHLIST-031, 032는 실제 외부 로그인 완료 처리가 필요한 리디렉션 검증으로, 자동화 시
  안정적인 로그인 자동화 방안이 함께 필요함을 별도로 안내합니다. QA Decision은 두 건 모두
  Approved로 확정되었습니다.
- TC-WISHLIST-004, 005, 012, 030은 AI Candidate(Hold)와 달리 QA Decision이 Approved로
  결정되었습니다(QA Decision이 AI Candidate 추천보다 우선하므로 그대로 반영).
- 자동화 대상 확정 시점 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태,
  원본 TC 변경 여부) 결과 문제가 발견되지 않아 확정을 진행했습니다.

## Approved TC 목록 (자동화 대상 확정)

- 확정일: 2026-09-05
- Approved 28건: TC-WISHLIST-001, 002, 003, 004, 005, 006, 007, 008, 009, 012, 014, 015,
  016, 017, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 030, 031, 032, 033
- Hold(미확정) 5건: TC-WISHLIST-010, 011, 013, 018, 019
- Rejected 0건

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-09-05 | 승인완료 TC 문서(docs/tc/wishlist.md, 33건) 기반 최초 자동화 후보 평가 | 평가중 |
| 2026-09-05 | Google Sheet QA Decision/QA Comment 재조회 및 반영 | 사용자검토완료 |
| 2026-09-05 | 사용자의 자동화 대상 확정 요청에 따라 Validation 수행(문제 없음), Approved 28건/Hold 5건/Rejected 0건 확정 | 자동화대상확정 |
