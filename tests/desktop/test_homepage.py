#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.desktop.home import Home


class HeaderMenu:

    def __init__(self, name, items):
        self.name = name
        self.items = items

    @property
    def name(self):
        return self.name

    @property
    def items(self):
        return self.items


class TestHome:

    expected_header_menus = [
        HeaderMenu('EXTENSIONS', [
            "Featured", "Most Popular", "Top Rated", "Alerts & Updates", "Appearance", "Bookmarks",
            "Download Management", "Feeds, News & Blogging", "Games & Entertainment",
            "Language Support", "Photos, Music & Videos", "Privacy & Security", "Search Tools", "Shopping",
            "Social & Communication", "Tabs", "Web Development", "Other"]),
        HeaderMenu('THEMES', [
            "Most Popular", "Top Rated", "Newest", "Abstract", "Causes", "Fashion", "Film and TV",
            "Firefox", "Foxkeh", "Holiday", "Music", "Nature", "Other", "Scenery", "Seasonal",
            "Solid", "Sports", "Websites"]),
        HeaderMenu('COLLECTIONS', [
            "Featured", "Most Followers", "Newest", "Collections I've Made",
            "Collections I'm Following", "My Favorite Add-ons"]),
        HeaderMenu(u'MORE\u2026', [
            "Add-ons for Mobile", "Dictionaries & Language Packs", "Search Tools", "Developer Hub"])]

    @pytest.mark.nondestructive
    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        home_page = Home(mozwebqa)
        assert 'MOST POPULAR' in home_page.most_popular_list_heading
        assert home_page.most_popular_count == 10

    @pytest.mark.nondestructive
    def test_that_checks_the_promo_box_exists(self, mozwebqa):
        home_page = Home(mozwebqa)
        assert home_page.promo_box_present

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        details_page = home_page.click_on_first_addon()
        assert details_page.is_the_current_page

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_featured_themes_exist_on_the_home(self, mozwebqa):
        home_page = Home(mozwebqa)
        assert home_page.featured_themes_title == u'Featured Themes See all \xbb', 'Featured Themes region title doesn\'t match'
        assert home_page.featured_themes_count >= 6

    @pytest.mark.nondestructive
    def test_that_clicking_see_all_themes_link_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_theme_page = home_page.click_featured_themes_see_all_link()

        assert featured_theme_page.is_the_current_page
        assert featured_theme_page.theme_header == 'Themes'

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        extensions_page = home_page.header.site_navigation_menu("EXTENSIONS").click()
        assert extensions_page.is_the_current_page

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_most_popular_section_is_ordered_by_users(self, mozwebqa):
        home_page = Home(mozwebqa)

        most_popular_items = home_page.most_popular_items
        assert [i.users_number for i in most_popular_items].sort(reverse=True)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_featured_collections_exist_on_the_home(self, mozwebqa):
        home_page = Home(mozwebqa)
        assert home_page.featured_collections_title == u'Featured Collections See all \xbb', 'Featured Collection region title doesn\'t match'
        assert home_page.featured_collections_count == 4

    @pytest.mark.nondestructive
    def test_that_featured_extensions_exist_on_the_home(self, mozwebqa):
        home_page = Home(mozwebqa)
        assert home_page.featured_extensions_title == 'Featured Extensions', 'Featured Extensions region title doesn\'t match'
        assert home_page.featured_extensions_see_all == u'See all \xbb', 'Featured Extensions region see all link is not correct'
        assert home_page.featured_extensions_count > 1

    @pytest.mark.nondestructive
    def test_that_clicking_see_all_collections_link_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_collection_page = home_page.click_featured_collections_see_all_link()
        assert featured_collection_page.is_the_current_page
        assert featured_collection_page.get_url_current_page().endswith('/collections/?sort=featured')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_items_menu_fly_out_while_hovering(self, mozwebqa):

        # I've adapted the test to check open/closed for all menu items
        home_page = Home(mozwebqa)

        for menu in self.expected_header_menus:
            menu_item = home_page.header.site_navigation_menu(menu.name)
            menu_item.hover()
            assert menu_item.is_menu_dropdown_visible
            home_page.hover_over_addons_home_title()
            assert menu_item.is_menu_dropdown_visible is False

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_clicking_top_rated_shows_addons_sorted_by_rating(self, mozwebqa):
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('top_rated')

        assert 'sort=rating' in extensions_page.get_url_current_page()
        assert 'Top Rated' == extensions_page.sorter.sorted_by

    @pytest.mark.nondestructive
    def test_that_clicking_most_popular_shows_addons_sorted_by_users(self, mozwebqa):
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('popular')

        assert 'sort=users' in extensions_page.get_url_current_page()
        assert 'Most Users' == extensions_page.sorter.sorted_by

    @pytest.mark.nondestructive
    def test_that_clicking_featured_shows_addons_sorted_by_featured(self, mozwebqa):
        home_page = Home(mozwebqa)
        extensions_page = home_page.click_to_explore('featured')

        assert 'sort=featured' in extensions_page.get_url_current_page()
        assert 'Featured' == extensions_page.sorter.sorted_by

    @pytest.mark.nondestructive
    def test_header_site_navigation_menus_are_correct(self, mozwebqa):
        home_page = Home(mozwebqa)

        # compile lists of the expected and actual top level navigation items
        expected_navigation_menu = [menu.name for menu in self.expected_header_menus]
        actual_navigation_menus = [actual_menu.name for actual_menu in home_page.header.site_navigation_menus]

        assert expected_navigation_menu == actual_navigation_menus

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_the_name_of_each_site_navigation_menu_in_the_header(self, mozwebqa):
        home_page = Home(mozwebqa)

        # loop through each expected menu and collect a list of the items in the menu
        # and then assert that they exist in the actual menu on the page
        for menu in self.expected_header_menus:
            expected_menu_items = menu.items
            actual_menu_items = [menu_items.name for menu_items in home_page.header.site_navigation_menu(menu.name).items]

            assert expected_menu_items == actual_menu_items

    @pytest.mark.nondestructive
    def test_top_three_items_in_each_site_navigation_menu_are_featured(self, mozwebqa):
        home_page = Home(mozwebqa)

        # loop through each actual top level menu
        for actual_menu in home_page.header.site_navigation_menus:
            # 'more' navigation_menu has no featured items so we have a different assertion
            if actual_menu.name == u"MORE\u2026":
                # loop through each of the items in the top level menu and check is_featured property
                [assert (item.is_featured) is False for item in actual_menu.items]
            else:
                # first 3 are featured, the others are not
                [assert (item.is_featured) for item in actual_menu.items[:3]]
                [assert (item.is_featured) is False for item in actual_menu.items[3:]]

    @pytest.mark.nondestructive
    def test_that_checks_the_up_and_coming_extensions_island(self, mozwebqa):

        home_page = Home(mozwebqa)

        up_and_coming_island = home_page.up_and_coming_island

        assert up_and_coming_island.title == 'Up & Coming Extensions'
        assert up_and_coming_island.see_all_text == u'See all \xbb'

        for idx in range(up_and_coming_island.pager.dot_count):
            assert idx == up_and_coming_island.visible_section)
            assert idx == up_and_coming_island.pager.selected_dot)
            assert len(up_and_coming_island.addons) == 6)
            up_and_coming_island.pager.next()

        for idx in range(up_and_coming_island.pager.dot_count - 1, -1, -1):
            assert idx == up_and_coming_island.visible_section
            assert idx == up_and_coming_island.pager.selected_dot
            assert len(up_and_coming_island.addons) == 6
            up_and_coming_island.pager.prev()

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_addons_author_link(self, mozwebqa):

        home_page = Home(mozwebqa)
        first_addon = home_page.featured_extensions[0]

        first_author = first_addon.author_name
        user_page = first_addon.click_first_author()

        assert user_page.username == first_author[0]
        assert 'user' in user_page.get_url_current_page()

    def test_that_checks_explore_side_navigation(self, mozwebqa):
        home_page = Home(mozwebqa)

        assert 'EXPLORE' == home_page.explore_side_navigation_header_text
        assert 'Featured' == home_page.explore_featured_link_text
        assert 'Most Popular' == home_page.explore_popular_link_text
        assert 'Top Rated' == home_page.explore_top_rated_link_text

    @pytest.mark.nondestructive
    def test_that_clicking_see_all_extensions_link_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extension_page = home_page.click_featured_extensions_see_all_link()
        assert featured_extension_page.is_the_current_page
        assert featured_extension_page.get_url_current_page().endswith('/extensions/?sort=featured')

    @pytest.mark.nondestructive
    def test_that_checks_all_categories_side_navigation(self, mozwebqa):
        home_page = Home(mozwebqa)
        category_region = home_page.get_category()

        assert 'CATEGORIES' == category_region.categories_side_navigation_header_text
        assert 'Alerts & Updates' == category_region.categories_alert_updates_header_text
        assert 'Appearance' == category_region.categories_appearance_header_text
        assert 'Bookmarks' == category_region.categories_bookmark_header_text
        assert 'Download Management' == category_region.categories_download_management_header_text
        assert 'Feeds, News & Blogging' == category_region.categories_feed_news_blog_header_text
        assert 'Games & Entertainment' == category_region.categories_games_entertainment_header_text
        assert 'Language Support' == category_region.categories_language_support_header_text
        assert 'Ph otos, Music & Videos' == category_region.categories_photo_music_video_header_text
        assert 'Privacy & Security' == category_region.categories_privacy_security_header_text
        assert 'Shopping' == category_region.categories_shopping_header_text
        assert 'Social & Communication' == category_region.categories_social_communication_header_text
        assert 'Tabs' == category_region.categories_tabs_header_text
        assert 'Web Development' == category_region.categories_web_development_header_text
        assert 'Other' == category_region.categories_other_header_text

    @pytest.mark.nondestructive
    def test_that_checks_other_applications_menu(self, mozwebqa):
        home_page = Home(mozwebqa)

        # Thunderbird
        assert home_page.header.is_other_application_visible("Thunderbird")
        home_page.header.click_other_application("Thunderbird")
        current_page_url = home_page.get_url_current_page()
        assert current_page_url.endswith("/thunderbird/")
        assert 'Thunderbird Add-ons' in home_page.amo_logo_title

        # Android
        assert home_page.header.is_other_application_visible("Android")
        home_page.header.click_other_application("Android")
        current_page_url = home_page.get_url_current_page()
        assert current_page_url.endswith("/android/")
        assert 'Android Add-ons' in home_page.amo_logo_title

        # Seamonkey
        assert home_page.header.is_other_application_visible("Seamonkey")
        home_page.header.click_other_application("Seamonkey")
        current_page_url = home_page.get_url_current_page()
        assert current_page_url.endswith("/seamonkey/")
        assert 'SeaMonkey Add-ons' in home_page.amo_logo_title
