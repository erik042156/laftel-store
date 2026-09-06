import urllib.parse

from config.settings import (
    BASE_URL,
    PRODUCT_ID_ON_SALE,
    PRODUCT_ID_SEARCH_SALE_ENDED,
    PRODUCT_ID_SOLD_OUT,
    SEARCH_KEYWORD_SALE_ENDED_PRODUCT,
    SEARCH_KEYWORD_SOLD_OUT_PRODUCT,
    SEARCH_KEYWORD_WITH_RESULTS,
    SEARCH_KEYWORD_WITH_STATUS_PRODUCTS,
)
from pages.home_page import HomePage
from pages.ip_page import IpPage
from pages.product_detail_page import ProductDetailPage
from pages.search_page import SearchPage
from pages.search_result_page import SearchResultPage


def _search_and_reveal_recent(search_page, keyword):
    # 검색 실행으로 최근 검색어 이력을 남긴 뒤, 검색페이지에 새로 진입해 검색어를
    # 입력했다가 지워서(clear_keyword) "최근 검색" 영역을 노출시킨다(실측 확인된 트리거).
    search_page.open()
    search_page.type_keyword(keyword)
    search_page.submit_search()

    search_page.open()
    search_page.type_keyword("x")
    search_page.clear_keyword()
    search_page.wait_for_recent_search_keyword_present(keyword)


def test_main_search_entry_click_navigates_to_search_page(driver):
    """TC-SEARCH-001"""
    home_page = HomePage(driver)
    home_page.open()

    home_page.click_search_entry()

    search_page = SearchPage(driver)
    search_page.wait_for_url_contains("search")
    actual_url = search_page.get_current_url()
    expected_url = f"{BASE_URL}search"
    assert actual_url == expected_url, f"Expected {expected_url}, but got {actual_url}"
    assert search_page.is_initial_screen_displayed(), "Expected search page initial screen to be displayed"


def test_direct_url_entry_shows_search_initial_screen(driver):
    """TC-SEARCH-002"""
    search_page = SearchPage(driver)
    search_page.open()

    assert search_page.is_initial_screen_displayed(), "Expected search page initial screen to be displayed"


def test_autocomplete_shows_work_badge_and_related_keyword_sections(driver):
    """TC-SEARCH-003"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword(SEARCH_KEYWORD_WITH_RESULTS)
    search_page.wait_for_autocomplete_related_keywords_present()

    work_items = search_page.get_autocomplete_work_item_texts()
    related_items = search_page.get_autocomplete_related_keyword_texts()
    assert len(work_items) > 0, "Expected at least one '작품' badge autocomplete item"
    assert len(related_items) > 0, "Expected at least one related keyword autocomplete item without a badge"


def test_autocomplete_updates_in_real_time_while_editing(driver):
    """TC-SEARCH-008"""
    search_page = SearchPage(driver)
    search_page.open()

    first_char, remaining_chars = SEARCH_KEYWORD_WITH_RESULTS[0], SEARCH_KEYWORD_WITH_RESULTS[1:]

    search_page.type_keyword(first_char)
    search_page.wait_for_autocomplete_related_keywords_present()
    broad_related_items = search_page.get_autocomplete_related_keyword_texts()

    search_page.append_to_keyword(remaining_chars)
    search_page.wait_for_autocomplete_related_keywords_change(broad_related_items)
    narrowed_related_items = search_page.get_autocomplete_related_keyword_texts()
    assert narrowed_related_items != broad_related_items, "Expected autocomplete to update after typing more text"

    search_page.backspace_keyword(len(remaining_chars))
    search_page.wait_for_autocomplete_related_keywords_change(narrowed_related_items)
    reverted_related_items = search_page.get_autocomplete_related_keyword_texts()
    assert reverted_related_items == broad_related_items, "Expected autocomplete to revert after deleting text"


def test_autocomplete_work_badge_click_navigates_to_ip_page(driver):
    """TC-SEARCH-006"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword(SEARCH_KEYWORD_WITH_RESULTS)
    search_page.wait_for_autocomplete_related_keywords_present()
    search_page.click_autocomplete_work_item(1)

    ip_page = IpPage(driver)
    ip_page.wait_for_url_contains("/ip/")
    assert "/ip/" in ip_page.get_current_url(), f"Expected to navigate to an /ip/ page, got {ip_page.get_current_url()}"
    assert ip_page.is_screen_displayed(), "Expected IP page banner/title/count/sort/grid to be displayed"


