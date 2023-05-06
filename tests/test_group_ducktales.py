from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

LOADER_CONTAINER = By.CSS_SELECTOR, 'div.owm-loader-container > div'
SEARCH_CITY_INPUT = By.CSS_SELECTOR, "input[placeholder='Search city']"
BTN_SEARCH = By.CSS_SELECTOR, "button[class ='button-round dark']"
SEARCH_DROPDOWN_MENU = By.CLASS_NAME, 'search-dropdown-menu'
SEARCH_DROPDOWN_MENU_FIRST_CHILD = By.CSS_SELECTOR, 'ul.search-dropdown-menu li:nth-child(1) span:nth-child(1)'
SEARCH_DROPDOWN_MENU_FIRST_CHILD_TEXT = By.CSS_SELECTOR, '.grid-container.grid-4-5 h2'


def test_tc_001_01_01_verify_city_name_displayed_by_zip(driver, open_and_load_main_page, wait):
    search_city_field = driver.find_element(*SEARCH_CITY_INPUT)
    search_city_field.send_keys('66002')
    search_button = driver.find_element(*BTN_SEARCH)
    search_button.click()
    search_option = wait.until(EC.element_to_be_clickable(SEARCH_DROPDOWN_MENU_FIRST_CHILD))
    search_option.click()
    expected_city = 'Atchison, US'
    wait.until(EC.text_to_be_present_in_element(SEARCH_DROPDOWN_MENU_FIRST_CHILD_TEXT, 'Atchison'))
    displayed_city = driver.find_element(* SEARCH_DROPDOWN_MENU_FIRST_CHILD_TEXT).text
    assert displayed_city == expected_city


def test_tc_001_01_02_verify_dropdown_options_contain_valid_value(driver, open_and_load_main_page, wait):
    driver.find_element(*SEARCH_CITY_INPUT).send_keys('California')
    driver.find_element(*BTN_SEARCH).click()
    wait.until(EC.element_to_be_clickable(SEARCH_DROPDOWN_MENU))
    dropdown_list = driver.find_element(*SEARCH_DROPDOWN_MENU)
    for i in dropdown_list.find_elements(By.CSS_SELECTOR, 'li'):
        assert 'California' in i.text, 'Not all search suggestions in the drop-down list contain "California"'


# TC_001.02.04_01 | Main page> Search city widget > Verify the buttons for metric and imperial are visible and clickable
def test_tc_001_02_04_01_switch_toggle_buttons(driver):
    driver.get('https://openweathermap.org/')
    # switch the temperature system to imperial
    imperial_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(),'Imperial: °F, mph')]")))
    time.sleep(5)
    imperial_button.click()
    # verify the temperature system is imperial
    temp_system = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//span[@class='heading']"))).text
    assert "°F" in temp_system, "Failed to switch to imperial temperature system"
    metric_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(),'Metric: °C, m/s')]")))
    # ActionChains(driver).move_to_element(metric_button).click(metric_button).perform()
    metric_button.click()
    # verify that toggle buttons are displayed on the page
    assert metric_button.is_displayed() and imperial_button.is_displayed()
