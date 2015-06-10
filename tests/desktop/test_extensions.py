#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.desktop.home import Home


class TestExtensions:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert featured_extensions_page.sorter.sorted_by == "Featured"

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_pagination(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_next_page()

        assert "&page=2" in featured_extensions_page.get_url_current_page()

        featured_extensions_page.paginator.click_prev_page()

        assert "&page=1" in featured_extensions_page.get_url_current_page()

        featured_extensions_page.paginator.click_last_page()

        assert featured_extensions_page.paginator.is_next_page_disabled

        featured_extensions_page.paginator.click_first_page()

        assert featured_extensions_page.paginator.is_prev_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_previous_button_is_disabled_on_the_first_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('Most Users')

        assert featured_extensions_page.paginator.is_prev_page_disabled

        featured_extensions_page.paginator.click_next_page()
        featured_extensions_page.paginator.click_prev_page()

        assert featured_extensions_page.paginator.is_prev_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_next_button_is_disabled_on_the_last_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')
        featured_extensions_page.paginator.click_last_page()

        assert featured_extensions_page.paginator.is_next_page_disabled, 'Next button is available'

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_top_rated(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by("Top Rated")
        assert featured_extensions_page.sorter.sorted_by == "Top Rated"
        assert "sort=rating" == featured_extensions_page.get_url_current_page()

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_most_user(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('most_users')

        assert "sort=users" in featured_extensions_page.get_url_current_page()
        user_counts = [extension.user_count for extension in featured_extensions_page.extensions]
        assert user_counts.sort(reverse=True)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_newest(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        featured_extensions_page.sorter.sort_by('newest')
        assert featured_extensions_page.sorter.sorted_by == "Newest"
        assert "sort=created" in featured_extensions_page.get_url_current_page()

        added_dates = [i.added_date for i in featured_extensions_page.extensions]
        assert added_dates.sort(reverse=True)
        featured_extensions_page.paginator.click_next_page()

        added_dates.extend([i.added_date for i in featured_extensions_page.extensions])
        assert added_dates.sort(reverse=True)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_extensions_are_sorted_by_recently_updated(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('recently updated')
        assert featured_extensions_page.sorter.sorted_by == "Recently Updated"
        assert "sort=updated" in featured_extensions_page.get_url_current_page()

        updated_dates = [i.updated_date for i in featured_extensions_page.extensions]
        assert updated_dates.sort(reverse=True)
        featured_extensions_page.paginator.click_next_page()

        updated_dates.extend([i.updated_date for i in featured_extensions_page.extensions])
        assert updated_dates.sort(reverse=True)

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_extensions_are_sorted_by_up_and_coming(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        featured_extensions_page.sorter.sort_by('up and coming')
        assert featured_extensions_page.sorter.sorted_by == "Up & Coming"
        assert "sort=hotness" in featured_extensions_page.get_url_current_page()
        assert len(featured_extensions_page.extensions) > 0

    @pytest.mark.nondestructive
    def test_that_extensions_page_contains_addons_and_the_pagination_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        # Assert that at least one addon is displayed
        assert len(featured_extensions_page.extensions) > 0

        if len(featured_extensions_page.extensions) < 20:
            # Assert that the paginator is not present if fewer than 20 extensions are displayed
            assert not featured_extensions_page.is_paginator_present
        else:
            # Assert that the paginator is present if 20 extensions are displayed
            assert featured_extensions_page.is_paginator_present
            assert featured_extensions_page.paginator.is_prev_page_disabled
            assert featured_extensions_page.paginator.is_next_page_disabled

            featured_extensions_page.paginator.click_next_page()

            assert not featured_extensions_page.paginator.is_prev_page_disabled
            assert not featured_extensions_page.paginator.is_next_page_disabled

            featured_extensions_page.paginator.click_prev_page()

            assert len(featured_extensions_page.extensions) == 20
            assert featured_extensions_page.paginator.is_prev_page_disabled
            assert not featured_extensions_page.paginator.is_next_page_disabled

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_breadcrumb_menu_in_extensions_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()

        breadcrumbs = featured_extensions_page.breadcrumbs

        assert breadcrumbs[0].text == 'Add-ons for Firefox'
        assert breadcrumbs[1].text == 'Extensions'

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_if_the_subscribe_link_exists(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert "Subscribe" in featured_extensions_page.subscribe_link_text

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_that_checks_featured_extensions_header(self, mozwebqa):
        home_page = Home(mozwebqa)
        featured_extensions_page = home_page.header.site_navigation_menu("Extensions").click()
        assert "Featured Extensions" == featured_extensions_page.featured_extensions_header_text
