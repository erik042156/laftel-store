import pytest

from config.settings import (
    BASE_URL,
    IP_ID_ON_SALE,
    IP_PRODUCT_ID_A,
    IP_PRODUCT_ID_B,
    PRODUCT_ID_HIGH_PRICE,
    PRODUCT_ID_ON_SALE,
    PRODUCT_ID_SOLD_OUT,
    SEARCH_KEYWORD_WITH_RESULTS,
)
from conftest import _complete_google_login
from pages.home_page import HomePage
from pages.my_store_page import MyStorePage
from pages.product_detail_page import ProductDetailPage
from pages.wishlist_page import WishlistPage


def test_main_wish_icon_click_when_logged_out_shows_login_prompt(driver):
    """TC-WISHLIST-001 (Negative)"""
    page = HomePage(driver)
    page.open()

    page.click_wish_icon(1)

    actual_message = page.get_login_prompt_text()
    expected_message = "로그인 후 이용해 주세요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"
    assert not page.is_wish_icon_filled(1), "Expected wish icon to remain unfilled when login is required"


def test_main_wish_icon_click_when_logged_in_adds_wish(logged_in_driver):
    """TC-WISHLIST-002"""
    page = HomePage(logged_in_driver)
    page.open()

    if page.is_wish_icon_filled(1):
        page.click_wish_icon(1)
        page.wait_for_wish_icon_state(1, filled=False)

    page.click_wish_icon(1)
    page.wait_for_wish_icon_state(1, filled=True)

    actual_toast = page.get_wish_toast_text()
    assert actual_toast == "찜한 상품에 추가했어요.", f"Expected wish toast text, but got {actual_toast}"
    assert page.is_wish_icon_filled(1), "Expected wish icon to be filled after clicking while logged in"

    page.click_wish_icon(1)  # 테스트 종료 후 찜 상태 원복
    page.wait_for_wish_icon_state(1, filled=False)


def test_main_wish_icon_re_click_removes_wish(logged_in_driver):
    """TC-WISHLIST-003"""
    page = HomePage(logged_in_driver)
    page.open()

    if not page.is_wish_icon_filled(1):
        page.click_wish_icon(1)
        page.wait_for_wish_icon_state(1, filled=True)

    page.click_wish_icon(1)
    page.wait_for_wish_icon_state(1, filled=False)

    assert not page.is_wish_icon_filled(1), "Expected wish icon to be unfilled after re-clicking"


def test_search_result_wish_icon_click_adds_wish(logged_in_driver):
    """TC-WISHLIST-004"""
    page = HomePage(logged_in_driver)
    page.open_search_result(SEARCH_KEYWORD_WITH_RESULTS)

    if page.is_wish_icon_filled(1):
        page.click_wish_icon(1)
        page.wait_for_wish_icon_state(1, filled=False)

    page.click_wish_icon(1)
    page.wait_for_wish_icon_state(1, filled=True)

    actual_toast = page.get_wish_toast_text()
    assert actual_toast == "찜한 상품에 추가했어요.", f"Expected wish toast text, but got {actual_toast}"
    assert page.is_wish_icon_filled(1), "Expected wish icon to be filled after clicking on search result"

    page.click_wish_icon(1)  # 테스트 종료 후 찜 상태 원복
    page.wait_for_wish_icon_state(1, filled=False)


