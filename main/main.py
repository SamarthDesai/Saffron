from app.Functions import gains
from app.Functions import consolidate_data
from app.Classes import TransactionStore as ts
from app.Robinhood import scraper

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
  print(transaction.type, transaction.ticker, transaction.quantity, " @ ", transaction.price, " on ", transaction.date)
  transactions_store.addTransaction(transaction)

index = 0

for stock in transactions_store.transactions_dict.keys():

  #arr = gains.getGains(transactions_store.transactions_dict[stock], 1000, method="AVERAGE_COST")
  #print(f"{stock} \n realized gains: {arr[0]} \n remaining shares: {arr[1]} \n unrealized gains: {arr[3]}")
  arr = gains.getGains(transactions_store.transactions_dict[stock], 1000)
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