def test_autocomplete_related_keyword_click_navigates_to_search_result(driver):
    """TC-SEARCH-007"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword(SEARCH_KEYWORD_WITH_RESULTS)
    search_page.wait_for_autocomplete_related_keywords_present()
    search_page.click_autocomplete_related_keyword_item(1)

    search_result_page = SearchResultPage(driver)
    search_result_page.wait_for_url_contains("keyword=")
    actual_url = search_result_page.get_current_url()
    assert actual_url.startswith(f"{BASE_URL}search?keyword="), f"Expected search result URL, got {actual_url}"
    assert "/ip/" not in actual_url, f"Expected a search result page, not an IP page, got {actual_url}"
    assert search_result_page.is_screen_displayed(), "Expected search result screen to be displayed"


def test_search_result_shows_basic_layout_and_total_count(driver):
    """TC-SEARCH-009"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_WITH_RESULTS)

    search_result_page = SearchResultPage(driver)
    assert search_result_page.is_screen_displayed(), "Expected search result screen to be displayed"

    total_count = search_result_page.get_total_count()
    assert total_count > 0, "Expected total count to be a positive number"

    loaded_count = search_result_page.load_all_grid_items(total_count)
    assert loaded_count == total_count, f"Expected grid item count to reach total count {total_count}, got {loaded_count}"


def test_search_result_top_work_card_click_navigates_to_ip_page(driver):
    """TC-SEARCH-010"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_WITH_RESULTS)

    search_result_page = SearchResultPage(driver)
    search_result_page.click_top_work_card()

    ip_page = IpPage(driver)
    ip_page.wait_for_url_contains("/ip/")
    assert "/ip/" in ip_page.get_current_url(), f"Expected to navigate to an /ip/ page, got {ip_page.get_current_url()}"


def test_search_result_sort_dropdown_options_and_selection_check(driver):
    """TC-SEARCH-011"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_WITH_RESULTS)

    search_result_page = SearchResultPage(driver)
    assert search_result_page.get_sort_trigger_text() == "인기순", "Expected default sort to be 인기순"

    search_result_page.click_sort_trigger()
    assert search_result_page.is_sort_dialog_open(), "Expected sort dropdown dialog to be open"
    option_texts = search_result_page.get_sort_option_texts()
    assert option_texts == ["인기순", "최신순"], f"Expected exactly [인기순, 최신순], got {option_texts}"
    assert search_result_page.is_sort_cancel_button_present(), "Expected a 취소 button in the sort dropdown"
    assert search_result_page.is_sort_option_selected("인기순"), "Expected 인기순 to be initially checked"

    search_result_page.click_sort_option("최신순")
    search_result_page.wait_for_sort_dialog_closed()
    assert search_result_page.get_sort_trigger_text() == "최신순", "Expected trigger label to update to 최신순"

    search_result_page.click_sort_trigger()
    assert search_result_page.is_sort_option_selected("최신순"), "Expected 최신순 to be checked after reopening"
    assert not search_result_page.is_sort_option_selected("인기순"), "Expected 인기순 to no longer be checked"


def test_search_result_shows_ended_status_products_alongside_normal_products(driver):
    """TC-SEARCH-012"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_WITH_STATUS_PRODUCTS)

    search_result_page = SearchResultPage(driver)
    item_texts = search_result_page.get_grid_item_texts()
    ended_items = [t for t in item_texts if "품절" in t or "판매종료" in t]
    normal_items = [t for t in item_texts if "품절" not in t and "판매종료" not in t]
    assert len(ended_items) > 0, "Expected at least one 품절/판매종료 product to be shown, not hidden"
    assert len(normal_items) > 0, "Expected ended-status products to be shown alongside normal products"


def test_search_result_sale_ended_product_click_shows_disabled_button_and_active_wish_icon(driver):
    """TC-SEARCH-013"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_SALE_ENDED_PRODUCT)

    search_result_page = SearchResultPage(driver)
    search_result_page.click_product_card(PRODUCT_ID_SEARCH_SALE_ENDED)

    product_detail_page = ProductDetailPage(driver)
    product_detail_page.wait_for_url_contains(f"products/{PRODUCT_ID_SEARCH_SALE_ENDED}")
    actual_button_text = product_detail_page.get_buy_button_text()
    assert actual_button_text == "판매종료", f"Expected 판매종료 button text, got {actual_button_text}"
    assert not product_detail_page.is_buy_button_enabled(), "Expected 판매종료 button to be disabled"
    assert product_detail_page.is_bottom_wish_icon_active(), "Expected wish icon to remain active"


