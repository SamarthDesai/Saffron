from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import os
import time
from datetime import datetime
import locale
import pickle
import platform
import yfinance
from ..Classes import Transaction

LOGIN_PAGE = "Login"
HISTORY_PAGE = "History"
PORTFOLIO_PAGE = "Portfolio"
MFA_PAGE = "MFA"

COOKIES_PATH_PREFIX = "../Data/"
COOKIES_PATH_SUFFIX = "_cookies.txt"

transaction_types = {
    "MARKET_SELL": "Market Sell",
    "MARKET_BUY": "Market Buy",
    "LIMIT_SELL": "Limit Sell",
    "LIMIT_BUY": "Limit Buy",
    "DIVIDEND": "Dividend",
    "FREE": "from Robinhood",
    "CANCELED": "Canceled"
}


section_types = {
  "PENDING": "Pending",
  "RECENT": "Recent",
  "OLDER": "Older"
}


class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass


def getRHData():


  driver, saffronUsername = createSession()

  navigateToRobinhood(driver)

  currentPage = checkCurrentPage(driver)

  while currentPage != HISTORY_PAGE:
    if (currentPage == LOGIN_PAGE):
      enterUserCredentials(driver)
      letNonLoginPageLoad(driver)

    if (currentPage == MFA_PAGE):
      enterMFA(driver)
      letNonMFAPageLoad(driver)

    if (currentPage == PORTFOLIO_PAGE):
      navigateToHistoryPage(driver)

    currentPage = checkCurrentPage(driver)

  #at this point you should be at the history page

  scroll_down(driver)
  
  transactions = gatherTransactions(driver)

  
  transaction_arr = parseTransactions(driver, transactions)
      
  endSession(driver, saffronUsername)

  return transaction_arr



  	# elif transaction_types[DIVIDEND] in header_text:

  #driver.close()

def createSession():
  username = input("Please enter your Saffron username: ")

  driver = webdriver.Chrome()
  navigateToRobinhood(driver)

  fileName = COOKIES_PATH_PREFIX + username.rstrip() + COOKIES_PATH_SUFFIX
  
  fileDir = os.path.dirname(os.path.realpath(__file__))
  filePath = os.path.join(fileDir, fileName)
  filePath = os.path.abspath(os.path.realpath(filePath))

  try:
    cookieFile = open(filePath)
    loadCookies(driver, filePath)
  except: #TODO: catch specific exceptions here
    pass 
  

  return (driver, username)


def endSession(driver, username):
  fileName = COOKIES_PATH_PREFIX + username.rstrip() + COOKIES_PATH_SUFFIX
  
  fileDir = os.path.dirname(os.path.realpath(__file__))
  filePath = os.path.join(fileDir, fileName)
  filePath = os.path.abspath(os.path.realpath(filePath))

  open(filePath, "w").close() #creates file if doesn't exist, clears contents if it does
  saveCookies(driver, filePath)
  driver.quit()
  #driver.close() TODO: might be worth testing out if quit or close is better


def saveCookies(driver, filePath):
    with open(filePath, 'wb') as filehandler:
        cookies = driver.get_cookies()
        pickle.dump(cookies, filehandler)



def loadCookies(driver, filePath):
  with open(filePath, 'rb') as cookiesfile:
      cookies = pickle.load(cookiesfile)
      
      for cookie in cookies:
        driver.add_cookie(cookie)



def navigateToRobinhood(driver):

  driver.get("https://robinhood.com/account/history")

def navigateToStock(driver, stock_ticker):

  driver.get(f"https://robinhood.com/stocks/{stock_ticker}")

  WebDriverWait(driver, 20).until(AnyEc(
    EC.presence_of_element_located((By.CLASS_NAME, "Jo5RGrWjFiX_iyW3gMLsy"))
    )
  )


def letPageLoad(driver):
  WebDriverWait(driver, 20).until(AnyEc(
      EC.presence_of_element_located((By.CLASS_NAME, "css-16758fh")),
      EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad")),
      EC.title_contains("Portfolio"),
      EC.presence_of_element_located((By.CLASS_NAME, "css-1upilqn"))
      )
  )

def letNonLoginPageLoad(driver):
  WebDriverWait(driver, 20).until(AnyEc(
      EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad")),
      EC.title_contains("Portfolio"),
      EC.presence_of_element_located((By.CLASS_NAME, "css-1upilqn")),
      )
  )

def letNonMFAPageLoad(driver):
  WebDriverWait(driver, 20).until(AnyEc(
      EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad")),
      EC.title_contains("Portfolio")
      )
  )