def test_ip_page_wish_icon_click_adds_wish(logged_in_driver):
    """TC-WISHLIST-005"""
    # index=1은 작품(IP) 자체의 찜 버튼(토스트 "찜한 작품에 추가했어요.")이라 TC 대상이 아니며,
    # 이미 찜된 기존 데이터일 수 있어 건드리지 않는다. index=2부터가 실제 상품 카드의 찜 아이콘이다.
    target_index = 2
    page = HomePage(logged_in_driver)
    page.open_ip_page(IP_ID_ON_SALE)

    if page.is_wish_icon_filled(target_index):
        page.click_wish_icon(target_index)
        page.wait_for_wish_icon_state(target_index, filled=False)

    page.click_wish_icon(target_index)
    page.wait_for_wish_icon_state(target_index, filled=True)

    actual_toast = page.get_wish_toast_text()
    assert actual_toast == "찜한 상품에 추가했어요.", f"Expected wish toast text, but got {actual_toast}"
    assert page.is_wish_icon_filled(target_index), "Expected wish icon to be filled after clicking on an IP page card"

    page.click_wish_icon(target_index)  # 테스트 종료 후 찜 상태 원복
    page.wait_for_wish_icon_state(target_index, filled=False)


def test_wish_menu_badge_updates_immediately_after_adding_wish(logged_in_driver):
    """TC-WISHLIST-006"""
    target_index = 1
    page = MyStorePage(logged_in_driver)
    page.open()

    if page.is_recent_section_item_filled(target_index):
        page.click_recent_section_item_wish_icon(target_index)
        page.wait_for_recent_section_item_state(target_index, filled=False)

    before_count = int(page.get_wish_menu_badge_count())

    page.click_recent_section_item_wish_icon(target_index)
    page.wait_for_recent_section_item_state(target_index, filled=True)

    after_count = int(page.get_wish_menu_badge_count())
    assert after_count == before_count + 1, (
        f"Expected wish badge count to increase by 1 without reload, but got {before_count} -> {after_count}"
    )

    page.click_recent_section_item_wish_icon(target_index)  # 테스트 종료 후 찜 상태 원복
    page.wait_for_recent_section_item_state(target_index, filled=False)


def test_wish_section_shows_filled_wish_icons(logged_in_driver):
    """TC-WISHLIST-007"""
    page = MyStorePage(logged_in_driver)
    page.open()

    assert page.is_wish_section_item_filled(1), "Expected 찜한 상품 section card to show a filled wish icon"


