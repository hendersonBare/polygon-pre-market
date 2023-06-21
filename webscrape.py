"""
6/17/2023

used to extract important data from websites. Only current use case is 
extracting ticker that are apart of a certain index using reputable websites. Only intended to be 
used sparingly since there are a wide range of errors that can arrise from relying to heavily on
web scraping
"""

import selenium, config, bs4
from selenium import webdriver
from bs4 import BeautifulSoup


Options = webdriver.ChromeOptions()
Options.headless = True
#options below copied from a youtube video, hopefully solves current errors
#Options.add_argument(f'user-agent={user_agent}')
Options.add_argument("--window-size=1920,1080")
Options.add_argument('--ignore-certificate-errors')
Options.add_argument('--allow-running-insecure-content')
Options.add_argument("--disable-extensions")
Options.add_argument("--proxy-server='direct://'")
Options.add_argument("--proxy-bypass-list=*")
Options.add_argument("--start-maximized")
Options.add_argument('--disable-gpu')
Options.add_argument('--disable-dev-shm-usage')
Options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=Options)

webURL = driver.get("https://www.slickcharts.com/sp500")

html_content = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the <td> elements containing ticker symbols
ticker_elements = soup.find_all('td', {'class': ''})

# Extract the ticker symbols and add them to a list
ticker_symbols = [element.text for element in ticker_elements if element.text.isalpha()]


print(html_content);