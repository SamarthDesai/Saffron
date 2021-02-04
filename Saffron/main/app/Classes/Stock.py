class Stock:
  def __init__(self, ticker, current_price):
    self.ticker = ticker
    self.current_price = int(current_price)

  def __str__(self):
    return f"{self.ticker} is currently priced at ${self.current_price}"