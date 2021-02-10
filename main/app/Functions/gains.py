from collections import deque 

#for stock in x.keys():
#  getRealizedGainForTicker(stock, x[stock])
  
class CostBasisPosition:

  def __init__(self, price, quantity, date):
    self.price = price
    self.quantity = quantity
    self.date = date


def getGains(transaction_arr, current_price, method="FIFO"):
  if method == "FIFO":
    return getFIFOGains(transaction_arr, current_price)
  if method == "AVERAGE_COST":
    return getAverageCostGains(transaction_arr, current_price)




def getAverageCostGains(transaction_arr, current_price):
  stock_quantity_held = 0
  stock_revenue_total = 0
  realized_gains = 0
  stock_cost_total = float(0)
  stock_average_price_bought = float(0)

  for transaction in transaction_arr:
    if transaction.type == "buy":
      stock_quantity_held += transaction.quantity
      stock_cost_total += (transaction.quantity*transaction.price)
      stock_average_price_bought = stock_cost_total/stock_quantity_held
    else:
      #remove quantity from stock_quantity_held
      #remove quantity*avg from stock_cost_total, #then recalculate average
      revenue = float(transaction.price*transaction.quantity)
      cost = (transaction.quantity*stock_average_price_bought)
      stock_revenue_total += revenue
      realized_gains += (revenue - cost)
      stock_quantity_held -= transaction.quantity
      stock_cost_total -= (transaction.quantity*stock_average_price_bought)
  unrealized_gains = calculateUnrealizedGains(stock_quantity_held, stock_average_price_bought, current_price)
  return [realized_gains, stock_quantity_held, stock_average_price_bought, unrealized_gains]


def calculateUnrealizedGains(quantity, buy_price, current_price):
  return (quantity*(current_price - buy_price))

def getNetGains(transaction_arr, current_price):
  gains_arr = getGains(transaction_arr, current_price)
  return (gains_arr[0] + gains_arr[3])



def getFIFOGains(transaction_arr, current_price):

  bought_shares_queue = deque()
  gain = float(0)
  quantity_shares_remaining = 0

  for transaction in transaction_arr:
    if transaction.type == "Buy" or transaction.type == "Free":
      cost_basis_buy = CostBasisPosition(transaction.price, transaction.quantity, transaction.date) #TODO, FIX TRANSACTION DATE from 1
      bought_shares_queue.append(cost_basis_buy)
      quantity_shares_remaining += transaction.quantity
    elif transaction.type == "Sell":
      sell_price = transaction.price
      sell_quantity = transaction.quantity
      partial_gain = determineFIFOGain(bought_shares_queue, sell_price, sell_quantity)
      gain += (partial_gain - transaction.regulatory_fee)
      quantity_shares_remaining -= sell_quantity
    elif transaction.type == "Dividend":
      gain += transaction.total_value

  unrealized_gains = determineFIFOGain(bought_shares_queue, current_price, quantity_shares_remaining)

  return [gain, quantity_shares_remaining, unrealized_gains]


def determineFIFOGain(held_shares_queue, sell_price, sell_quantity):
  #use popleft to pull, and appendleft to add back
  gain = float(0)
  while sell_quantity > 0:
    oldest_shares = held_shares_queue.popleft()
    share_deficit = oldest_shares.quantity - sell_quantity
    if (share_deficit <= 0):
      #fewer bought shares than sold
      sold_shares_quantity = oldest_shares.quantity
      partial_gain = (sell_price - oldest_shares.price)*sold_shares_quantity
      sell_quantity -= sold_shares_quantity
      gain += partial_gain
    else: 
      #more bought shares than sold
      sold_shares_quantity = sell_quantity
      partial_gain = (sell_price - oldest_shares.price)*sold_shares_quantity
      sell_quantity = 0
      gain += partial_gain
      oldest_shares.quantity -= sold_shares_quantity
      held_shares_queue.appendleft(oldest_shares)
  return gain

