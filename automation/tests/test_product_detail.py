from config.settings import (
    BASE_URL,
    PRODUCT_ID_NOT_FOUND,
    PRODUCT_ID_ON_SALE,
    PRODUCT_ID_SALE_ENDED,
    PRODUCT_ID_SOLD_OUT,
    PRODUCT_ID_WITH_OPTIONS,
)
from pages.cart_page import CartPage
from pages.exchange_return_info_page import ExchangeReturnInfoPage
from pages.my_store_page import MyStorePage
from pages.not_found_page import NotFoundPage
from pages.notice_page import NoticePage
from pages.product_detail_page import ProductDetailPage
from pages.product_info_page import ProductInfoPage
from pages.related_products_page import RelatedProductsPage
from pages.seller_info_page import SellerInfoPage
from pages.wishlist_page import WishlistPage


def test_direct_url_entry(driver):
    """TC-PRODUCT-DETAIL-006"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    actual_url = page.get_current_url()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}"
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"


def test_not_found_page_on_invalid_product_id(driver):
    """TC-PRODUCT-DETAIL-007"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_NOT_FOUND)

    not_found_page = NotFoundPage(driver)
    actual_message = not_found_page.get_message_text()
    expected_message = "이런, 이미 사라진 페이지군요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"


def test_search_icon_navigates_to_search(driver):
    """TC-PRODUCT-DETAIL-010"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_search_icon()
    page.wait_for_url_contains("/search")

    actual_url = page.get_current_url()
    assert "/search" in actual_url, f"Expected URL to contain '/search', but got {actual_url}"


def test_cart_icon_click_when_logged_out_shows_login_prompt(driver):
    """TC-PRODUCT-DETAIL-011"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_cart_icon()

    actual_message = page.get_login_prompt_text()
    expected_message = "로그인 후 이용해 주세요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"

    actual_url = page.get_current_url()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}"
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"


def test_back_button_returns_previous_page(driver):
    """TC-PRODUCT-DETAIL-012"""
    driver.get(BASE_URL)
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_back()
    page.wait_for_url_to_be(BASE_URL)

    actual_url = page.get_current_url()
    assert actual_url == BASE_URL, f"Expected {BASE_URL}, but got {actual_url}"


def test_main_list_click_enters_product_detail(driver):
    """TC-PRODUCT-DETAIL-002"""
    driver.get(BASE_URL)
    page = ProductDetailPage(driver)

    page.click_main_list_product()
    page.wait_for_url_contains(f"{BASE_URL}products/")

    actual_url = page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"


def test_carousel_next_updates_pagination(driver):
    """TC-PRODUCT-DETAIL-013 (페이지네이션 초기 표시 + 다음 이미지 전환)"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    initial_pagination = page.get_carousel_pagination_text()
    assert initial_pagination == "1/4", f"Expected 1/4, but got {initial_pagination}"

    page.go_to_next_image()
    page.wait_for_text(page.CAROUSEL_PAGINATION, "2/4")

    actual_pagination = page.get_carousel_pagination_text()
    assert actual_pagination == "2/4", f"Expected 2/4, but got {actual_pagination}"


def test_carousel_first_prev_cycles_to_last(driver):
    """TC-PRODUCT-DETAIL-013 (첫 번째 사진에서 이전으로 넘기면 마지막으로 순환, Boundary)"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.go_to_prev_image()
    page.wait_for_text(page.CAROUSEL_PAGINATION, "4/4")

    actual_pagination = page.get_carousel_pagination_text()
    assert actual_pagination == "4/4", f"Expected 4/4, but got {actual_pagination}"


def test_ip_title_link_navigates_to_ip_page(driver):
    """TC-PRODUCT-DETAIL-014"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_ip_title_link()
    page.wait_for_url_contains(f"{BASE_URL}ip/")

    actual_url = page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}ip/"), f"Expected an IP page URL, but got {actual_url}"


def test_product_name_and_price_displayed(driver):
    """TC-PRODUCT-DETAIL-015"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    actual_name = page.get_product_name()
    actual_price = page.get_product_price()
    assert actual_name != "", "Expected product name to be displayed, but it was empty"
    assert actual_price != "", "Expected product price to be displayed, but it was empty"


