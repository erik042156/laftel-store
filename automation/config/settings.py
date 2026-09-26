BASE_URL = "https://store.laftel.net/"
DEFAULT_TIMEOUT = 10
LOGIN_TIMEOUT = 20
LOGIN_EMAIL_URL = "https://laftel.net/auth/email"
LOGIN_LANDING_URL = "https://laftel.net/auth/login"
# 이메일 로그인 계정(TEST_ACCOUNT_*)이 서버측 잠금으로 추정되는 오류로 막혀
# 임시로 구글 로그인으로 전환(AUTOMATION_GUIDE 7.7 참고). 잠금 해제 후 "email"로 원복.
LOGIN_METHOD = "google"
WINDOW_SIZE = (1600, 1000)

# 테스트 상품 ID
#
# 아래 상수들은 실제 판매자/재고 데이터의 "지금 이 순간 상태"를 가정한다. QA가 통제할 수
# 없는 데이터이므로 재입고/판매 재개/옵션 재고 소진/가격 변경으로 가정이 깨질 수 있다.
# conftest.py의 _skip_if_product_status_changed / _skip_for_data_drift가 실행 시점에 실제
# 상태를 재확인해, 가정이 깨지면 관련 테스트가 실패 대신 "[TEST DATA DRIFT]" 사유로 skip된다.
# skip이 뜨면 실제 사이트에서 조건에 맞는 상품/키워드를 다시 찾아 아래 값을 갱신할 것.
PRODUCT_ID_ON_SALE = "3630"  # 가정: 정상 판매중(구매하기 활성). 의존: 거의 전체 스위트(cart/order/product_detail/wishlist)
PRODUCT_ID_NOT_FOUND = "2"
PRODUCT_ID_WITH_OPTIONS = "553"  # 가정: 옵션 중 품절/구매가능이 혼재. 의존: TC-PD-036/037/046, test_cart._add_product_to_cart
PRODUCT_ID_SOLD_OUT = "3029"  # 가정: 품절(버튼 비활성). 의존: TC-PD-042/044, TC-SEARCH-014, TC-WISHLIST-008/017
PRODUCT_ID_SALE_ENDED = "1608"  # 가정: 판매종료(버튼 비활성). 의존: TC-PD-043
PRODUCT_ID_HIGH_PRICE = "3747"  # 가정: 가격 100,000원 이상(묶음배송비 무료 임계값을 넘김). 의존: TC-CART-007, TC-WISHLIST-008
IP_ID_ON_SALE = "103"  # PRODUCT_ID_ON_SALE(3630)의 작품 페이지
SEARCH_KEYWORD_WITH_RESULTS = "피스"  # 찜 아이콘이 있는 검색 결과가 노출되는 것을 실측으로 확인한 키워드
# 참고: TC-CART-008(test_single_item_under_threshold_shows_individual_shipping_notice)은 반대로
# PRODUCT_ID_ON_SALE 가격이 100,000원 미만이어야 성립한다(현재는 별도 skip 가드 없음).

# Phase 5(검색) TC-SEARCH-012~014용. 검색은 키워드 단어 단위로 넓게 매칭되어(예: "피스"
# 검색에도 "피규어" 등이 함께 노출됨) 특정 상품이 검색 결과 1페이지(20건)에 실제로
# 노출되는지를 실측으로 별도 확인해야 했다. 검색 순위는 실시간으로 바뀔 수 있어, TC-SEARCH-013/014는
# 클릭 전에 search_result_page.is_product_present/get_product_card_status_badge_text로 1페이지 노출과
# 상태를 재확인하고, 어긋나면 "[TEST DATA DRIFT]" 사유로 skip한다.
SEARCH_KEYWORD_WITH_STATUS_PRODUCTS = "루피"  # 품절/판매종료 상품과 정상 상품이 함께 노출됨을 실측 확인 (TC-SEARCH-012)
SEARCH_KEYWORD_SOLD_OUT_PRODUCT = "이누이 사쥬나"  # PRODUCT_ID_SOLD_OUT(3029)이 1페이지에 노출되는 키워드 (TC-SEARCH-014)
SEARCH_KEYWORD_SALE_ENDED_PRODUCT = "[예약] THEORAM"  # PRODUCT_ID_SEARCH_SALE_ENDED가 1페이지에 노출되는 키워드 (TC-SEARCH-013)
# PRODUCT_ID_SALE_ENDED(1608, Phase1)는 검색 키워드 매칭 순위가 낮아 1페이지에 노출되지
# 않아 검색 전용으로 별도 확인한 판매종료 상품 ID. 가정: 판매종료. 의존: TC-SEARCH-013
PRODUCT_ID_SEARCH_SALE_ENDED = "3809"
