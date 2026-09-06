from config.settings import BASE_URL, PRODUCT_ID_ON_SALE
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.product_detail_page import ProductDetailPage


def test_buy_now_button_navigates_to_checkout(logged_in_driver):
    """TC-ORDER-001"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")
    product_detail_page.click_buy_now_button()

    product_detail_page.wait_for_url_contains(f"{BASE_URL}check-out/")

    checkout_page = CheckoutPage(logged_in_driver)
    actual_url = checkout_page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}check-out/"), f"Expected a checkout URL, but got {actual_url}"


def test_cart_buy_button_navigates_to_checkout(logged_in_driver):
    """TC-ORDER-002"""
    cart_page = CartPage(logged_in_driver)
    cart_page.clear_cart()

    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")
    product_detail_page.click_add_to_cart_button()
    product_detail_page.get_add_to_cart_toast_text()

    cart_page.open()
    cart_page.wait_for_items_loaded()
    cart_page.ensure_all_selected()
    cart_page.click_bottom_buy_button()

    cart_page.wait_for_url_contains(f"{BASE_URL}check-out/")

    checkout_page = CheckoutPage(logged_in_driver)
    actual_url = checkout_page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}check-out/"), f"Expected a checkout URL, but got {actual_url}"

    # 카트 경유 진입은 결제 화면으로 이동해도 카트에 담긴 상품이 그대로 남아있어,
    # 다음 테스트를 위해 정리한다.
    cart_page.clear_cart()


def _go_to_checkout(driver):
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")
    product_detail_page.click_buy_now_button()
    product_detail_page.wait_for_url_contains(f"{BASE_URL}check-out/")


def test_shipping_section_shows_all_fields(logged_in_driver):
    """TC-ORDER-004"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    assert checkout_page.get_recipient_name_placeholder() == "이름을 입력해 주세요.", "Expected recipient name placeholder"
    assert checkout_page.get_phone_placeholder() == "숫자만 입력해 주세요.", "Expected phone placeholder"
    assert checkout_page.get_zip_code_placeholder() == "우편번호", "Expected zip code placeholder"
    assert checkout_page.get_address_placeholder() == "주소", "Expected address placeholder"

    actual_shipping_request = checkout_page.get_shipping_request_value_text()
    assert actual_shipping_request == "문 앞에 놓아주세요.", (
        f"Expected default shipping request '문 앞에 놓아주세요.', but got {actual_shipping_request}"
    )


def test_submitting_empty_form_shows_field_errors(logged_in_driver):
    """TC-ORDER-005 (Negative)"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    # 이 테스트 계정은 Phase3-E/F 검증 과정에서 실제 배송지를 입력한 이력이 있어
    # 체크아웃 화면이 "최근 배송지"를 자동으로 채워준다(REQ-ORDER-020, TC-ORDER-021
    # 참고). 받는 사람/휴대폰번호는 편집 가능해 명시적으로 비워 검증하지만, 우편번호/
    # 주소는 readonly라 카카오 모달 없이는 다시 빈 값으로 되돌릴 수 없어 이 테스트에서는
    # 검증하지 않는다(AUTOMATION_GUIDE 7.10절 참고).
    checkout_page.clear_recipient_name()
    checkout_page.clear_phone()
    checkout_page.click_buy_button()

    actual_name_error = checkout_page.get_name_error_text()
    assert actual_name_error == "이름을 확인해 주세요.", f"Expected name error, but got {actual_name_error}"

    actual_phone_error = checkout_page.get_phone_error_text()
    assert actual_phone_error == "휴대폰번호를 확인해 주세요.", f"Expected phone error, but got {actual_phone_error}"


def test_phone_field_strips_non_numeric_characters(logged_in_driver):
    """TC-ORDER-007 (Negative/Boundary)"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.type_phone("abc123가나다")

    actual_value = checkout_page.get_phone_value()
    assert actual_value == "123", f"Expected only digits '123' to remain, but got {actual_value}"


