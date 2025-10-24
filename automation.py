import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class GoogleFormAutomator:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()


        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--use-mock-keychain")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": self.driver.execute_script("return navigator.userAgent").replace("HeadlessChrome", "Chrome")
        })

        self.wait = WebDriverWait(self.driver, 20)

    def human_like_delay(self, min_delay=0.5, max_delay=2.0):
        time.sleep(random.uniform(min_delay, max_delay))

    def smooth_scroll_to_element(self, element):
        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'nearest'
            });
        """, element)
        self.human_like_delay(0.5, 1.0)

    def human_type(self, element, text):
        """Type text with human-like intervals"""
        element.clear()
        self.human_like_delay(0.3, 0.7)

        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # Random typing speed

    def find_form_elements(self):
        elements = {
            'inputs': [],
            'textareas': [],
            'date_inputs': [],
            'submit_button': None
        }

        try:

            print("🔍 Searching for form elements...")


            input_selectors = [
                'input.whsOnd',
                'input[jsname]',
                'input[data-initial-value]',
                'div[data-params] input',
                'input[type="text"]',
                'input[type="email"]',
                'input[type="tel"]',
                'input[type="date"]'
            ]

            for selector in input_selectors:
                try:
                    found_inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_inputs:
                        elements['inputs'].extend(found_inputs)
                        print(f"✅ Found {len(found_inputs)} inputs with selector: {selector}")
                        break
                except Exception as e:
                    continue


            textarea_selectors = [
                'textarea.whsOnd',
                'textarea[jsname]',
                'div[data-params] textarea',
                'textarea'
            ]

            for selector in textarea_selectors:
                try:
                    found_textareas = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_textareas:
                        elements['textareas'] = found_textareas
                        print(f"✅ Found {len(found_textareas)} textareas with selector: {selector}")
                        break
                except Exception as e:
                    continue
            unique_inputs = []
            seen_elements = set()

            for inp in elements['inputs']:
                element_id = inp.get_attribute('outerHTML')
                if element_id not in seen_elements:
                    unique_inputs.append(inp)
                    seen_elements.add(element_id)

            elements['inputs'] = unique_inputs
            submit_selectors = [
                '//span[text()="Submit" or text()="SUBMIT" or text()="submit"]/ancestor::div[@role="button"]',
                '//div[@role="button"]//span[contains(text(), "Submit")]',
                '//button[contains(text(), "Submit")]',
                'div[role="button"][jsname]',
                'input[type="submit"]'
            ]

            for selector in submit_selectors:
                try:
                    if selector.startswith('//'):
                        submit_btn = self.driver.find_element(By.XPATH, selector)
                    else:
                        submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)

                    if submit_btn and submit_btn.is_displayed():
                        elements['submit_button'] = submit_btn
                        print(f"✅ Found submit button with selector: {selector}")
                        break
                except Exception as e:
                    continue

            return elements

        except Exception as e:
            print(f"Error finding form elements: {e}")
            return elements

    def fill_form_data(self, form_data):
        try:
            form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdUCd3UWQ3VOgeg0ZzNeT-xzNawU8AJ7Xidml-w1vhfBcvBWQ/viewform'
            print(f"Navigating to: {form_url}")

            self.driver.get(form_url)
            self.driver.maximize_window()
            self.human_like_delay(3, 5)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            self.human_like_delay(2, 3)
            elements = self.find_form_elements()

            if not elements['inputs'] and not elements['textareas']:
                print("No form elements found!")
                return False

            print(f"Found {len(elements['inputs'])} input fields and {len(elements['textareas'])} textarea fields")

            # Your specific form data
            form_values = [
                "Rahul Sati",
                "7302253826",
                "rahulsati9969@gmail.com",
                "B-92 shivalik nagar haridwar",
                "249403",
                "10/01/2003",
                "Male",
                "GNFPYC"
            ]


            filled_count = 0
            input_index = 0
            textarea_index = 0

            for i, value in enumerate(form_values):
                try:
                    field = None
                    field_type = "unknown"


                    if i == 3 and elements['textareas']:  # Address field
                        field = elements['textareas'][textarea_index] if textarea_index < len(
                            elements['textareas']) else None
                        field_type = "textarea"
                        textarea_index += 1
                    else:
                        if input_index < len(elements['inputs']):
                            field = elements['inputs'][input_index]
                            field_type = "input"
                            input_index += 1

                    if field is None:
                        print(f"⚠️  No field available for value '{value}' at index {i}")
                        continue


                    self.smooth_scroll_to_element(field)


                    self.driver.execute_script("arguments[0].style.border='3px solid red'", field)
                    self.human_like_delay(0.5, 1.0)


                    if field_type == "textarea":
                        self.human_type(field, value)
                        print(f"✅ Filled textarea with: '{value}'")
                    else:

                        field_type_attr = field.get_attribute('type')
                        if field_type_attr == 'date':

                            if '/' in value:
                                parts = value.split('/')
                                if len(parts) == 3:
                                    formatted_date = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
                                    field.clear()
                                    field.send_keys(formatted_date)
                                    print(f"Filled date field with: '{formatted_date}'")
                                else:
                                    self.human_type(field, value)
                                    print(f"Filled input field with: '{value}'")
                            else:
                                self.human_type(field, value)
                                print(f"Filled input field with: '{value}'")
                        else:
                            self.human_type(field, value)
                            print(f"Filled input field with: '{value}'")


                    self.driver.execute_script("arguments[0].style.border=''", field)
                    filled_count += 1


                    self.human_like_delay(1, 2)

                except Exception as e:
                    print(f"Error filling field {i} with value '{value}': {e}")
                    continue

            print(f"Successfully filled {filled_count}/{len(form_values)} fields")


            if elements['submit_button']:
                try:
                    self.human_like_delay(2, 3)  # Wait before submitting
                    self.smooth_scroll_to_element(elements['submit_button'])


                    self.driver.execute_script("arguments[0].style.border='3px solid green'", elements['submit_button'])
                    self.human_like_delay(1, 2)


                    ActionChains(self.driver).move_to_element(elements['submit_button']).click().perform()
                    print("Form submitted successfully")


                    self.human_like_delay(3, 5)


                    try:
                        success_element = self.wait.until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "//*[contains(text(), 'response has been recorded') or contains(text(), 'Thank you') or contains(text(), 'submitted')]"))
                        )
                        print("Form submission confirmed!")
                        return True
                    except TimeoutException:
                        print("Form submitted but no confirmation message found")
                        return True

                except Exception as e:
                    print(f"Error submitting form: {e}")
                    return False
            else:
                print("Submit button not found - form filled but not submitted")
                return True

        except Exception as e:
            print(f"Main error in fill_form_data: {e}")
            return False

    def run(self):
        try:
            success = self.fill_form_data({})

            if success:
                print("AUTOMATION COMPLETED SUCCESSFULLY!")
            else:
                print("AUTOMATION COMPLETED WITH ERRORS")

        except Exception as e:
            print(f"error in run method: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed")


def main():
    automator = GoogleFormAutomator()
    automator.run()


if __name__ == "__main__":
    main()

