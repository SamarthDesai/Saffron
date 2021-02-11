from scipy import optimize
from datetime import datetime
from datetime import date
from ..Classes import Transaction
from ..Classes import CurrentPosition


def XNPV(rate, cashflows):
    t0 = cashflows[0][0]
    return sum([cf/(1+rate)**((t-t0).days/365.0) for (t,cf) in cashflows])


def XIRR_Calc(transaction_array, guess=0.1):
    buy_count = 0

    cashflow_array = []
    for transaction in transaction_array:
        date = datetime.strptime(transaction.date, '%b %d, %Y').date()
        cashflow = transaction.price*transaction.quantity
        if (transaction.type != "Sell" and transaction.type != "Dividend"):
            cashflow = cashflow * -1
        cashflow_array.append((date, cashflow))
        if (transaction.type == "Buy"):
            buy_count+=1
    if (buy_count == 0):
        return "Infinite"
    return optimize.newton(lambda rate: XNPV(rate, cashflow_array), guess)


#ticker, transaction_type, quantity, price, total_value, transaction_date, regulatory_fee=0
def test():   
    t1 = Transaction.Transaction("A", "Buy", 2, 1, 2, "Jan 1, 2016", 0)
    t3 = Transaction.Transaction("A", "Sell", 1, 100, 100, "Dec 1, 2016", 0)
    t_arr = [t1, t3]
    current_position = CurrentPosition.CurrentPosition("A", 1)
    current_position_store = {"A": current_position}
    tickers = ["A"]
    current_prices = {"A": 150}


    xirr = XIRR(t_arr)
    print(xirr)


def XIRR(transaction_array, current_positions=None, tickers=[], current_prices={}):
    if not current_positions:
        return XIRR_Calc(transaction_array)
    transactions_with_unrealized = transaction_array.copy() #copy makes sure modifying new list won't modify old one
    for ticker in tickers:
        quantity_left = current_positions[ticker].quantity
        current_price = current_prices[ticker]
        transaction_type = "Sell"
        transaction_date = date.today().strftime("%b %d, %Y")
        unrealized_gains_transaction = Transaction.Transaction(ticker, transaction_type,
            quantity_left, current_price, current_price*quantity_left, transaction_date)
        transactions_with_unrealized.append(unrealized_gains_transaction)
    return XIRR_Calc(transactions_with_unrealized)





