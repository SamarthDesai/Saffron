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

def getCurrentPrice(ticker):
  stock_current_price = float(0)
  try:
    stock_current_info = yf.Ticker(ticker).info
    stock_current_price = (float(stock_current_info['ask']) + float(stock_current_info['ask']))/2
    if (float(stock_current_info['ask']) == float(0) or float(stock_current_info['buy']) == float(0)):
      stock_current_price = float(stock_current_info['open'])
  except:
    pass
  return stock_current_price

transactions_store = ts.TransactionStore()
transactions_arr = scraper.getRHData()

for transaction in transactions_arr:
  print(transaction.type, transaction.ticker, transaction.quantity, " @ ", transaction.price, " on ", transaction.date)
  transactions_store.addTransaction(transaction)

index = 0

total_gains = float(0)
for stock in transactions_store.transactions_dict.keys():

  #arr = gains.getGains(transactions_store.transactions_dict[stock], 1000, method="AVERAGE_COST")
  #print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[3]}")
  stock_current_price = getCurrentPrice(stock)
  arr = gains.getGains(transactions_store.transactions_dict[stock], stock_current_price)
  total_gains+= (float(arr[0]) + float(arr[2]))
  print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[2]}")

print("Total gains: ", total_gains)
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




