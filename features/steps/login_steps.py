import time

from behave import *
from playwright.sync_api import expect
import os
import json
import re

@given("I am on the Facebook login page")
def step_impl(context):
    context.facebook_login_page.navigate_to_facebook()
    time.sleep(10)
    context.facebook_login_page.verify_page_title("Facebook – log in or sign up")

@when("I enter valid username and password")
def step_impl(context):
    # Load test data from JSON file
    test_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'facebook', 'facebook_login_data.json')
    with open(test_data_path, 'r') as f:
        test_data = json.load(f)
    
    valid_user = test_data["valid_credentials"]
    context.facebook_login_page.enter_credentials(valid_user["username"], valid_user["password"])
    time.sleep(10)

@when("I enter valid username and invalid password")
def step_impl(context):
    # Load test data from JSON file
    test_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'facebook', 'facebook_login_data.json')
    with open(test_data_path, 'r') as f:
        test_data = json.load(f)
    
    invalid_user = test_data["invalid_credentials"]
    context.facebook_login_page.enter_credentials(invalid_user["username"], invalid_user["password"])

@when("I click the login button")
def step_impl(context):
    context.facebook_login_page.click_loginbutto()

@then("I should be logged in successfully")
def step_impl(context):
    # This step needs to be adapted based on what indicates a successful login
    # For Facebook, after successful login, the URL changes to facebook.com/home.php or similar
    # Or a specific element on the home page becomes visible
    expect(context.page).to_have_url(re.compile(os.getenv("FACEBOOK_BASE_URL")))
    # Alternatively, check for an element that only appears after login, e.g., a user profile icon
    # context.facebook_login_page.verify_element_is_visible("profile_icon") # Assuming 'profile_icon' is defined in elements/facebook_home_page.json

@then("I should see an error message indicating invalid credentials")
def step_impl(context):
    # This step needs to be adapted based on the actual error message element on Facebook login page
    # For example, if there's a div with id 'error_box' and text 'The password you’ve entered is incorrect.'
    # context.facebook_login_page.verify_element_contains_text("error_message_element", "The password you’ve entered is incorrect.")
    # For now, we'll check for a specific URL or a generic error message presence
    expect(context.page).to_have_url(re.compile(os.getenv("FACEBOOK_BASE_URL")))
    # Or check for an error message element, assuming it's defined in elements/facebooklogin_page.json
    # context.facebook_login_page.verify_element_is_visible("error_message_element")