def checkCurrentPage(driver):
  letPageLoad(driver)

  loginPageCheck = driver.find_elements_by_class_name("css-16758fh")
  historyPageCheck = driver.find_elements_by_class_name("rh-expandable-item-a32bb9ad")
  mfaPageCheck = driver.find_elements_by_class_name("css-1upilqn")
  if loginPageCheck:
    return LOGIN_PAGE
  if historyPageCheck:
    return HISTORY_PAGE
  if mfaPageCheck:
    return MFA_PAGE
  return PORTFOLIO_PAGE


def enterUserCredentials(driver):
  username_input = input("Please enter your Robinhood username: ")

  password_input = getpass("Please enter your Robinhood password: ")

  if username_input and password_input:

    username = driver.find_element_by_name('username')

    username.send_keys(username_input)

    password = driver.find_element_by_xpath("//div[@class='css-19gyy64']/input[1]")

    password.send_keys(password_input)

    driver.find_element_by_class_name("css-1l2vicc").click()

  #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='css-0']/button[1]")))

  #driver.find_element_by_class_name("css-1l2vicc").click()




def enterMFA(driver):
  driver.find_element_by_class_name("css-1l2vicc").click()
  verification_code = input("Please input your 6 digit verification code: ")

  if verification_code:

    verification_request = driver.find_element_by_name('response')
    verification_request.send_keys(verification_code)

    driver.find_element_by_class_name("_2GHn41jUsfSSC9HmVWT-eg").click()



def navigateToHistoryPage(driver):
  driver.get("https://www.robinhood.com/account/history")

  WebDriverWait(driver, 50).until(EC.title_contains("Account"))

  WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad")))



def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height


def gatherTransactions(driver):
  transactions = []
  sections = driver.find_elements_by_class_name("_2wuDJhUh9lal-48SV5IIfk")

  for section in sections:
    section_name = section.find_element_by_xpath(".//h2").get_attribute('textContent')
    if section_types["PENDING"] not in section_name:
      section_transactions = section.find_elements_by_class_name("rh-expandable-item-a32bb9ad")
      transactions.extend(section_transactions)
  return transactions


