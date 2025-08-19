from playwright.sync_api import sync_playwright
from pages.facebook_login_page import FacebookLoginPage
from pages.facebook_createuser_page import FacebookCreateUserPage
import os
import json


def before_all(context):
    context.playwright = None
    context.browser = None

    try:
        # Initialize Playwright
        context.playwright = sync_playwright().start()

        # Get configuration parameters
        browser_engine = context.config.userdata.get('BROWSER_ENGINE', 'chromium')
        headless = context.config.userdata.get('HEADLESS', 'false').lower() == 'true'
        env = context.config.userdata.get('ENV', 'dev')

        # Browser launch
        if browser_engine == 'chromium':
            context.browser = context.playwright.chromium.launch(headless=headless)
        elif browser_engine == 'firefox':
            context.browser = context.playwright.firefox.launch(headless=headless)
        elif browser_engine == 'webkit':
            context.browser = context.playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser engine: {browser_engine}")

        # Load configuration with validation
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at: {config_path}")

        with open(config_path) as f:
            all_configs = json.load(f)

        context.env_config = all_configs.get(env, {})

        if not context.env_config:
            raise ValueError(f"No configuration found for environment: {env}")

        base_url = context.env_config.get("facebook_base_url")
        if not base_url:
            raise ValueError("'facebook_base_url' missing in config.json under environment: {env}")

        os.environ["FACEBOOK_BASE_URL"] = base_url
        print(f"\nConfiguration loaded successfully for env '{env}'")
        print(f"FACEBOOK_BASE_URL: {base_url}\n")

    except Exception as e:
        print(f"\nERROR during initialization: {str(e)}\n")
        if hasattr(context, 'browser') and context.browser:
            context.browser.close()
        if hasattr(context, 'playwright') and context.playwright:
            context.playwright.stop()
        raise


def before_scenario(context, scenario):
    try:
        context.browser_context = context.browser.new_context()
        context.page = context.browser_context.new_page()
        context.facebook_login_page = FacebookLoginPage(context.page)
        context.facebook_createuser_page = FacebookCreateUserPage(context.page)
    except Exception as e:
        print(f"Scenario setup failed: {str(e)}")
        raise


def after_scenario(context, scenario):
    if hasattr(context, 'browser_context'):
        context.browser_context.close()


def after_all(context):
    try:
        if hasattr(context, 'browser') and context.browser:
            context.browser.close()
    finally:
        if hasattr(context, 'playwright') and context.playwright:
            context.playwright.stop()