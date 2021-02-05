from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def getRHData():

  driver = webdriver.Chrome()

  driver.get("https://www.robinhood.com/login")

  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "css-19gyy64")))

  username_input = input("Please enter your username: ")

  password_input = input("Please enter your password: ")

  if username_input and password_input:

    username = driver.find_element_by_name('username')

    username.send_keys(username_input)

    password = driver.find_element_by_xpath("//div[@class='css-19gyy64']/input[1]")

    password.send_keys(password_input)

    driver.find_element_by_class_name("css-1l2vicc").click()

  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='css-0']/button[1]")))

  driver.find_element_by_class_name("css-1l2vicc").click()

  verification_code = input("Please input your 6 digit verification code: ")

  if verification_code:

    verification_request = driver.find_element_by_name('response')
    verification_request.send_keys(verification_code)

    driver.find_element_by_class_name("_2GHn41jUsfSSC9HmVWT-eg").click()

  WebDriverWait(driver, 20).until(EC.title_contains("Portfolio"))

  driver.get("https://www.robinhood.com/account/history")

  WebDriverWait(driver, 20).until(EC.title_contains("Account"))

  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "rh-expandable-item-a32bb9ad")))

  scroll_down(driver)

  transactions = []

  sections = driver.find_elements_by_class_name("_2wuDJhUh9lal-48SV5IIfk")

  section_types = {
    "PENDING": "Pending",
    "RECENT": "Recent",
    "OLDER": "Older"
  }

  for section in sections:
    section_name = section.find_element_by_xpath(".//h2").get_attribute('textContent')
    if section_types["PENDING"] not in section_name:
      section_transactions = section.find_elements_by_class_name("rh-expandable-item-a32bb9ad")
      transactions.extend(section_transactions)

  #transactions = driver.find_elements_by_class_name("rh-expandable-item-a32bb9ad")

  transaction_types = {
      "MARKET_SELL": "Market Sell",
      "MARKET_BUY": "Market Buy",
      "LIMIT_SELL": "Limit Sell",
      "LIMIT_BUY": "Limit Buy",
      "DIVIDEND": "Dividend",
      "CANCELED": "Canceled"
  }

  transaction_arr = []
  company_name_dict = {}

  transactions_with_dates = []

  for transaction in transactions:

    header_text = transaction.find_element_by_xpath(".//div[@class='_2VPzNpwfga_8Mcn-DCUwug']").text

    if transaction_types["LIMIT_SELL"] in header_text or transaction_types["LIMIT_BUY"] in header_text or transaction_types["MARKET_SELL"] in header_text or transaction_types["MARKET_BUY"] in header_text:

      info_children = transaction.find_elements_by_xpath(".//div[@class='css-1qd1r5f']")

      date_node = info_children[7]
      date = date_node.get_attribute('textContent')

      transaction_with_date = (transaction, date)
      transactions_with_dates.append(transaction_with_date)

    elif transaction_types["DIVIDEND"] in header_text

      date_node = transaction.find_elements_by_xpath(".//span[@class='css-zy0xqa']")[1]
      date = transaction_date_node.get_attribute('textContent')

      transaction_with_date = (transaction, date)
      transactions_with_dates.append(transaction_with_date)

  sorted_transactions = transactions_with_dates.sort(key = lambda date: datetime.strptime(date[1], '%b %d, %Y')) 

  for transaction_number in range(len(sorted_transactions)-1, -1, -1):

    transaction = sorted_transactions[transaction_number][0]

    header_text = transaction.find_element_by_xpath(".//div[@class='_2VPzNpwfga_8Mcn-DCUwug']").text

    canceled_text = transaction.find_element_by_xpath(".//div[@class='_22YwnO0XVSevsIC6rD9HS3']").text

    company_name_title = header_text.split("\n")

    company_name_list = company_name_title[0].split(" ")

    print(company_name_list)
    
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
      price = price.split("$")[1]
      total_value_node = info_children[19]
      total_value = total_value_node.get_attribute('textContent')
      transaction_tuple = (ticker_symbol, transaction_type_final, quantity, price, total_value, transaction_date)
      transaction_arr.insert(0, transaction_tuple)
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
      price = price.split("$")[1]
      total_value_node = info_children[17]
      total_value = total_value_node.get_attribute('textContent')
      transaction_tuple = (ticker_symbol, transaction_type_final, quantity, price, total_value, transaction_date)
      transaction_arr.insert(0, transaction_tuple)
      continue

    if transaction_types["DIVIDEND"] in header_text:

      company_name = " ".join(company_name_list[2:])

      ticker_symbol = company_name_dict[company_name]

      info_children = transaction.find_elements_by_xpath(".//div[@class='_2SYphfY1DF71e5bReqgDyP']")

      transaction_type = "Dividend"
      transaction_date_node = transaction.find_elements_by_xpath(".//span[@class='css-zy0xqa']")[1]
      transaction_date = transaction_date_node.get_attribute('textContent')

      quantity = info_children[0].get_attribute('textContent')

      price = info_children[1].get_attribute('textContent')

      total_value = info_children[2].get_attribute('textContent')

      transaction_tuple = (ticker_symbol, transaction_type, quantity, price, total_value, transaction_date)
      transaction_arr.insert(0, transaction_tuple)

  return transaction_arr



  	# elif transaction_types[DIVIDEND] in header_text:

  #driver.close()

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