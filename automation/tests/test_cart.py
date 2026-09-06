from config.settings import BASE_URL, PRODUCT_ID_HIGH_PRICE, PRODUCT_ID_ON_SALE, PRODUCT_ID_WITH_OPTIONS
from pages.cart_page import CartPage
from pages.product_detail_page import ProductDetailPage


def _add_product_to_cart(driver, product_id):
    page = ProductDetailPage(driver)
    page.open(product_id)
    page.click_buy_button()

    if product_id == PRODUCT_ID_WITH_OPTIONS:
        # 구매하기 클릭 직후 옵션 드롭다운이 이미 펼쳐진 상태이며, 옵션을 선택해야만
        # 수량 UI가 나타난다(product_detail_page.click_option_dropdown 참고).
        page.click_option_dropdown()
        option_items = page.get_option_items()
        selectable_index = next(i for i in range(len(option_items)) if not page.is_option_sold_out(i))
        page.click_option_by_index(selectable_index)

    page.wait_for_text(page.QUANTITY_VALUE, "1")
    page.click_add_to_cart_button()
    # 담기 API 호출이 끝나기 전에 다음 페이지로 이동하면 담기가 취소될 수 있어,
    # 완료를 알리는 토스트가 뜰 때까지 기다린 뒤에 넘어간다.
    page.get_add_to_cart_toast_text()


def test_empty_cart_shows_empty_message(logged_in_driver):
    """TC-CART-022"""
    cart_page = CartPage(logged_in_driver)
    # 이전 테스트/디버깅 세션에서 남은 잔여 상품이 있을 수 있으므로, 빈 카트라는
    # 이 테스트의 Precondition을 스스로 보장한다(테스트 격리/재현성 원칙).
    cart_page.clear_cart()

    assert cart_page.is_empty(), "Expected cart to be empty for this test's precondition"

    actual_message = cart_page.get_empty_message_text()
    expected_message = "장바구니에 담긴 상품이 아직 없어요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"


def test_cart_icon_and_direct_url_navigate_to_cart(logged_in_driver):
    """TC-CART-002"""
    expected_url = f"{BASE_URL}cart"

    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_cart_icon()
    product_detail_page.wait_for_url_contains(expected_url)

    actual_url = logged_in_driver.current_url
    assert actual_url.startswith(expected_url), f"Expected URL to start with {expected_url}, but got {actual_url}"

    cart_page = CartPage(logged_in_driver)
    cart_page.open()

    actual_url = logged_in_driver.current_url
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"


def test_adding_to_cart_shows_toast_and_badge(logged_in_driver):
    """TC-CART-001"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")

    product_detail_page.click_add_to_cart_button()

    actual_toast = product_detail_page.get_add_to_cart_toast_text()
    assert "장바구니에 상품을 담았어요" in actual_toast, (
        f"Expected toast to contain '장바구니에 상품을 담았어요', but got {actual_toast}"
    )
    assert "보러가기" in actual_toast, f"Expected toast to contain '보러가기', but got {actual_toast}"

    actual_badge = product_detail_page.get_cart_icon_badge_count()
    assert actual_badge == "1", f"Expected cart badge to show '1', but got {actual_badge}"


def test_individual_delete_with_confirm_removes_item(logged_in_driver):
    """TC-CART-018"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    initial_count = cart_page.get_item_count()
    assert initial_count == 2, f"Expected 2 items in cart precondition, but got {initial_count}"

    cart_page.click_individual_delete(index=1)

    actual_heading = cart_page.get_delete_confirm_heading_text()
    expected_heading = "선택한 상품을 삭제하시겠어요?"
    assert actual_heading == expected_heading, f"Expected {expected_heading}, but got {actual_heading}"

    cart_page.confirm_delete()
    cart_page.wait_for_item_count(1)

    remaining_count = cart_page.get_item_count()
    assert remaining_count == 1, f"Expected 1 item to remain after deleting one, but got {remaining_count}"

    cart_page.clear_cart()


