import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

CHROME_DRIVER_PATH = "C:\Devlelopment\chromedriver_win32\chromedriver.exe"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSewb_G18GFYcz_CfifBJTpzXzWJo7wJ_d4o3eEpqIhNkQd81A/viewform?usp=sf_link"
URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63863600683594%2C%22east%22%3A-122.22802199316406%2C%22south%22%3A37.6454633630373%2C%22north%22%3A37.90489195672952%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

# Scrapping zillow to get listing URL, price and address
response = requests.get(url=URL, headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

listing_links = []
prices_list = []
addresses_list = []

all_listing_link_elements = soup.select("div.search-page-container div div#grid-search-results ul li.ListItem-c11n-8-85-1__sc-10e22w8-0 div div article div div.StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 a")
for link in all_listing_link_elements:
    if "http" not in link['href']:
        link['href'] = "https://www.zillow.com"+link['href']
    listing_links.append(link['href'])

all_price_elements = soup.select("div.search-page-container div div#grid-search-results ul li.ListItem-c11n-8-85-1__sc-10e22w8-0 div div article div div.StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 div.StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 span")
for price in all_price_elements:
    if "+" in price.text:
        prices_list.append(price.text.split("+")[0])
    elif "/" in price.text:
        prices_list.append(price.text.split("/")[0])

all_address_link_elements = soup.select("div.search-page-container div div#grid-search-results ul li.ListItem-c11n-8-85-1__sc-10e22w8-0 div div article div div.StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 a address")
for address in all_address_link_elements:
    addresses_list.append(address.text.split("|")[-1])


# Using selenium to fill the Google form
option = Options()
option.add_experimental_option('detach', True)
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=option)

for i in range(len(listing_links)):
    driver.get(GOOGLE_FORM_LINK)
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    address = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    address.send_keys(addresses_list[i])
    price_per_month = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    price_per_month.send_keys(prices_list[i])
    property_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    property_link.send_keys(listing_links[i])
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')))
    submit_button.click()
    time.sleep(1)

driver.quit()




