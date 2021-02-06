from app.Functions import gains
from app.Functions import consolidate_data
from app.Classes import TransactionStore as ts
from app.Robinhood import scraper
import yfinance as yf
'''
transactions = consolidate_data.getTransactions()
stocks = consolidate_data.getStockInfo()

for stock in transactions.keys():
  arr = gains.getGains(transactions[stock], stocks[stock]['current_price'], method="AVERAGE_COST")
  print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[3]}")
  arr = gains.getGains(transactions[stock], stocks[stock]['current_price'], method="FIFO")
  print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[2]}")
'''

transactions_store = ts.TransactionStore()
transactions_arr = scraper.getRHData()

for transaction in transactions_arr:
  ticker, transaction_type, quantity, price, total_value, transaction_date = transaction
  print(transaction_type, ticker, quantity, " @ ", price, " on ", transaction_date)
  transactions_store.addTransaction(ticker, transaction_type, quantity, price, total_value, transaction_date)


for stock in transactions_store.transactions_dict.keys():
  #arr = gains.getGains(transactions_store.transactions_dict[stock], 1000, method="AVERAGE_COST")
  #print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[3]}")
  stock_current_price = ""
  try:
    stock_current_info = yf.Ticker(stock).info
    stock_current_price = stock_current_info['ask']
  except:
    stock_current_price = 0
  arr = gains.getGains(transactions_store.transactions_dict[stock], stock_current_price)
  print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[2]}")

'''
for i in range(50):
  print("\n")

for transaction in transactions_arr:
  ticker, transaction_type, quantity, price, total_value, transaction_date = transaction
  transactions_store.addTransaction(ticker, transaction_type, quantity, price, total_value, transaction_date)


for stock in transactions_store.transactions_dict.keys():
  #arr = gains.getGains(transactions_store.transactions_dict[stock], 1000, method="AVERAGE_COST")
  #print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[3]}")
  arr = gains.getGains(transactions_store.transactions_dict[stock], 1000)
  print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[2]}")
'''



