class Transaction:

  def __init__(self, ticker, transaction_type, quantity, price, total_value, transaction_date, regulatory_fee=0):
    self.ticker = ticker
    self.type = transaction_type
    self.quantity = float(quantity)
    self.price = float(price)
    self.total_value = float(total_value)
    self.regulatory_fee = regulatory_fee
    self.date = transaction_date

  def __str__(self):
    return f"{self.type} of {self.quantity} {self.ticker} at ${self.price}"