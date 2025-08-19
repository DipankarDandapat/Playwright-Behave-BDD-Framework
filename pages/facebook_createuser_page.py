import os
import time

from playwright.sync_api import Page
from .base_page import BasePage


class FacebookCreateUserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)


    def navigate_to_facebook_signup(self):
        """Navigate to the Facebook signup page."""
        self.page.goto("https://www.facebook.com/r.php")

    def enter_registration_details(self, first_name, last_name, email, password, birth_day, birth_month, birth_year, gender):
        """Enter registration details."""
        self.enter_text("firstname", first_name)
        self.enter_text("lastname", last_name)
        self.enter_text("reg_email__", email)
        self.enter_text("reg_passwd__", password)
        self.select_dropdown("day", birth_day)
        self.select_dropdown("month", birth_month)
        self.select_dropdown("year", birth_year)
        if gender == "1": # Female
            self.click("gender_female")
        elif gender == "2": # Male
            self.click("gender_male")
        elif gender == "-1": # Custom
            self.click("gender_custom")


    def click_signup_button(self):
        time.sleep(10)
        """Click the sign up button."""
        self.click("websubmit")