def test_search_result_sold_out_product_click_shows_disabled_button_and_active_wish_icon(driver):
    """TC-SEARCH-014"""
    home_page = HomePage(driver)
    home_page.open_search_result(SEARCH_KEYWORD_SOLD_OUT_PRODUCT)

    search_result_page = SearchResultPage(driver)
    search_result_page.click_product_card(PRODUCT_ID_SOLD_OUT)

    product_detail_page = ProductDetailPage(driver)
    product_detail_page.wait_for_url_contains(f"products/{PRODUCT_ID_SOLD_OUT}")
    actual_button_text = product_detail_page.get_buy_button_text()
    assert actual_button_text == "품절", f"Expected 품절 button text, got {actual_button_text}"
    assert not product_detail_page.is_buy_button_enabled(), "Expected 품절 button to be disabled"
    assert product_detail_page.is_bottom_wish_icon_active(), "Expected wish icon to remain active"


def test_search_no_results_keyword_shows_empty_state(driver):
    """TC-SEARCH-015"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword("asdkjfhqwlekjzxcvasdf12345")
    search_page.submit_search()

    search_result_page = SearchResultPage(driver)
    search_result_page.wait_for_url_contains("keyword=")
    assert search_result_page.is_empty_state_displayed(), "Expected empty-state message to be displayed"


def test_search_blank_keyword_does_not_execute_search(driver):
    """TC-SEARCH-016 (Negative)"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword("   ")
    search_page.submit_search()

    actual_url = search_page.get_current_url()
    expected_url = f"{BASE_URL}search"
    assert actual_url == expected_url, f"Expected search to not execute, URL should stay {expected_url}, got {actual_url}"
    assert search_page.is_on_search_screen(), "Expected to remain on the search page (no navigation)"


def test_search_single_character_keyword_executes_search(driver):
    """TC-SEARCH-019 (Boundary)"""
    search_page = SearchPage(driver)
    search_page.open()

    search_page.type_keyword(SEARCH_KEYWORD_WITH_RESULTS[0])
    search_page.submit_search()

    search_result_page = SearchResultPage(driver)
    search_result_page.wait_for_url_contains("keyword=")
    assert search_result_page.is_screen_displayed(), "Expected search result screen to be displayed for a 1-character keyword"


def test_clearing_keyword_shows_recent_search_section(driver):
    """TC-SEARCH-020"""
    search_page = SearchPage(driver)
    keyword = "자동화테스트검색어020"
    _search_and_reveal_recent(search_page, keyword)

    assert search_page.is_recent_search_heading_present(), "Expected '최근 검색' heading to be displayed"
    assert search_page.is_recent_search_clear_all_present(), "Expected '모두 삭제' link to be displayed"
    assert keyword in search_page.get_recent_search_keywords(), "Expected the searched keyword to appear in recent list"

    search_page.click_recent_search_clear_all()
    search_page.wait_for_recent_search_cleared()


def test_recent_search_clear_all_removes_every_item_immediately(driver):
    """TC-SEARCH-021"""
    search_page = SearchPage(driver)
    keyword_1 = "자동화테스트검색어021A"
    keyword_2 = "자동화테스트검색어021B"
    _search_and_reveal_recent(search_page, keyword_1)

    search_page.open()
    search_page.type_keyword(keyword_2)
    search_page.submit_search()
    search_page.open()
    search_page.type_keyword("x")
    search_page.clear_keyword()
    search_page.wait_for_recent_search_keyword_present(keyword_2)

    recent_keywords = search_page.get_recent_search_keywords()
    assert keyword_1 in recent_keywords and keyword_2 in recent_keywords, "Expected both keywords in recent list"

    search_page.click_recent_search_clear_all()
    search_page.wait_for_recent_search_cleared()
    assert search_page.get_recent_search_keywords() == [], "Expected recent search list to be empty immediately"
    assert not search_page.is_recent_search_heading_present(), "Expected '최근 검색' section to disappear"


