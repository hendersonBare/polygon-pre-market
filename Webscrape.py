"""
6/17/2023

used to extract important data from websites. Only current use case is 
extracting ticker that are apart of a certain index using reputable websites. Only intended to be 
used sparingly since there are a wide range of errors that can arrise from relying to heavily on
web scraping
"""
import time, re, logging

import selenium, config, bs4, requests
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import Comment
from selenium.webdriver import Firefox


Options = webdriver.FirefoxOptions()
Options.headless = True
#options below copied from a youtube video: https://www.youtube.com/watch?v=LN1a0JoKlX8&t=230s
#TODO: delete some of these unneeded options to make code more concise
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

file_path = 'NASDAQ_screener_tickers.txt'

file = open(file_path, "w")

def get_stock_list(page_number):
  url = "https://finviz.com/screener.ashx?v=111&f=exch_nasd&r=%s" % page_number #page_number used to iterate through pages
  driver.get(url)
  response = driver.page_source
  soup = BeautifulSoup(response, "html.parser")
  stock_list = []
  table = soup.find("table", class_="fv-container") 
  comments = soup.find_all(string=lambda t: isinstance(t, Comment)) #finds the comment in the table, refer to bottom of file for syntax
  for comment in comments:
    if re.match(' TS\n[a-zA-z]+', comment): #since there are multiple comments in the table, 
      #uses regex to match the one with the desired header ( TS symbol in example comment)
      tickers = split_comment_into_tickers(comment) #extracts the tickers from the comment
      stock_list.append((tickers)) #adds tickers to our list of stocks
  return stock_list


def main():
  config.WebscrapeOutput.clear
  stocks = []
  for page_number in range(1, 3941, 20):
    stock_list = get_stock_list(page_number)
    for nestedList in stock_list:
      for indivstock in nestedList:
        config.WebscrapeOutput.append(indivstock)
        stocks.append(indivstock)
        file.writelines(indivstock + '\n')
    logging.info(len(stocks)) #prints lengths of the list to ensure data is being added properly
    #for symbol in stock_list:
      #print(symbol)
  logging.info(len(config.WebscrapeOutput))
  file.close()
  return stocks



"""splits the comment that contains ticker data for each page
into lines, then extracts the tickers from the comment
returns the tickers to be added a larger list"""
def split_comment_into_tickers(comment):
  lines = comment.split('\n') #splits the comment by newlines
  #line format example: AAPL
  tickers = []
  for line in lines:
    try:
      ticker = line[0:line.index('|')] #takes the first 'phrase' in the sequence (the ticker)
      if re.match('^[a-zA-z]{3,}$', ticker): #regex expression for a 3+ letter combination (eliminates headers)
        tickers.append(ticker)
    except:
      continue
  return tickers

main()


"""HTML comment example (whitespace included):

 TS
ZIVO|2.43|19978
ZJYL|11.84|12311
ZKIN|0.76|15987
ZLAB|26.68|399168
ZM|68.05|2865121
ZNTL|28.99|697110
ZS|144.66|1639500
ZTEK|1.58|19814
ZUMZ|17.18|526164
ZURA|8.81|378543
ZVRA|4.98|245447
ZVSA|0.25|544303
ZYME|8.18|585311
ZYNE|0.31|910777
ZYXI|9.60|179831
TE """
