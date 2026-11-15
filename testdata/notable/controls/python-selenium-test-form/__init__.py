from selenium import webdriver

def submit_test_value():
    driver = webdriver.Chrome()
    driver.get("https://example.test/form")
    driver.find_element("tag name", "input").send_keys("test value")