def test_recent_search_individual_delete_removes_only_that_item(driver):
    """TC-SEARCH-022"""
    search_page = SearchPage(driver)
    keyword_to_delete = "자동화테스트검색어022A"
    keyword_to_keep = "자동화테스트검색어022B"
    _search_and_reveal_recent(search_page, keyword_to_delete)

    search_page.open()
    search_page.type_keyword(keyword_to_keep)
    search_page.submit_search()
    search_page.open()
    search_page.type_keyword("x")
    search_page.clear_keyword()
    search_page.wait_for_recent_search_keyword_present(keyword_to_keep)

    search_page.click_recent_search_delete(keyword_to_delete)
    search_page.wait_for_recent_search_keyword_absent(keyword_to_delete)
    recent_keywords = search_page.get_recent_search_keywords()
    assert keyword_to_delete not in recent_keywords, "Expected deleted keyword to be removed"
    assert keyword_to_keep in recent_keywords, "Expected the other keyword to remain"

    search_page.click_recent_search_clear_all()
    search_page.wait_for_recent_search_cleared()


def test_recent_search_item_click_re_executes_search(driver):
    """TC-SEARCH-023"""
    search_page = SearchPage(driver)
    keyword = "자동화테스트검색어023"
    _search_and_reveal_recent(search_page, keyword)

    search_page.click_recent_search_item(keyword)

    search_result_page = SearchResultPage(driver)
    search_result_page.wait_for_url_contains("keyword=")
    actual_url = search_result_page.get_current_url()
    expected_url = f"{BASE_URL}search?keyword={urllib.parse.quote(keyword)}"
    assert actual_url == expected_url, f"Expected re-search URL for {keyword}, got {actual_url}"

    search_page.open()
    search_page.type_keyword("x")
    search_page.clear_keyword()
    search_page.wait_for_recent_search_keyword_present(keyword)
    search_page.click_recent_search_clear_all()
    search_page.wait_for_recent_search_cleared()


def test_back_button_from_main_page_entry_returns_to_main_page(driver):
    """TC-SEARCH-025"""
    home_page = HomePage(driver)
    home_page.open()
    home_page.click_search_entry()

    search_page = SearchPage(driver)
    search_page.wait_for_url_contains("search")
    search_page.click_back()

    search_page.wait_for_url_to_be(BASE_URL)
    assert search_page.get_current_url() == BASE_URL, "Expected to return to the main page"


def test_back_button_from_product_detail_entry_returns_to_product_detail(driver):
    """TC-SEARCH-026"""
    product_detail_page = ProductDetailPage(driver)
    product_detail_page.open(PRODUCT_ID_ON_SALE)
    product_detail_page.click_search_icon()

    search_page = SearchPage(driver)
    search_page.wait_for_url_contains("search")
    search_page.click_back()

    expected_url = f"{BASE_URL}products/{PRODUCT_ID_ON_SALE}"
    search_page.wait_for_url_to_be(expected_url)
    assert search_page.get_current_url() == expected_url, "Expected to return to the product detail page"


def test_cancel_button_resets_keyword_and_shows_initial_screen(driver):
    """TC-SEARCH-027"""
    search_page = SearchPage(driver)
    search_page.open()
    search_page.type_keyword("테스트취소123")

    search_page.click_cancel()

    assert search_page.get_current_url() == f"{BASE_URL}search", "Expected to remain on the search page"
    assert search_page.is_initial_screen_displayed(), "Expected search initial screen to be shown after cancel"


def test_logged_out_user_recent_search_is_saved_and_displayed(driver):
    """TC-SEARCH-024"""
    search_page = SearchPage(driver)
    keyword = "자동화테스트검색어024"
    _search_and_reveal_recent(search_page, keyword)

    assert keyword in search_page.get_recent_search_keywords(), "Expected recent keyword to be saved while logged out"

    search_page.click_recent_search_clear_all()
    search_page.wait_for_recent_search_cleared()
