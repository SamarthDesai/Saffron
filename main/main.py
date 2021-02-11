from app.Functions import gains
from app.Functions import consolidate_data
from app.Classes import TransactionStore as ts
from app.Robinhood import scraper
import yfinance as yf
from app.Functions import XIRR
from app.Classes import CurrentPositionStore as curr_pos_store
from app.Classes import CurrentPosition as curr_pos





transactions_store = ts.TransactionStore()
current_positions_store = curr_pos_store.CurrentPositionStore()
transactions_arr = scraper.getRHData()
current_stock_prices = {}


def getCurrentPrice(ticker):
  stock_current_price = float(0)
  try:
    stock_current_info = yf.Ticker(ticker).info
    stock_current_price = (float(stock_current_info['ask']) + float(stock_current_info['bid']))/2
    if (float(stock_current_info['ask']) == float(0) or float(stock_current_info['bid']) == float(0)):
      stock_current_price = float(stock_current_info['open'])
  except:
    pass
  current_stock_prices[ticker] = stock_current_price
  return stock_current_price




for transaction in transactions_arr:
  print(transaction.type, transaction.ticker, transaction.quantity, " @ ", transaction.price, " on ", transaction.date)
  transactions_store.addTransaction(transaction)

index = 0

total_realized_gains = float(0)
total_unrealized_gains = float(0)
for stock in transactions_store.transactions_dict.keys():
  try:

    stock_current_price = getCurrentPrice(stock)
    arr = gains.getGains(transactions_store.transactions_dict[stock], stock_current_price)
    current_position = curr_pos.CurrentPosition(stock, arr[1])
    current_positions_store.addCurrentPosition(current_position)
    total_realized_gains += float(arr[0])
    total_unrealized_gains += float(arr[2])
    realized_xirr = XIRR.XIRR_Calc(transactions_store.transactions_dict[stock])

    print(f"{stock} \n realized gains: {arr[0]} \n realized irr: {realized_xirr} \n remaining shares: {arr[1]} \n unrealized gains: {arr[2]}")
  except:
    continue


total_gains = total_realized_gains + total_unrealized_gains
print("Total Realized Gains: ", total_realized_gains, "Total Unrealized Gains: ", total_unrealized_gains, "Total Gains: ", total_gains)
total_realized_irr = XIRR.XIRR(transactions_arr)
print("Total Realized IRR: ", total_realized_irr)

total_irr = XIRR.XIRR(transactions_arr, current_positions_store.current_position_dict, 
  transactions_store.transactions_dict.keys(), current_stock_prices)

print(total_irr, " is the total irr")