def test_individual_delete_cancel_keeps_item(logged_in_driver):
    """TC-CART-019"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    initial_count = cart_page.get_item_count()
    assert initial_count == 1, f"Expected 1 item in cart precondition, but got {initial_count}"

    cart_page.click_individual_delete(index=1)
    cart_page.get_delete_confirm_heading_text()

    cart_page.cancel_delete()

    remaining_count = cart_page.get_item_count()
    assert remaining_count == 1, f"Expected item to remain after cancel, but got {remaining_count}"
    assert not cart_page.is_empty(), "Expected cart to remain non-empty after cancelling delete"

    cart_page.clear_cart()


def test_bulk_delete_removes_selected_items(logged_in_driver):
    """TC-CART-020"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    initial_count = cart_page.get_item_count()
    assert initial_count == 2, f"Expected 2 items in cart precondition, but got {initial_count}"

    cart_page.ensure_all_selected()
    cart_page.click_bulk_delete()

    actual_heading = cart_page.get_delete_confirm_heading_text()
    expected_heading = "선택한 상품을 삭제하시겠어요?"
    assert actual_heading == expected_heading, f"Expected {expected_heading}, but got {actual_heading}"

    cart_page.confirm_delete()
    cart_page.wait_for_item_count(0)

    assert cart_page.is_empty(), "Expected all selected items to be removed after bulk delete"


def _parse_won(text):
    return int(text.replace(",", "").replace("원", ""))


def test_payment_summary_shows_all_line_items(logged_in_driver):
    """TC-CART-009"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()

    actual_payment_total = cart_page.get_payment_total_price()
    actual_product_total = cart_page.get_product_total_price()
    actual_shipping_fee = cart_page.get_shipping_fee_text()
    actual_discount = cart_page.get_product_discount_text()

    for label, value in (
        ("결제금액", actual_payment_total),
        ("총 상품 금액", actual_product_total),
        ("배송비", actual_shipping_fee),
        ("상품 할인", actual_discount),
    ):
        assert value.endswith("원"), f"Expected {label} to end with '원', but got {value}"

    expected_payment_total = _parse_won(actual_product_total) + _parse_won(actual_shipping_fee) + _parse_won(
        actual_discount
    )
    assert _parse_won(actual_payment_total) == expected_payment_total, (
        f"Expected 결제금액 {expected_payment_total}, but got {_parse_won(actual_payment_total)}"
    )

    cart_page.clear_cart()


def test_bottom_buy_button_shows_amount_and_selected_count(logged_in_driver):
    """TC-CART-010"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()

    # 상품 2종 중 1건만 선택된 상태로 전환한다(N은 카드 수 기준임을 검증하기 위함).
    cart_page.click_item_checkbox(index=2)

    actual_count = cart_page.get_bottom_buy_button_count()
    assert actual_count == "1", f"Expected selected card count '1', but got {actual_count}"

    actual_button_text = cart_page.get_bottom_buy_button_text()
    assert "구매하기" in actual_button_text, f"Expected button text to contain '구매하기', but got {actual_button_text}"

    actual_payment_total = cart_page.get_payment_total_price()
    assert actual_payment_total in actual_button_text, (
        f"Expected button text to contain payment total {actual_payment_total}, but got {actual_button_text}"
    )

    cart_page.clear_cart()


def test_two_or_more_items_over_threshold_shows_free_bundled_shipping(logged_in_driver):
    """TC-CART-007"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    # 합산 100,000원 이상을 만들기 위해 고가 상품(PRODUCT_ID_HIGH_PRICE, 344,000원)과
    # 저가 상품을 각 1개씩 담는다(재고 상한을 피하기 위해 수량 증가는 사용하지 않음).
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_HIGH_PRICE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()

    actual_notice = cart_page.get_shipping_notice_text()
    assert "묶음배송비 무료" in actual_notice, f"Expected '묶음배송비 무료' in notice, but got {actual_notice}"

    cart_page.clear_cart()


def test_single_item_under_threshold_shows_individual_shipping_notice(logged_in_driver):
    """TC-CART-008"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()

    # 상품 2종 중 1건만 선택된 상태로 전환한다(선택 금액이 100,000원 미만인 상태).
    cart_page.click_item_checkbox(index=2)

    actual_notice = cart_page.get_shipping_notice_text()
    assert "배송비 3,000원" in actual_notice, f"Expected '배송비 3,000원' in notice, but got {actual_notice}"
    assert "묶음배송비 무료" not in actual_notice, f"Expected notice not to say free shipping, but got {actual_notice}"
    assert "100,000원 이상 무료배송" in actual_notice, (
        f"Expected '100,000원 이상 무료배송' in notice, but got {actual_notice}"
    )

    cart_page.clear_cart()


