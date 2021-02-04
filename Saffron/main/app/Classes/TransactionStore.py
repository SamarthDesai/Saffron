from . import Transaction as Transaction

class TransactionStore:

  def __init__(self):
    self.transactions_dict = {}
    self.NEW_TRANSACTION_INDEX = -1 #TODO: this isn't used
    self.OLD_TRANSACTION_INDEX = 0
    
  def addTransaction(self, ticker, price, quantity, transaction_type, transaction_date):
    transaction = Transaction.Transaction(ticker, transaction_type, quantity, price, transaction_date)
    if ticker not in self.transactions_dict.keys():
      self.transactions_dict[ticker] = []
      self.transactions_dict[ticker].append(transaction)
    else:
      self.transactions_dict[ticker].append
      (self.OLD_TRANSACTION_INDEX, transaction)
    

    
