# Playwright-Behave BDD Framework

This project provides a scalable and maintainable test automation framework that integrates Playwright (for modern end-to-end browser automation) with Behave (a Behavior-Driven Development tool for Python). It enables writing test scenarios in a natural language style (Gherkin syntax), making it easier for technical and non-technical stakeholders to collaborate on defining system behavior.

## Project Structure

```
playwright_framework/
│
├── config/
│   ├── config.json                # Environment-specific configurations (URLs, credentials)
│   └── __init__.py
│
├── features/                      # Behave (BDD) feature files
│   ├── login.feature              # Example Gherkin scenarios for login
│   └── environment.py             # Behave hooks for setup and teardown
│
├── steps/                         # Step definitions for Behave features
│   ├── login_steps.py             # Step definitions for login.feature
│   └── __init__.py
│
├── elements/                      # JSON files defining page elements (locators)
│   ├── facebooklogin_page.json
│   └── facebookcreateuser_page.json
│
├── pages/                         # Page Object Model (POM) classes
│   ├── base_page.py               # Base class for all page objects
│   ├── facebook_login_page.py     # Page object for Facebook login
│   ├── facebook_createuser_page.py # Page object for Facebook user creation
│   └── __init__.py
│
├── reports/                       # Test reports (Allure reports)
│
├── testdata/                      # Test data in JSON format
│   └── facebook/
│       ├── facebook_login_data.json
│       └── facebook_createuser_data.json
│
├── utils/
│   ├── logger.py                  # Custom logging utility
│   ├── file_reader.py             # Utility for reading files (e.g., JSON test data)
│   ├── functions.py               # General utility functions
│   ├── waits.py                   # Custom wait conditions
│   ├── db/                        # Database utilities
│   └── __init__.py
│
├── requirements.txt               # Python dependencies
├── behave.ini                     # Behave configuration
└── README.md
```

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd playwright_framework
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

## Configuration

-   **`config/config.json`**: This file contains environment-specific URLs and other configurations. You can define `dev`, `qa`, `prod`, etc., environments.

    ```json
    {
      "dev": {
        "facebook_base_url": "https://www.facebook.com/",
        "timeout": 30000
      },
      "qa": {
        "facebook_base_url": "https://www.facebook.com/"
      },
      "prod": {
        "facebook_base_url": "https://www.facebook.com/"
      }
    }
    ```

-   **`behave.ini`**: Configure Behave settings, including paths, formatters, and user data (for browser engine, headless mode, and environment).

    ```ini
    [behave]
    paths = features
    format = pretty
    format = allure_behave.formatter:AllureFormatter
    outfiles = reports/allure-results
    stop = yes
    color = yes
    stderr_capture = yes
    stdout_capture = yes

    [behave.userdata]
    BROWSER_ENGINE = chromium
    HEADLESS = false
    ENV = dev
    ```

## Running Tests

Tests are executed using the `behave` command. You can pass user data parameters to control browser, headless mode, and environment.

### Basic Run

To run all features:

```bash
behave
```

### Running with Specific Browser and Headless Mode

```bash
behave -D BROWSER_ENGINE=firefox -D HEADLESS=true
```

-   `BROWSER_ENGINE`: `chromium`, `firefox`, or `webkit` (default: `chromium`)
-   `HEADLESS`: `true` or `false` (default: `false`)

### Running for a Specific Environment

```bash
behave -D ENV=qa
```

-   `ENV`: `dev`, `qa`, or `prod` (default: `dev`)

### Running a Specific Feature File

```bash
behave features/login.feature
```

### Running a Specific Scenario

```bash
behave features/login.feature --name "Successful Login with Valid Credentials"
```

### Generating Allure Reports

After running tests, Allure reports will be generated in the `reports/allure-results` directory. To view them:

1.  **Install Allure Commandline (if not already installed):**
    Follow instructions [here](https://docs.qameta.io/allure/latest/#_installing_a_commandline).

2.  **Generate and open the report:**
    ```bash
    allure serve reports/allure-results
    ```

## Extending the Framework

### Adding a New Page

1.  Create a new Python file in `pages/` (e.g., `my_new_page.py`) inheriting from `BasePage`.
2.  Define elements for the new page in a JSON file in `elements/` (e.g., `mynew_page.json`).
3.  Implement methods in `MyNewPage` class for interactions specific to that page.

### Adding a New Feature

1.  Create a new `.feature` file in `features/` (e.g., `my_new_feature.feature`) with Gherkin scenarios.
2.  Create a corresponding Python file in `steps/` (e.g., `my_new_feature_steps.py`) to define the step implementations.
3.  Import necessary page objects into your step definition file.

## Real-time Examples

### Example: Successful Login (features/login.feature)

```gherkin
Feature: Facebook Login Functionality
  As a Facebook user
  I want to log in to my account
  So that I can access my feed and interact with friends

  Scenario: Successful Login with Valid Credentials
    Given I am on the Facebook login page
    When I enter valid username and password
    And I click the login button
    Then I should be logged in successfully
```

### Example: Invalid Login (features/login.feature)

```gherkin
  Scenario: Unsuccessful Login with Invalid Password
    Given I am on the Facebook login page
    When I enter valid username and invalid password
    And I click the login button
    Then I should see an error message indicating invalid credentials
```

### Example: Step Definitions (steps/login_steps.py)

```python
from behave import *
from playwright.sync_api import expect
import os
import json

@given("I am on the Facebook login page")
def step_impl(context):
    context.facebook_login_page.navigate_to_facebook()
    context.facebook_login_page.verify_page_title("Facebook – log in or sign up")

@when("I enter valid username and password")
def step_impl(context):
    test_data_path = os.path.join(os.path.dirname(__file__), '..', 'testdata', 'facebook', 'facebook_login_data.json')
    with open(test_data_path, 'r') as f:
        test_data = json.load(f)
    
    valid_user = test_data["valid_credentials"]
    context.facebook_login_page.enter_credentials(valid_user["username"], valid_user["password"])

# ... other steps ...
```

## Troubleshooting

-   **`playwright install` errors**: Ensure you have Python and pip correctly installed and configured in your PATH.
-   **Element not found errors**: Double-check your locators in the `elements/*.json` files and ensure the page is in the expected state when the element is accessed.
-   **Browser not launching**: Verify Playwright browsers are installed (`playwright install`) and that your `behave.ini` `BROWSER_ENGINE` is correctly set.