def test_related_carousel_card_click_navigates_to_product_detail(driver):
    """TC-PRODUCT-DETAIL-019"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)
    original_url = page.get_current_url()

    page.click_related_card(index=1)
    page.wait_for_url_change(original_url)

    actual_url = page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"
    assert actual_url != original_url, f"Expected navigation to a different product, but stayed on {actual_url}"


def test_related_more_button_navigates_to_related_page_with_grid(driver):
    """TC-PRODUCT-DETAIL-020"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    product_detail_page.click_related_more()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}/related"
    product_detail_page.wait_for_url_to_be(expected_url)

    actual_url = product_detail_page.get_current_url()
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    related_products_page = RelatedProductsPage(driver)
    actual_title = related_products_page.get_title_text()
    assert actual_title == "같은 작품 굿즈", f"Expected '같은 작품 굿즈', but got {actual_title}"

    actual_item_count = related_products_page.get_grid_item_count()
    assert actual_item_count > 0, f"Expected at least 1 grid item, but got {actual_item_count}"


def test_detail_more_toggle_expands_content(driver):
    """TC-PRODUCT-DETAIL-024"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    initial_text = page.get_detail_toggle_text()
    assert initial_text == "상세정보 더보기", f"Expected '상세정보 더보기', but got {initial_text}"

    page.click_detail_more_toggle()
    page.wait_for_text(page.DETAIL_MORE_TOGGLE, "접기")

    actual_text = page.get_detail_toggle_text()
    assert actual_text == "상세정보 접기", f"Expected '상세정보 접기', but got {actual_text}"


def test_product_info_accordion_navigates_and_shows_table(driver):
    """TC-PRODUCT-DETAIL-025"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    product_detail_page.click_product_info_accordion()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}/product-info"
    product_detail_page.wait_for_url_to_be(expected_url)

    actual_url = product_detail_page.get_current_url()
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    product_info_page = ProductInfoPage(driver)
    actual_title = product_info_page.get_title_text()
    assert actual_title == "상품정보 제공고시", f"Expected '상품정보 제공고시', but got {actual_title}"

    actual_content = product_info_page.get_content_text()
    for expected_label in ("브랜드", "원산지", "제조사", "공급사", "자체분류"):
        assert expected_label in actual_content, f"Expected '{expected_label}' in content, but got {actual_content}"


def test_exchange_return_info_accordion_navigates_and_shows_content(driver):
    """TC-PRODUCT-DETAIL-026"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    product_detail_page.click_exchange_return_info_accordion()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}/exchange-return-info"
    product_detail_page.wait_for_url_to_be(expected_url)

    actual_url = product_detail_page.get_current_url()
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    exchange_return_info_page = ExchangeReturnInfoPage(driver)
    actual_title = exchange_return_info_page.get_title_text()
    assert actual_title == "교환/반품 안내", f"Expected '교환/반품 안내', but got {actual_title}"

    actual_content = exchange_return_info_page.get_content_text()
    assert "7일 이내" in actual_content, f"Expected '7일 이내' in content, but got {actual_content}"
    assert "반송" in actual_content, f"Expected '반송' in content, but got {actual_content}"


def test_seller_info_accordion_navigates_and_shows_content(driver):
    """TC-PRODUCT-DETAIL-027"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    product_detail_page.click_seller_info_accordion()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}/seller-info"
    product_detail_page.wait_for_url_to_be(expected_url)

    actual_url = product_detail_page.get_current_url()
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    seller_info_page = SellerInfoPage(driver)
    actual_title = seller_info_page.get_title_text()
    assert actual_title == "판매자 정보", f"Expected '판매자 정보', but got {actual_title}"

    actual_content = seller_info_page.get_content_text()
    assert "공급사" in actual_content, f"Expected '공급사' in content, but got {actual_content}"


def test_notice_accordion_navigates_and_shows_content(driver):
    """TC-PRODUCT-DETAIL-028"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    product_detail_page.click_notice_accordion()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}/notice"
    product_detail_page.wait_for_url_to_be(expected_url)

    actual_url = product_detail_page.get_current_url()
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    notice_page = NoticePage(driver)
    actual_title = notice_page.get_title_text()
    assert actual_title == "유의사항", f"Expected '유의사항', but got {actual_title}"

    actual_content = notice_page.get_content_text()
    assert "배송 안내" in actual_content, f"Expected '배송 안내' in content, but got {actual_content}"
    assert "주문 취소" in actual_content, f"Expected '주문 취소' in content, but got {actual_content}"


def test_buy_button_expands_purchase_area(logged_in_driver):
    """TC-PRODUCT-DETAIL-035"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_buy_button()
    page.wait_for_text(page.QUANTITY_VALUE, "1")

    actual_quantity = page.get_quantity()
    assert actual_quantity == "1", f"Expected quantity 1, but got {actual_quantity}"

    add_to_cart_buttons = logged_in_driver.find_elements(*page.ADD_TO_CART_BUTTON)
    buy_now_buttons = logged_in_driver.find_elements(*page.BUY_NOW_BUTTON)
    assert len(add_to_cart_buttons) == 1, "Expected '장바구니에 담기' button to be displayed"
    assert len(buy_now_buttons) == 1, "Expected '바로구매' button to be displayed"


