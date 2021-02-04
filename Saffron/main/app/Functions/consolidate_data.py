from ..Classes import Transaction
from ..Classes import Stock
from . import data_reader as dr

def getTransactions():
  TRANSACTION_DATA_PATH = '../Data/sample_transactions.txt'
  transaction_dict = {}

  transaction_data = dr.data_reader(TRANSACTION_DATA_PATH)

  for line in transaction_data:
    stripped_line = line.rstrip()
    transaction_info = [item.strip() for item in stripped_line.split(" ")]
    transaction = Transaction.Transaction(transaction_info[0], transaction_info[1], transaction_info[2], transaction_info[3])
    addTransaction(transaction_dict, transaction)
  return transaction_dict
  
def addTransaction(transaction_dict, transaction):
  if transaction.ticker not in transaction_dict.keys():
    transaction_dict[transaction.ticker] = []
  transaction_dict[transaction.ticker].append(transaction)

def getStockInfo():
  STOCK_DATA_PATH = '../Data/stocks.txt'

  stock_dict = {}

  stock_data = dr.data_reader(STOCK_DATA_PATH)

  for line in stock_data:
    stripped_line = line.rstrip()
    stock_info = [item.strip() for item in stripped_line.split(" ")]
    stock = Stock.Stock(stock_info[0], stock_info[1])
    addStock(stock_dict, stock)
  return stock_dict

def addStock(stock_dict, stock):
  if stock.ticker not in stock_dict.keys():
    stock_dict[stock.ticker] = {"current_price": stock.current_price}