def test_individual_checkbox_updates_header_and_bottom_button(logged_in_driver):
    """TC-CART-012"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()

    initial_label = cart_page.get_select_all_label_text()
    assert initial_label == "전체선택 (2/2)", f"Expected '전체선택 (2/2)', but got {initial_label}"

    cart_page.click_item_checkbox(index=1)
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(1/2)")

    actual_label = cart_page.get_select_all_label_text()
    assert actual_label == "전체선택 (1/2)", f"Expected '전체선택 (1/2)', but got {actual_label}"

    actual_count = cart_page.get_bottom_buy_button_count()
    assert actual_count == "1", f"Expected bottom button count '1', but got {actual_count}"

    cart_page.clear_cart()


def test_seller_group_checkbox_toggles_group_items(logged_in_driver):
    """TC-CART-013"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()

    cart_page.click_seller_group_checkbox()
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(0/2)")
    assert not cart_page.is_item_checked(index=1), "Expected item 1 to be unchecked after group deselect"
    assert not cart_page.is_item_checked(index=2), "Expected item 2 to be unchecked after group deselect"

    cart_page.click_seller_group_checkbox()
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(2/2)")
    assert cart_page.is_item_checked(index=1), "Expected item 1 to be checked after group select"
    assert cart_page.is_item_checked(index=2), "Expected item 2 to be checked after group select"

    cart_page.clear_cart()


def test_select_all_checkbox_toggles_all_items(logged_in_driver):
    """TC-CART-014"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)
    _add_product_to_cart(logged_in_driver, PRODUCT_ID_WITH_OPTIONS)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()

    cart_page.click_select_all()
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(0/2)")
    assert not cart_page.is_item_checked(index=1), "Expected item 1 to be unchecked after select-all toggle off"
    assert not cart_page.is_item_checked(index=2), "Expected item 2 to be unchecked after select-all toggle off"

    cart_page.click_select_all()
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(2/2)")
    assert cart_page.is_item_checked(index=1), "Expected item 1 to be checked after select-all toggle on"
    assert cart_page.is_item_checked(index=2), "Expected item 2 to be checked after select-all toggle on"

    cart_page.clear_cart()


def test_quantity_change_updates_item_and_total_amount(logged_in_driver):
    """TC-CART-015"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()

    initial_amount = cart_page.get_item_amount_text(index=1)
    initial_total = cart_page.get_payment_total_price()

    cart_page.increase_quantity(index=1)
    cart_page.wait_for_text(cart_page.quantity_value_locator(1), "2")

    increased_amount = cart_page.get_item_amount_text(index=1)
    increased_total = cart_page.get_payment_total_price()
    assert _parse_won(increased_amount) == _parse_won(initial_amount) * 2, (
        f"Expected item amount to double, but got {increased_amount} from {initial_amount}"
    )
    assert _parse_won(increased_total) > _parse_won(initial_total), (
        f"Expected payment total to increase, but got {increased_total} from {initial_total}"
    )

    cart_page.decrease_quantity(index=1)
    cart_page.wait_for_text(cart_page.quantity_value_locator(1), "1")

    final_amount = cart_page.get_item_amount_text(index=1)
    final_total = cart_page.get_payment_total_price()
    assert final_amount == initial_amount, f"Expected item amount to revert to {initial_amount}, but got {final_amount}"
    assert final_total == initial_total, f"Expected payment total to revert to {initial_total}, but got {final_total}"

    cart_page.clear_cart()


def test_quantity_minimum_boundary_disables_decrease_button(logged_in_driver):
    """TC-CART-016 (Boundary/Negative)"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()

    assert cart_page.is_quantity_decrease_disabled(index=1), "Expected '-' button to be disabled at minimum quantity"

    cart_page.try_click_disabled_quantity_decrease(index=1)

    actual_quantity = cart_page.get_quantity(index=1)
    assert actual_quantity == "1", f"Expected quantity to remain 1, but got {actual_quantity}"

    dialog_elements = logged_in_driver.find_elements(*cart_page.DELETE_CONFIRM_DIALOG_HEADING)
    assert len(dialog_elements) == 0, "Expected no delete confirm dialog to appear"

    cart_page.clear_cart()


def test_clicking_buy_button_with_zero_selected_shows_guide_popup(logged_in_driver):
    """TC-CART-023 (Negative/상태 위반)"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    _add_product_to_cart(logged_in_driver, PRODUCT_ID_ON_SALE)

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()

    cart_page.click_select_all()
    cart_page.wait_for_text(cart_page.SELECT_ALL_LABEL, "(0/1)")

    before_url = logged_in_driver.current_url
    cart_page.click_bottom_buy_button()

    actual_dialog_text = cart_page.get_guide_dialog_text()
    expected_text = "구매할 상품을 선택해 주세요."
    assert actual_dialog_text == expected_text, f"Expected {expected_text}, but got {actual_dialog_text}"

    cart_page.click_guide_dialog_confirm()

    after_url = logged_in_driver.current_url
    assert after_url == before_url, f"Expected to remain on {before_url}, but got {after_url}"
    assert not cart_page.is_empty(), "Expected cart screen to remain with the item still present"

    cart_page.clear_cart()