def test_option_dropdown_shows_sold_out_options_disabled(logged_in_driver):
    """TC-PRODUCT-DETAIL-036"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_WITH_OPTIONS)

    page.click_buy_button()
    page.click_option_dropdown()

    option_items = page.get_option_items()
    assert len(option_items) > 0, "Expected at least one option item"

    sold_out_flags = [page.is_option_sold_out(i) for i in range(len(option_items))]
    assert any(sold_out_flags), "Expected at least one sold-out option"
    assert not all(sold_out_flags), "Expected at least one selectable (not sold-out) option"


def test_selecting_option_updates_total_price(logged_in_driver):
    """TC-PRODUCT-DETAIL-037"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_WITH_OPTIONS)

    page.click_buy_button()
    page.click_option_dropdown()

    option_items = page.get_option_items()
    selectable_index = next(i for i in range(len(option_items)) if not page.is_option_sold_out(i))
    page.click_option_by_index(selectable_index)

    page.wait_for_text(page.QUANTITY_VALUE, "1")
    actual_quantity = page.get_quantity()
    assert actual_quantity == "1", f"Expected quantity 1, but got {actual_quantity}"

    actual_total_price = page.get_total_price()
    assert actual_total_price.endswith("원"), f"Expected total price to end with '원', but got {actual_total_price}"


def test_no_option_product_shows_quantity_directly(logged_in_driver):
    """TC-PRODUCT-DETAIL-038"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_buy_button()
    page.wait_for_text(page.QUANTITY_VALUE, "1")

    assert not page.is_option_dropdown_present(), "Expected no option dropdown for a no-option product"

    actual_quantity = page.get_quantity()
    assert actual_quantity == "1", f"Expected quantity 1, but got {actual_quantity}"


def test_quantity_minimum_boundary(logged_in_driver):
    """TC-PRODUCT-DETAIL-039"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_buy_button()
    page.wait_for_text(page.QUANTITY_VALUE, "1")

    assert page.is_quantity_decrease_disabled(), "Expected quantity decrease button to be disabled at minimum quantity"

    actual_quantity = page.get_quantity()
    assert actual_quantity == "1", f"Expected quantity to remain 1, but got {actual_quantity}"


def test_clicking_sold_out_option_is_blocked(logged_in_driver):
    """TC-PRODUCT-DETAIL-046 (Negative)"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_WITH_OPTIONS)

    page.click_buy_button()
    page.click_option_dropdown()

    option_items = page.get_option_items()
    sold_out_index = next(i for i in range(len(option_items)) if page.is_option_sold_out(i))
    page.click_option_by_index(sold_out_index)

    quantity_elements = logged_in_driver.find_elements(*page.QUANTITY_DECREASE)
    assert len(quantity_elements) == 0, "Expected no quantity UI to appear after clicking a sold-out option"


def test_on_sale_button_shows_enabled_buy_text(driver):
    """TC-PRODUCT-DETAIL-040"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    actual_text = page.get_buy_button_text()
    assert actual_text == "구매하기", f"Expected '구매하기', but got {actual_text}"
    assert page.is_buy_button_enabled(), "Expected buy button to be enabled for an on-sale product"


def test_sold_out_button_shows_disabled_and_wish_icon_active(driver):
    """TC-PRODUCT-DETAIL-042"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_SOLD_OUT)

    actual_text = page.get_buy_button_text()
    assert actual_text == "품절", f"Expected '품절', but got {actual_text}"
    assert not page.is_buy_button_enabled(), "Expected buy button to be disabled for a sold-out product"
    assert page.is_bottom_wish_icon_active(), "Expected wish icon to remain active for a sold-out product"


def test_ended_button_shows_disabled_and_wish_icon_active(driver):
    """TC-PRODUCT-DETAIL-043"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_SALE_ENDED)

    actual_text = page.get_buy_button_text()
    assert actual_text == "판매종료", f"Expected '판매종료', but got {actual_text}"
    assert not page.is_buy_button_enabled(), "Expected buy button to be disabled for an ended-sale product"
    assert page.is_bottom_wish_icon_active(), "Expected wish icon to remain active for an ended-sale product"