def test_recent_section_shows_wish_state_and_status_badges(logged_in_driver):
    """TC-WISHLIST-008"""
    # 방문 순서(ON_SALE 미찜 -> SOLD_OUT -> HIGH_PRICE 찜)로 "최근 본 상품" 섹션의
    # 앞 3개 카드 상태를 실측 기반으로 결정적으로 구성한다(최신 방문이 index=1).
    product_detail_page = ProductDetailPage(logged_in_driver)

    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")

    product_detail_page.open(PRODUCT_ID_SOLD_OUT)

    product_detail_page.open(PRODUCT_ID_HIGH_PRICE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    my_store_page = MyStorePage(logged_in_driver)
    my_store_page.open()

    assert my_store_page.is_recent_section_item_filled(1), "Expected most recently viewed (wished) item to show a filled heart"
    assert not my_store_page.is_recent_section_item_filled(3), "Expected the not-wished item to show an empty heart"

    actual_badge = my_store_page.get_recent_section_item_status_badge_text(2)
    assert actual_badge == "품절", f"Expected sold-out status badge, but got {actual_badge}"

    product_detail_page.open(PRODUCT_ID_HIGH_PRICE)  # 테스트 종료 후 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_recent_section_wish_toggle_syncs_to_wish_section_and_wishlist_page(logged_in_driver):
    """TC-WISHLIST-009 (P0)"""
    target_index = 1
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")

    my_store_page = MyStorePage(logged_in_driver)
    my_store_page.open()
    assert PRODUCT_ID_ON_SALE in my_store_page.get_recent_section_item_href(target_index), (
        "Expected the just-viewed product to be the most recent item in 최근 본 상품"
    )

    my_store_page.click_recent_section_item_wish_icon(target_index)
    my_store_page.wait_for_recent_section_item_state(target_index, filled=True)

    assert my_store_page.is_wish_section_containing_product(PRODUCT_ID_ON_SALE), (
        "Expected the newly wished item to appear in 찜한 상품 section without reload"
    )

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    assert wishlist_page.is_product_present(PRODUCT_ID_ON_SALE), (
        "Expected the newly wished item to appear on /my/wish as well"
    )

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 테스트 종료 후 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_edit_link_only_shown_on_product_tab(logged_in_driver):
    """TC-WISHLIST-012"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)

    assert wishlist_page.is_edit_link_present(), "Expected 편집하기 link to be present on 상품 tab"

    wishlist_page.click_work_tab()
    wishlist_page.wait_for_edit_link_hidden()
    assert not wishlist_page.is_edit_link_present(), "Expected 편집하기 link to be absent on 작품 tab"

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 테스트 종료 후 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def _ensure_ip_wished(home_page, filled):
    # "작품" 탭 섹션은 상품 개별 찜과 무관하게 /ip/{id} 최상단의 작품(IP) 자체 찜
    # 버튼(index=1, AUTOMATION_GUIDE 7.11/7.13절)으로만 결정된다.
    if home_page.is_wish_icon_filled(1) != filled:
        home_page.click_wish_icon(1)
        home_page.wait_for_wish_icon_state(1, filled=filled)


def test_work_section_title_click_navigates_to_ip_page(logged_in_driver):
    """TC-WISHLIST-014"""
    home_page = HomePage(logged_in_driver)
    home_page.open_ip_page(IP_ID_ON_SALE)
    _ensure_ip_wished(home_page, filled=True)

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.click_work_tab()
    wishlist_page.wait_for_work_section_present(IP_ID_ON_SALE)
    section_index = wishlist_page.find_work_section_index(IP_ID_ON_SALE)

    wishlist_page.click_work_section_title(section_index)
    wishlist_page.wait_for_url_contains(f"ip/{IP_ID_ON_SALE}")

    actual_url = wishlist_page.get_current_url()
    expected_url = f"{BASE_URL}ip/{IP_ID_ON_SALE}"
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    home_page.open_ip_page(IP_ID_ON_SALE)  # 테스트 종료 후 작품 찜 상태 원복
    _ensure_ip_wished(home_page, filled=False)


def test_work_section_heart_click_removes_ip_wish_only(logged_in_driver):
    """TC-WISHLIST-015"""
    home_page = HomePage(logged_in_driver)
    home_page.open_ip_page(IP_ID_ON_SALE)
    _ensure_ip_wished(home_page, filled=True)

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.click_work_tab()
    wishlist_page.wait_for_work_section_present(IP_ID_ON_SALE)
    section_index = wishlist_page.find_work_section_index(IP_ID_ON_SALE)

    wishlist_page.click_work_section_heart(section_index)
    wishlist_page.wait_for_work_section_absent(IP_ID_ON_SALE)

    assert not wishlist_page.is_work_section_present(IP_ID_ON_SALE), (
        "Expected the IP section to disappear once the IP itself is unwished"
    )


def test_work_section_carousel_item_heart_click_removes_only_that_item(logged_in_driver):
    """TC-WISHLIST-016"""
    home_page = HomePage(logged_in_driver)
    home_page.open_ip_page(IP_ID_ON_SALE)
    _ensure_ip_wished(home_page, filled=True)

    product_detail_page = ProductDetailPage(logged_in_driver)
    for product_id in (IP_PRODUCT_ID_A, IP_PRODUCT_ID_B):
        product_detail_page.open(product_id)
        if not product_detail_page.is_wish_icon_filled():
            product_detail_page.click_wish_icon()
            product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.click_work_tab()
    wishlist_page.wait_for_work_section_present(IP_ID_ON_SALE)

    wishlist_page.click_product_wish_icon(IP_PRODUCT_ID_A)
    wishlist_page.wait_for_product_wish_icon_state(IP_PRODUCT_ID_A, filled=False)

    assert wishlist_page.is_work_section_present(IP_ID_ON_SALE), (
        "Expected the IP section to remain (IP-level wish is unaffected by removing one product)"
    )

    wishlist_page.click_product_tab()
    wishlist_page.wait_for_product_absent(IP_PRODUCT_ID_A)
    assert not wishlist_page.is_product_present(IP_PRODUCT_ID_A), (
        "Expected the removed item to disappear from 상품 tab without reload"
    )
    assert wishlist_page.is_product_present(IP_PRODUCT_ID_B), "Expected the still-wished item to remain on 상품 tab"

    product_detail_page.open(IP_PRODUCT_ID_B)  # 테스트 종료 후 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")

    home_page.open_ip_page(IP_ID_ON_SALE)
    _ensure_ip_wished(home_page, filled=False)


def test_sold_out_wished_item_shows_status_badge_and_opens_detail(logged_in_driver):
    """TC-WISHLIST-017"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_SOLD_OUT)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_SOLD_OUT)

    actual_badge = wishlist_page.get_product_status_badge_text(PRODUCT_ID_SOLD_OUT)
    assert actual_badge == "품절", f"Expected sold-out status badge, but got {actual_badge}"

    wishlist_page.click_product(PRODUCT_ID_SOLD_OUT)
    wishlist_page.wait_for_url_contains(f"products/{PRODUCT_ID_SOLD_OUT}")

    actual_url = wishlist_page.get_current_url()
    expected_url = f"{BASE_URL}products/{PRODUCT_ID_SOLD_OUT}"
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"

    product_detail_page.open(PRODUCT_ID_SOLD_OUT)  # 테스트 종료 후 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_edit_mode_shows_select_all_and_action_links(logged_in_driver):
    """TC-WISHLIST-020"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()

    actual_count_text = wishlist_page.get_selected_count_text()
    assert actual_count_text == "(0)", f"Expected selected count to start at (0), but got {actual_count_text}"
    assert wishlist_page.get_item_card_count() >= 1, "Expected at least one selectable item card in edit mode"
    assert len(wishlist_page.driver.find_elements(*wishlist_page.DELETE_SELECTED_LINK)) == 1, (
        "Expected 선택삭제 link to be present in edit mode"
    )
    assert len(wishlist_page.driver.find_elements(*wishlist_page.CANCEL_EDIT_LINK)) == 1, (
        "Expected 편집취소 link to be present in edit mode"
    )

    wishlist_page.click_cancel_edit()  # 테스트 종료 후 편집 모드 해제

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_select_all_checkbox_selects_all_cards(logged_in_driver):
    """TC-WISHLIST-021"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    for product_id in (IP_PRODUCT_ID_A, IP_PRODUCT_ID_B):
        product_detail_page.open(product_id)
        if not product_detail_page.is_wish_icon_filled():
            product_detail_page.click_wish_icon()
            product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(IP_PRODUCT_ID_A)
    wishlist_page.click_edit_link()

    total_count = wishlist_page.get_item_card_count()
    wishlist_page.click_select_all()

    actual_count_text = wishlist_page.get_selected_count_text()
    expected_count_text = f"({total_count})"
    assert actual_count_text == expected_count_text, (
        f"Expected all {total_count} items selected, but got {actual_count_text}"
    )
    for index in range(1, total_count + 1):
        assert wishlist_page.is_item_selected(index), f"Expected item {index} to be selected"

    wishlist_page.click_cancel_edit()  # 테스트 종료 후 편집 모드 해제

    for product_id in (IP_PRODUCT_ID_A, IP_PRODUCT_ID_B):  # 찜 상태 원복
        product_detail_page.open(product_id)
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_edit_mode_individual_card_toggle(logged_in_driver):
    """TC-WISHLIST-022"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()

    wishlist_page.click_item_card(1)
    assert wishlist_page.is_item_selected(1), "Expected item 1 to be selected after clicking"
    assert wishlist_page.get_selected_count_text() == "(1)", "Expected selected count to be (1) after selecting one item"

    wishlist_page.click_item_card(1)
    assert not wishlist_page.is_item_selected(1), "Expected item 1 to be deselected after re-clicking"
    assert wishlist_page.get_selected_count_text() == "(0)", "Expected selected count to return to (0) after deselecting"

    wishlist_page.click_cancel_edit()  # 테스트 종료 후 편집 모드 해제

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_bulk_delete_confirm_dialog_cancel_keeps_selection(logged_in_driver):
    """TC-WISHLIST-023 (Negative)"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()
    wishlist_page.click_item_card(1)

    wishlist_page.click_delete_selected()
    actual_dialog_text = wishlist_page.get_delete_confirm_dialog_text()
    assert "삭제하시겠어요?" in actual_dialog_text, f"Expected delete confirm dialog text, but got {actual_dialog_text}"
    assert "선택한 상품을 삭제합니다." in actual_dialog_text, (
        f"Expected delete confirm dialog description, but got {actual_dialog_text}"
    )

    wishlist_page.cancel_delete()

    assert wishlist_page.is_item_selected(1), "Expected selection to remain after cancelling delete"
    assert wishlist_page.get_selected_count_text() == "(1)", "Expected selected count to remain (1) after cancelling"
    assert not wishlist_page.is_edit_link_present(), "Expected to remain in edit mode after cancelling delete"

    wishlist_page.click_cancel_edit()  # 테스트 종료 후 편집 모드 해제

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_bulk_delete_confirm_removes_wish(logged_in_driver):
    """TC-WISHLIST-024"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    # 이 테스트가 방금 추가한 찜만 대상으로 삭제하도록, 항상 새로 찜을 건다(가장 최근 찜
    # 이어야 편집 모드 목록의 index=1로 결정적으로 위치함).
    if product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()
    wishlist_page.click_item_card(1)

    wishlist_page.click_delete_selected()
    wishlist_page.confirm_delete()
    wishlist_page.wait_for_product_absent(PRODUCT_ID_ON_SALE)

    assert not wishlist_page.is_product_present(PRODUCT_ID_ON_SALE), (
        "Expected the deleted item to disappear from the wishlist"
    )

    product_detail_page.open(PRODUCT_ID_ON_SALE)
    assert not product_detail_page.is_wish_icon_filled(), (
        "Expected the product to be genuinely unwished after confirmed deletion"
    )


def test_cancel_edit_exits_edit_mode(logged_in_driver):
    """TC-WISHLIST-025"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()

    wishlist_page.click_cancel_edit()

    assert wishlist_page.is_edit_link_present(), "Expected to return to normal view (편집하기 visible again)"
    assert wishlist_page.get_item_card_count() == 0, "Expected no selection overlays outside edit mode"

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_bulk_delete_click_with_no_selection_is_noop(logged_in_driver):
    """TC-WISHLIST-033 (Negative)"""
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    if not product_detail_page.is_wish_icon_filled():
        product_detail_page.click_wish_icon()
        product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "true")

    wishlist_page = WishlistPage(logged_in_driver)
    wishlist_page.open()
    wishlist_page.wait_for_product_present(PRODUCT_ID_ON_SALE)
    wishlist_page.click_edit_link()

    wishlist_page.click_delete_selected()

    assert len(wishlist_page.driver.find_elements(*wishlist_page.DELETE_CONFIRM_DIALOG)) == 0, (
        "Expected no confirm dialog when nothing is selected"
    )
    assert wishlist_page.get_selected_count_text() == "(0)", "Expected selected count to remain (0)"
    assert not wishlist_page.is_edit_link_present(), "Expected to remain in edit mode (no screen change)"

    wishlist_page.click_cancel_edit()  # 테스트 종료 후 편집 모드 해제

    product_detail_page.open(PRODUCT_ID_ON_SALE)  # 찜 상태 원복
    product_detail_page.click_wish_icon()
    product_detail_page.wait_for_attribute_value(product_detail_page.BOTTOM_WISH_ICON, "aria-pressed", "false")


