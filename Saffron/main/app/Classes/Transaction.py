class Transaction:

  def __init__(self, ticker, transaction_type, quantity, price, transaction_date="2020"):
    self.ticker = ticker
    self.type = transaction_type
    self.quantity = float(quantity)
    self.price = float(price)
    self.date = transaction_date

  def __str__(self):
    return f"{self.type} of {self.quantity} {self.ticker} at ${self.price}"