def test_clicking_disabled_button_has_no_effect(driver):
    """TC-PRODUCT-DETAIL-044 (Negative)"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_SOLD_OUT)

    page.try_click_disabled_buy_button()

    quantity_elements = driver.find_elements(*page.QUANTITY_DECREASE)
    assert len(quantity_elements) == 0, "Expected no purchase area to expand after clicking a disabled button"


def test_wish_icon_click_when_logged_out_shows_login_prompt(driver):
    """TC-PRODUCT-DETAIL-031"""
    page = ProductDetailPage(driver)
    page.open(PRODUCT_ID_ON_SALE)

    page.click_wish_icon()

    actual_message = page.get_login_prompt_text()
    expected_message = "로그인 후 이용해 주세요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"
    assert not page.is_wish_icon_filled(), "Expected wish icon to remain unfilled when login is required"


def test_wish_icon_click_when_logged_in_adds_wish(logged_in_driver):
    """TC-PRODUCT-DETAIL-032"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)

    if page.is_wish_icon_filled():
        page.click_wish_icon()
        page.wait_for_attribute_value(page.BOTTOM_WISH_ICON, "aria-pressed", "false")

    page.click_wish_icon()
    page.wait_for_attribute_value(page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    assert page.is_wish_icon_filled(), "Expected wish icon to be filled after clicking while logged in"

    page.click_wish_icon()  # 테스트 종료 후 찜 상태 원복
    page.wait_for_attribute_value(page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_wish_icon_re_click_removes_wish(logged_in_driver):
    """TC-PRODUCT-DETAIL-033"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)

    if not page.is_wish_icon_filled():
        page.click_wish_icon()
        page.wait_for_attribute_value(page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    page.click_wish_icon()
    page.wait_for_attribute_value(page.BOTTOM_WISH_ICON, "aria-pressed", "false")

    assert not page.is_wish_icon_filled(), "Expected wish icon to be unfilled after re-clicking"


def test_related_card_wish_icon_toggles_in_place(logged_in_driver):
    """TC-PRODUCT-DETAIL-034"""
    page = ProductDetailPage(logged_in_driver)
    page.open(PRODUCT_ID_ON_SALE)
    original_url = page.get_current_url()

    if page.is_related_card_wish_filled(index=1):
        page.click_related_card_wish_icon(index=1)
        page.wait_for_attribute_value(page.related_card_wish_icon_locator(index=1), "aria-pressed", "false")

    page.click_related_card_wish_icon(index=1)
    page.wait_for_attribute_value(page.related_card_wish_icon_locator(index=1), "aria-pressed", "true")

    assert page.is_related_card_wish_filled(index=1), "Expected related card wish icon to be filled"
    actual_url = page.get_current_url()
    assert actual_url == original_url, f"Expected no navigation, but URL changed to {actual_url}"

    page.click_related_card_wish_icon(index=1)  # 테스트 종료 후 찜 상태 원복
    page.wait_for_attribute_value(page.related_card_wish_icon_locator(index=1), "aria-pressed", "false")


def test_my_store_sections_click_enters_product_detail(logged_in_driver):
    """TC-PRODUCT-DETAIL-003"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    wished_here = False
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")
        wished_here = True

    my_store_page = MyStorePage(logged_in_driver)

    my_store_page.open()
    my_store_page.click_wish_section_product()
    my_store_page.wait_for_url_contains(f"{BASE_URL}products/")
    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"

    my_store_page.open()
    my_store_page.click_recent_section_product()
    my_store_page.wait_for_url_contains(f"{BASE_URL}products/")
    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"

    my_store_page.open()
    my_store_page.click_recommend_section_product()
    my_store_page.wait_for_url_contains(f"{BASE_URL}products/")
    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"

    if wished_here:
        product_detail_page.open(PRODUCT_ID_ON_SALE)
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_wishlist_page_item_click_enters_product_detail(logged_in_driver):
    """TC-PRODUCT-DETAIL-004"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    wished_here = False
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")
        wished_here = True

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.click_first_item()
    wishlist_page.wait_for_url_contains(f"{BASE_URL}products/")

    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"

    if wished_here:
        product_detail_page.open(PRODUCT_ID_ON_SALE)
        if product_detail_page.is_wish_icon_filled():
            product_detail_page.click_wish_icon()
            product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_cart_page_item_click_enters_product_detail(logged_in_driver):
    """TC-PRODUCT-DETAIL-005"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")
    product_detail_page.click_add_to_cart_button()

    cart_page = CartPage(logged_in_driver)
    cart_page.open()
    cart_page.click_first_item()
    cart_page.wait_for_url_contains(f"{BASE_URL}products/")

    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(f"{BASE_URL}products/"), f"Expected a product detail URL, but got {actual_url}"


def test_visiting_product_detail_records_recent_viewed(logged_in_driver):
    """TC-PRODUCT-DETAIL-045"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)

    my_store_page = MyStorePage(logged_in_driver)
    my_store_page.open()

    actual_href = my_store_page.get_recent_section_first_product_href()
    expected_href = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}"
    assert actual_href == expected_href, f"Expected {expected_href}, but got {actual_href}"
