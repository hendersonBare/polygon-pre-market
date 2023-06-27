"""
6/17/2023

used to extract important data from websites. Only current use case is 
extracting ticker that are apart of a certain index using reputable websites. Only intended to be 
used sparingly since there are a wide range of errors that can arrise from relying to heavily on
web scraping
"""
import time, re

import selenium, config, bs4, requests
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium.webdriver import Firefox


Options = webdriver.FirefoxOptions()
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
driver = webdriver.Firefox(options=Options)


"""webURL = driver.get("https://www.slickcharts.com/sp500")"""

html_content = driver.page_source
"""
# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the <td> elements containing ticker symbols
ticker_elements = soup.find_all('td', {'class': ''})

# Extract the ticker symbols and add them to a list
ticker_symbols = [element.text for element in ticker_elements if element.text.isalpha()]"""


#print(html_content);

def get_stock_list(page_number):
  url = "https://finviz.com/screener.ashx?v=111&f=exch_nasd&r=%s" % page_number
  driver.get(url)
  response = driver.page_source
  soup = BeautifulSoup(response, "html.parser")
  stock_list = []
  table = soup.find("table", class_="fv-container")
  #for stock in table.find_all(type="comment"):
  comments = soup.find_all(string=lambda t: isinstance(t, Comment))
  for comment in comments:
    if re.match(' TS\n[a-zA-z]+', comment):
      stock_list.append((comment))
  return stock_list

def main():
  for page_number in range(1, 41, 20):
    stock_list = get_stock_list(page_number)
    for symbol in stock_list:
      print(symbol)

def split_comment_into_tickers(comment):
  lines = comment.split('\n')

main()