def test_unauthenticated_my_page_loads_and_wish_menu_shows_login_prompt(driver):
    """TC-WISHLIST-026"""
    my_store_page = MyStorePage(driver)
    my_store_page.open()

    actual_url = my_store_page.get_current_url()
    assert actual_url == f"{BASE_URL}my", f"Expected {BASE_URL}my, but got {actual_url}"

    my_store_page.click_wish_menu()

    actual_message = my_store_page.get_login_prompt_text()
    expected_message = "로그인 후 이용해 주세요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"


def test_unauthenticated_direct_wishlist_url_shows_login_prompt(driver):
    """TC-WISHLIST-027"""
    wishlist_page = WishlistPage(driver)
    wishlist_page.open()

    actual_message = wishlist_page.get_login_prompt_text()
    expected_message = "로그인 후 이용해 주세요."
    assert actual_message == expected_message, f"Expected {expected_message}, but got {actual_message}"


def test_direct_entry_login_prompt_cancel_navigates_to_main_page(driver):
    """TC-WISHLIST-028"""
    wishlist_page = WishlistPage(driver)
    wishlist_page.open()
    wishlist_page.get_login_prompt_text()

    wishlist_page.click_login_prompt_cancel()
    wishlist_page.wait_for_url_to_be(BASE_URL)

    actual_url = wishlist_page.get_current_url()
    assert actual_url == BASE_URL, f"Expected {BASE_URL}, but got {actual_url}"


