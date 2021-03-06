#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random
from copy import deepcopy

from pages.desktop.home import Home


class TestAccounts:

    @pytest.mark.nondestructive
    @pytest.mark.login
    @pytest.mark.native
    def test_user_can_login_and_logout(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])
        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        home_page.header.click_logout()
        assert home_page.header.is_user_logged_in is False

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_access_the_edit_profile_page(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])
        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        amo_user_edit_page = home_page.header.click_edit_profile()
        assert "/users/edit" in amo_user_edit_page.get_url_current_page()
        assert amo_user_edit_page.is_the_current_page

        assert "My Account" == amo_user_edit_page.account_header_text
        assert "Profile" == amo_user_edit_page.profile_header_text
        assert "Details" == amo_user_edit_page.details_header_text
        assert "Notifications" == amo_user_edit_page.notification_header_text

    @pytest.mark.native
    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_user_can_access_the_view_profile_page(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])
        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        view_profile_page = home_page.header.click_view_profile()

        assert view_profile_page.about_me == 'About me'

    @pytest.mark.native
    @pytest.mark.login
    def test_hide_email_checkbox_works(self, mozwebqa, existing_user):
        home_page = Home(mozwebqa)
        home_page.login(existing_user['email'], existing_user['password'])

        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        view_profile_page = home_page.header.click_view_profile()
        initial_state = view_profile_page.is_email_field_present

        edit_profile_page = home_page.header.click_edit_profile()
        edit_profile_page.change_hide_email_state()
        edit_profile_page.click_update_account()

        view_profile_page = home_page.header.click_view_profile()
        final_state = view_profile_page.is_email_field_present

        assert initial_state, final_state != 'The initial and final states are the same. The profile change failed.'

    @pytest.mark.native
    @pytest.mark.login
    def test_user_can_update_profile_information_in_account_settings_page(self, mozwebqa, editable_user):
        home_page = Home(mozwebqa)
        home_page.login(editable_user['email'], editable_user['password'])

        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        user_edit_page = home_page.header.click_edit_profile()
        assert user_edit_page.is_the_current_page

        # save initial values to restore them after the test is finished
        fields_no = len(user_edit_page.profile_fields)
        initial_value = [None] * fields_no
        random_name = "webqa.account%s" % random.randrange(1, 100)

        # enter new values
        for i in range(0, fields_no):
            if user_edit_page.profile_fields[i].is_field_editable:
                initial_value[i] = deepcopy(user_edit_page.profile_fields[i].field_value)
                user_edit_page.profile_fields[i].clear_field()
                user_edit_page.profile_fields[i].type_value(random_name)

        user_edit_page.click_update_account()
        assert user_edit_page.update_message == "Profile Updated"

        # using try finally to ensure that the initial values are restore even if the Asserts fail.
        try:
            for i in range(0, fields_no):
                if user_edit_page.profile_fields[i].is_field_editable:
                    assert random_name in user_edit_page.profile_fields[i].field_value

        except Exception as exception:
            assert not exception.msg

        finally:
            # restore initial values
            for i in range(0, fields_no):
                if user_edit_page.profile_fields[i].is_field_editable:
                    user_edit_page.profile_fields[i].clear_field()
                    user_edit_page.profile_fields[i].type_value(initial_value[i])

            user_edit_page.click_update_account()
