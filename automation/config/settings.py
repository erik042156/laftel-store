BASE_URL = "https://store.laftel.net/"
DEFAULT_TIMEOUT = 10
LOGIN_TIMEOUT = 20
LOGIN_EMAIL_URL = "https://laftel.net/auth/email"
LOGIN_LANDING_URL = "https://laftel.net/auth/login"
# 이메일 로그인 계정(TEST_ACCOUNT_*)이 서버측 잠금으로 추정되는 오류로 막혀
# 임시로 구글 로그인으로 전환(AUTOMATION_GUIDE 7.7 참고). 잠금 해제 후 "email"로 원복.
LOGIN_METHOD = "google"
WINDOW_SIZE = (1600, 1000)

# Playwright MCP로 2026-09-05 실측한 테스트 상품 ID
PRODUCT_ID_ON_SALE = "4439"
PRODUCT_ID_NOT_FOUND = "2"
PRODUCT_ID_WITH_OPTIONS = "553"
PRODUCT_ID_SOLD_OUT = "3029"
PRODUCT_ID_SALE_ENDED = "1608"
PRODUCT_ID_HIGH_PRICE = "3747"  # 344,000원 — 묶음배송비 100,000원 이상 무료 조건 검증용
IP_ID_ON_SALE = "103"  # PRODUCT_ID_ON_SALE(4439)의 작품 페이지
SEARCH_KEYWORD_WITH_RESULTS = "피스"  # 찜 아이콘이 있는 검색 결과가 노출되는 것을 실측으로 확인한 키워드
# IP_ID_ON_SALE(103, 하츠네미쿠)에 속한 서로 다른 상품 2건 (찜 페이지 "작품" 탭 TC용).
# 같은 작품의 4499/4497 등은 예약구매 상품이라 구매하기 버튼 문구가 달라 기존
# ProductDetailPage.BOTTOM_WISH_ICON 로케이터가 매칭되지 않으므로 제외했다(AUTOMATION_GUIDE 7.12절).
IP_PRODUCT_ID_A = "4440"
IP_PRODUCT_ID_B = "4441"

# Phase 5(검색) TC-SEARCH-012~014용. 검색은 키워드 단어 단위로 넓게 매칭되어(예: "피스"
# 검색에도 "피규어" 등이 함께 노출됨) 특정 상품이 검색 결과 1페이지(20건)에 실제로
# 노출되는지를 실측으로 별도 확인해야 했다.
SEARCH_KEYWORD_WITH_STATUS_PRODUCTS = "루피"  # 품절/판매종료 상품과 정상 상품이 함께 노출됨을 실측 확인 (TC-SEARCH-012)
SEARCH_KEYWORD_SOLD_OUT_PRODUCT = "이누이 사쥬나"  # PRODUCT_ID_SOLD_OUT(3029)이 1페이지에 노출되는 키워드 (TC-SEARCH-014)
SEARCH_KEYWORD_SALE_ENDED_PRODUCT = "[예약] THEORAM"  # PRODUCT_ID_SEARCH_SALE_ENDED가 1페이지에 노출되는 키워드 (TC-SEARCH-013)
# PRODUCT_ID_SALE_ENDED(1608, Phase1)는 검색 키워드 매칭 순위가 낮아 1페이지에 노출되지
# 않아 검색 전용으로 별도 확인한 판매종료 상품 ID.
PRODUCT_ID_SEARCH_SALE_ENDED = "3809"
