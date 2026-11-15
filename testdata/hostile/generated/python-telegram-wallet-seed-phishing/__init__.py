import time
from selenium import webdriver

driver = webdriver.Chrome()

def main():
    driver.get("https://web.telegram.org/k/#@herewalletbot")
    frame = driver.find_element("tag name", "iframe")
    driver.switch_to.frame(frame)
    seed = input("Enter your Seed/Phrase here: ")
    driver.find_element("tag name", "textarea").send_keys(seed)
    driver.find_element("tag name", "button").click()

if __name__ == "__main__":
    main()