def test_shipping_request_direct_input_shows_textarea_and_counter(logged_in_driver):
    """TC-ORDER-009"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.click_shipping_request_dropdown()
    checkout_page.click_shipping_request_direct_input()

    actual_value_text = checkout_page.get_shipping_request_value_text()
    assert actual_value_text == "직접입력", f"Expected dropdown value '직접입력', but got {actual_value_text}"

    actual_counter = checkout_page.get_shipping_request_char_count_text()
    assert actual_counter == "0", f"Expected char counter to start at '0', but got {actual_counter}"


def test_shipping_request_direct_input_blocks_over_50_chars(logged_in_driver):
    """TC-ORDER-020 (Boundary)"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.click_shipping_request_dropdown()
    checkout_page.click_shipping_request_direct_input()

    checkout_page.type_shipping_request_text("가" * 50)
    actual_counter = checkout_page.get_shipping_request_char_count_text()
    assert actual_counter == "50", f"Expected char counter '50', but got {actual_counter}"

    checkout_page.type_shipping_request_text("X")

    actual_value = checkout_page.get_shipping_request_text_value()
    assert len(actual_value) == 50, f"Expected text to remain at 50 chars, but got {len(actual_value)}"

    assert checkout_page.is_shipping_request_char_count_warning(), "Expected char counter to show warning color"


def _parse_won(text):
    return int(text.replace(",", "").replace("원", ""))


def test_payment_summary_shows_all_line_items(logged_in_driver):
    """TC-ORDER-015"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    actual_payment_total = checkout_page.get_payment_total_price()
    actual_product_total = checkout_page.get_product_total_price()
    actual_shipping_fee = checkout_page.get_shipping_fee_text()
    actual_discount = checkout_page.get_product_discount_text()

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


def test_bottom_buy_button_shows_amount_and_product_type_count(logged_in_driver):
    """TC-ORDER-018"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_buy_button()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "1")
    product_detail_page.increase_quantity()
    product_detail_page.wait_for_text(product_detail_page.QUANTITY_VALUE, "2")
    product_detail_page.click_buy_now_button()
    product_detail_page.wait_for_url_contains(f"{BASE_URL}check-out/")

    checkout_page = CheckoutPage(logged_in_driver)
    actual_count = checkout_page.get_buy_button_count()
    assert actual_count == "1", f"Expected product type count '1' (not quantity 2), but got {actual_count}"

    actual_button_text = checkout_page.get_buy_button_text()
    actual_payment_total = checkout_page.get_payment_total_price()
    assert actual_payment_total in actual_button_text, (
        f"Expected button text to contain payment total {actual_payment_total}, but got {actual_button_text}"
    )
    assert "구매하기" in actual_button_text, f"Expected button text to contain '구매하기', but got {actual_button_text}"


def test_submitting_without_agreements_shows_guide_popup(logged_in_driver):
    """TC-ORDER-017 (Negative)"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.type_recipient_name("홍길동")
    checkout_page.type_phone("01012345678")
    # address1/zipCode 입력란이 readonly라 유효한 배송지를 갖추려면 카카오 우편번호
    # 검색을 거쳐야 한다(사용자 승인 하에 최소 조작으로만 사용, TC-ORDER-006 자체는
    # 검증하지 않음).
    checkout_page.fill_address_via_kakao_postcode_search("테헤란로 152")
    checkout_page.ensure_all_agreements_unchecked()

    before_url = checkout_page.get_current_url()
    checkout_page.click_buy_button()

    actual_dialog_text = checkout_page.get_agreement_guide_dialog_text()
    assert "결제에 동의해 주세요" in actual_dialog_text, (
        f"Expected agreement guide popup text, but got {actual_dialog_text}"
    )

    checkout_page.click_agreement_guide_dialog_confirm()

    after_url = checkout_page.get_current_url()
    assert after_url == before_url, f"Expected to remain on {before_url}, but got {after_url}"


def test_previously_saved_shipping_info_is_prefilled(logged_in_driver):
    """TC-ORDER-021"""
    _go_to_checkout(logged_in_driver)

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.wait_for_shipping_info_prefilled()

    actual_name = checkout_page.get_recipient_name_value()
    assert actual_name != "", "Expected recipient name to be prefilled from saved shipping info"

    actual_phone = checkout_page.get_phone_value()
    assert actual_phone != "", "Expected phone to be prefilled from saved shipping info"

    actual_zip_code = checkout_page.get_zip_code_value()
    assert actual_zip_code != "", "Expected zip code to be prefilled from saved shipping info"

    actual_address = checkout_page.get_address_value()
    assert actual_address != "", "Expected address to be prefilled from saved shipping info"
