#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest



from pages.desktop.home import Home


class TestCompleteThemes:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_can_be_sorted_by_name(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.click_sort_by("name")
        addons = complete_themes_page.addon_names
        addons_set = set(addons)
		assert len(addons) == len(addons_set), 'There are duplicates in the names'
        addons_orig = addons
        addons.sort()
        [assert (addons_orig[i] == addons[i]) for i in xrange(len(addons))]
        complete_themes_page.paginator.click_next_page()
        addons = complete_themes_page.addon_names
        addons_set = set(addons)
        assert len(addons) == len(addons_set), 'There are duplicates in the names'
        addons_orig = addons
        addons.sort()
        [assert (addons_orig[i], addons[i]) for i in xrange(len(addons))]

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_can_be_sorted_by_updated_date(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.click_sort_by("recently updated")
        addons = complete_themes_page.addon_names
        addons_set = set(addons)
        assert len(addons) == len(addons_set), 'There are duplicates in the names'
        updated_dates = complete_themes_page.addon_updated_dates
        assert is_sorted_descending(updated_dates)
        complete_themes_page.paginator.click_next_page()
        updated_dates.extend(complete_themes_page.addon_updated_dates)
        assert is_sorted_descending(updated_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_can_be_sorted_by_created_date(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.click_sort_by("newest")
        addons = complete_themes_page.addon_names
        addons_set = set(addons)
        assert len(addons) == len(addons_set), 'There are duplicates in the names'
        created_dates = complete_themes_page.addon_created_dates
        assert is_sorted_descending(created_dates)
        complete_themes_page.paginator.click_next_page()
        created_dates.extend(complete_themes_page.addon_created_dates)
        assert is_sorted_descending(created_dates)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_can_be_sorted_by_popularity(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.click_sort_by("weekly downloads")
        addons = complete_themes_page.addon_names
        addons_set = set(addons)
        assert len(addons) == len(addons_set), 'There are duplicates in the names'
        downloads = complete_themes_page.addon_download_number
        assert is_sorted_descending(downloads)
        complete_themes_page.paginator.click_next_page()
        downloads.extend(complete_themes_page.addon_download_number)
        assert is_sorted_descending(downloads)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_loads_landing_page_correctly(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_clicking_on_complete_theme_name_loads_its_detail_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_theme_name = complete_themes_page.addon_name(1)
        complete_theme_page = complete_themes_page.click_on_first_addon()
        Assert.contains(complete_theme_name, complete_theme_page.addon_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_page_has_correct_title(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        expected_title = "Most Popular Complete Themes :: Add-ons for Firefox"
        Assert.equal(expected_title, complete_themes_page.page_title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_complete_themes_page_breadcrumb(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        expected_breadcrumb = "Complete Themes"
        Assert.equal(expected_breadcrumb, complete_themes_page.breadcrumbs[1].text)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_clicking_on_a_subcategory_loads_expected_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        selected_category = complete_themes_page.complete_themes_category
        amo_category_page = complete_themes_page.click_on_first_category()
        Assert.equal(selected_category, amo_category_page.title)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_complete_themes_subcategory_page_breadcrumb(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        selected_category = complete_themes_page.complete_themes_category
        amo_category_page = complete_themes_page.click_on_first_category()
        expected_breadcrumbs = ['Add-ons for Firefox', 'Complete Themes', selected_category]

        [Assert.equal(expected_breadcrumbs[i], amo_category_page.breadcrumbs[i].text) for i in range(len(amo_category_page.breadcrumbs))]

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_categories_are_listed_on_left_hand_side(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        current_page_url = home_page.get_url_current_page()
        Assert.true(current_page_url.endswith("/complete-themes/"))
        default_categories = ["Animals", "Compact", "Large", "Miscellaneous", "Modern", "Nature", "OS Integration", "Retro", "Sports"]
        Assert.equal(complete_themes_page.categories_count, len(default_categories))
        count = 0
        for category in default_categories:
            count += 1
            current_category = complete_themes_page.get_category(count)
            Assert.equal(category, current_category)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_complete_themes_categories_are_not_extensions_categories(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_categories = complete_themes_page.get_all_categories

        home_page.header.site_navigation_menu("Extensions").click()
        extensions_categories = complete_themes_page.get_all_categories

        Assert.not_equal(len(complete_themes_categories), len(extensions_categories))
        Assert.equal(list(set(complete_themes_categories) & set(extensions_categories)), [])

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_last_complete_themes_page_is_not_empty(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.paginator.click_last_page()
        Assert.greater_equal(complete_themes_page.addon_count, 1)

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_the_displayed_message_for_incompatible_complete_themes(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        complete_themes_page.clear_hover_cards()

        complete_themes = complete_themes_page.complete_themes

        for complete_theme in complete_themes:
            if complete_theme.is_incompatible:
                Assert.true(complete_theme.is_incompatible_flag_visible)
                Assert.contains('Not available',
                                complete_theme.not_available_flag_text)
            else:
                Assert.false(complete_theme.is_incompatible_flag_visible)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_most_popular_link_is_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))
        Assert.equal(complete_themes_page.selected_explore_filter, 'Most Popular')

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_sorted_by_most_users_is_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        complete_themes_page = home_page.header.click_complete_themes()
        url_current_page = complete_themes_page.get_url_current_page()
        Assert.true(url_current_page.endswith("/complete-themes/"))
        Assert.equal(complete_themes_page.sorted_by, 'Most Users')
