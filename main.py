from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

CHROME_DRIVER_PATH = "C:\Devlelopment\chromedriver_win32\chromedriver.exe"
SIMILAR_ACCOUNT = "seinfeldepisodes"
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")


class InstaFollower:

    def __init__(self):
        option = Options()
        option.add_experimental_option('detach', True)
        service = Service(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=option)
        self.driver.maximize_window()

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(10)
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys(USERNAME)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(10)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(10)
        followers_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_button.click()
        time.sleep(10)
        pop_up_window = self.driver.find_element(By.CSS_SELECTOR, '.x7r02ix ._aano')
        for i in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)
            time.sleep(5)

    def follow(self):
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._aano div div button")
        for button in all_buttons:
            try:
                if button.text == "Follow":
                    button.click()
                    time.sleep(3)
                else:
                    time.sleep(2)
                    continue
            except NoSuchElementException:
                break
        else:
            print("Follow limit reached.")


insta_bot = InstaFollower()
insta_bot.login()
insta_bot.find_followers()
insta_bot.follow()
