from . import Transaction as Transaction

class TransactionStore:

  def __init__(self):
    self.transactions_dict = {}
    
  def addTransaction(self, transaction):
    if transaction.ticker not in self.transactions_dict.keys():
      self.transactions_dict[transaction.ticker] = []
    self.transactions_dict[transaction.ticker].append(transaction)

    