def parseTransactions(driver, transactions):
  if platform.system() == 'Darwin':
    locale.setlocale(locale.LC_NUMERIC, "EN_US")
  else:
    locale.setlocale(locale.LC_NUMERIC, "")

  transaction_arr = []
  company_name_dict = {}

  transactions_with_dates = []

  for transaction in transactions:

    header_text = transaction.find_element_by_xpath(".//div[@class='_2VPzNpwfga_8Mcn-DCUwug']").text

    canceled_text = transaction.find_element_by_xpath(".//div[@class='_22YwnO0XVSevsIC6rD9HS3']").text

    if transaction_types["CANCELED"] in canceled_text:
      continue

    if transaction_types["LIMIT_SELL"] in header_text or transaction_types["LIMIT_BUY"] in header_text or transaction_types["MARKET_SELL"] in header_text or transaction_types["MARKET_BUY"] in header_text:

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")

      date_node = info_children[7]
      date = date_node.get_attribute('textContent')

      transaction_with_date = (transaction, date)
      transactions_with_dates.append(transaction_with_date)

    elif transaction_types["DIVIDEND"] in header_text:

      date_node = transaction.find_elements_by_xpath(".//span[@class='css-zy0xqa']")[1]
      date = date_node.get_attribute('textContent')

      transaction_with_date = (transaction, date)
      transactions_with_dates.append(transaction_with_date)

    elif transaction_types["FREE"] in header_text:

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")

      date_node = info_children[5]
      date = date_node.get_attribute('textContent')

      transaction_with_date = (transaction, date)
      transactions_with_dates.append(transaction_with_date)

  for transaction_with_date in transactions_with_dates:
    print(transaction_with_date)

  transactions_with_dates.sort(key = lambda date: datetime.strptime(date[1], '%b %d, %Y'))

  dividends_from_free_stocks = []

  free_stocks = []

  for transaction_with_date in transactions_with_dates:

    transaction = transaction_with_date[0]

    header_text = transaction.find_element_by_xpath(".//div[@class='_2VPzNpwfga_8Mcn-DCUwug']").text

    canceled_text = transaction.find_element_by_xpath(".//div[@class='_22YwnO0XVSevsIC6rD9HS3']").text

    company_name_title = header_text.split("\n")

    company_name_list = company_name_title[0].split(" ")
    
    if transaction_types["CANCELED"] in canceled_text:
      continue


    if transaction_types["LIMIT_SELL"] in header_text or transaction_types["LIMIT_BUY"] in header_text:

      company_name = " ".join(company_name_list[:-2])


      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")
      ticker_symbol_node = info_children[1]
      ticker_symbol = ticker_symbol_node.find_element_by_xpath(".//a").get_attribute('textContent')

      if company_name not in company_name_dict.keys():
        company_name_dict[company_name] = ticker_symbol

      transaction_type_node = info_children[3]
      transaction_type = transaction_type_node.find_element_by_xpath(".//span").get_attribute('textContent')
      transaction_type_split = transaction_type.split(" ")
      transaction_type_final = transaction_type_split[1]
      transaction_date_node = info_children[7]
      transaction_date = transaction_date_node.get_attribute('textContent')
      filled_transaction_node = info_children[17]
      filled_transaction = filled_transaction_node.get_attribute('textContent')
      filled_transaction_split = filled_transaction.split(" ")
      quantity = filled_transaction_split[0]
      price = filled_transaction_split[3]
      price = locale.atof(price.split("$")[1])
      total_value_node = info_children[19]
      total_value = locale.atof(total_value_node.get_attribute('textContent').split("$")[1])
      
      transaction_obj = Transaction.Transaction(ticker_symbol, transaction_type, quantity, price, total_value, transaction_date)

      transaction_arr.append(transaction_obj)

      continue

    if transaction_types["MARKET_SELL"] in header_text or transaction_types["MARKET_BUY"] in header_text:

      company_name = " ".join(company_name_list[:-2])

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")
      ticker_symbol_node = info_children[1]
      ticker_symbol = ticker_symbol_node.find_element_by_xpath(".//a").get_attribute('textContent')

      if company_name not in company_name_dict.keys():
        company_name_dict[company_name] = ticker_symbol

      transaction_type_node = info_children[3]
      transaction_type = transaction_type_node.find_element_by_xpath(".//span").get_attribute('textContent')
      transaction_type_split = transaction_type.split(" ")
      transaction_type_final = transaction_type_split[1]
      transaction_date_node = info_children[7]
      transaction_date = transaction_date_node.get_attribute('textContent')
      filled_transaction_node = info_children[15]
      filled_transaction = filled_transaction_node.get_attribute('textContent')
      filled_transaction_split = filled_transaction.split(" ")
      quantity = filled_transaction_split[0]
      price = filled_transaction_split[3]
      price = locale.atof(price.split("$")[1])
      total_value_node = info_children[17]
      total_value = locale.atof(total_value_node.get_attribute('textContent').split("$")[1])

      transaction_obj = Transaction.Transaction(ticker_symbol, transaction_type, quantity, price, total_value, transaction_date)

      transaction_arr.append(transaction_obj)

      continue

    if transaction_types["DIVIDEND"] in header_text:

      company_name = " ".join(company_name_list[2:])

      ticker_symbol = ""

      if company_name in company_name_dict.keys():

        ticker_symbol = company_name_dict[company_name]

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")

      transaction_type = "Dividend"
      transaction_date_node = transaction.find_elements_by_xpath(".//span[@class='css-zy0xqa']")[1]
      transaction_date = transaction_date_node.get_attribute('textContent')

      quantity = info_children[1].get_attribute('textContent')

      price = locale.atof(info_children[3].get_attribute('textContent').split("$")[1])

      total_value = locale.atof(info_children[5].get_attribute('textContent').split("$")[1])

      transaction_obj = Transaction.Transaction(ticker_symbol, transaction_type, quantity, price, total_value, transaction_date)

      transaction_arr.append(transaction_obj)

      if ticker_symbol == "":
        dividends_from_free_stocks.append((transaction_obj, company_name))

      continue

    if transaction_types["FREE"] in header_text:

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")

      ticker_symbol = company_name_list[0]

      # company_name = yfinance.Ticker(ticker_symbol).info

      # stock_driver = webdriver.Chrome()

      print("KD > LEBRON")

      transaction_type = "Free"
      transaction_date_node = info_children[5]
      transaction_date = transaction_date_node.get_attribute('textContent')

      quantity_and_total_value_node = info_children[7]
      quantity_and_total_value = quantity_and_total_value_node.get_attribute('textContent')

      quantity = quantity_and_total_value.split(" ")[0]

      price = 0

      total_value = locale.atof(quantity_and_total_value.split(" ")[3].split("$")[1])

      transaction_obj = Transaction.Transaction(ticker_symbol, transaction_type, quantity, price, total_value, transaction_date)

      free_stocks.append(transaction_obj)

      transaction_arr.append(transaction_obj)

  for free_stock in free_stocks:

    ticker = free_stock.ticker

    navigateToStock(driver, ticker)

    company_name = driver.find_element_by_xpath("//header[@class='Jo5RGrWjFiX_iyW3gMLsy']/h1[1]").text

    if company_name not in company_name_dict.keys():
      company_name_dict[company_name] = ticker

  for dividend in dividends_from_free_stocks:
    dividend_obj, company_name = dividend
    dividend_obj.ticker = company_name_dict[company_name]

  return transaction_arr