def test_site_entry_login_prompt_cancel_keeps_previous_screen(driver):
    """TC-WISHLIST-029"""
    my_store_page = MyStorePage(driver)
    my_store_page.open()
    my_store_page.click_wish_menu()
    my_store_page.get_login_prompt_text()

    my_store_page.click_login_prompt_cancel()

    actual_url = my_store_page.get_current_url()
    expected_url = f"{BASE_URL}my"
    assert actual_url == expected_url, f"Expected to remain on {expected_url}, but got {actual_url}"


def test_login_prompt_login_button_navigates_to_login_page(driver):
    """TC-WISHLIST-030"""
    wishlist_page = WishlistPage(driver)
    wishlist_page.open()
    wishlist_page.get_login_prompt_text()

    wishlist_page.click_login_prompt_login()
    wishlist_page.wait_for_url_contains("auth/login")

    actual_url = wishlist_page.get_current_url()
    assert "auth/login" in actual_url, f"Expected a login page URL, but got {actual_url}"


@pytest.mark.requires_real_browser
def test_direct_entry_login_completes_to_original_destination(driver):
    """TC-WISHLIST-031"""
    wishlist_page = WishlistPage(driver)
    wishlist_page.open()
    wishlist_page.get_login_prompt_text()

    wishlist_page.click_login_prompt_login()
    wishlist_page.wait_for_url_contains("auth/login")

    _complete_google_login(driver)

    actual_url = wishlist_page.get_current_url()
    expected_url = f"{BASE_URL}my/wish"
    assert actual_url == expected_url, f"Expected to land on {expected_url}, but got {actual_url}"


@pytest.mark.requires_real_browser
def test_site_entry_login_completes_to_previous_screen(driver):
    """TC-WISHLIST-032"""
    my_store_page = MyStorePage(driver)
    my_store_page.open()
    my_store_page.click_wish_menu()
    my_store_page.get_login_prompt_text()

    my_store_page.click_login_prompt_login()
    my_store_page.wait_for_url_contains("auth/login")

    _complete_google_login(driver)

    actual_url = my_store_page.get_current_url()
    expected_url = f"{BASE_URL}my"
    assert actual_url == expected_url, f"Expected to land on {expected_url} (not /my/wish), but got {actual_url}"
