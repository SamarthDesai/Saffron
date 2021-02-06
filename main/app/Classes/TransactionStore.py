from . import Transaction as Transaction

class TransactionStore:

  def __init__(self):
    self.transactions_dict = {}
    
  def addTransaction(self, ticker, transaction_type, quantity, price, total_value, transaction_date):
    transaction = Transaction.Transaction(ticker, transaction_type, quantity, price, total_value, transaction_date)
    if ticker not in self.transactions_dict.keys():
      self.transactions_dict[ticker] = []
    self.transactions_dict[ticker].append(transaction)

    
