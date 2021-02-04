from . import Transaction as Transaction

class TransactionStore:

  def __init__(self):
    self.transactions_dict = {}
    
  def addTransaction(self, ticker, price, quantity, transaction_type, transaction_date):
    transaction = Transaction.Transaction(ticker, transaction_type, quantity, price, transaction_date)
    if ticker not in self.transactions_dict.keys():
      self.transactions_dict[ticker] = []
    self.transactions_dict[ticker].append(transaction)
    
    

    
