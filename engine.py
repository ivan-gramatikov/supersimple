# -*- coding: utf-8 -*-
#
"""

# Main script governing the trading system
"""

#----------------------------------------------------------------------
#Library Declarations as needed
import json
import datetime
import random

#----------------------------------------------------------------------
#Variable Declarations as needed

#----------------------------------------------------------------------

with open('sample_data_gbce.json') as stock_market_data:
    data = json.load(stock_market_data)


def calculate_dividend_yield(symbol, price):
    locator = next(item for item in data if item["Stock_Symbol"] == symbol)
    type = locator['Type']
    fixed_dividend = locator['Fixed_Dividend']
    last_dividend = locator['Last_Dividend']
    par_value = locator['Par_Value']

    if type == 'Preferred':
        dividend_yield = ((fixed_dividend*par_value)/price)
    elif type == 'Common':
        dividend_yield = (last_dividend/price)
    else:
        return -1

    return dividend_yield*100

def p_to_e_ratio(symbol, price):
    locator = next(item for item in data if item["Stock_Symbol"] == symbol)
    dividend = locator['Last_Dividend']
    p_e_ratio = (price/dividend)
    return p_e_ratio

def trade_record(quantity_of_shares, movement, price):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    if quantity_of_shares < 1:
        return -1
    if movement != 'SELL' or movement != 'BUY':
        return -1
    if price < 0:
        return -1

    record_trade = [timestamp, quantity_of_shares, movement, price]
    trade = ":".join(record_trade)
    #quantity_of_shares = random.randint(1, 1000)
    #buy_sell = random.choice('BUY', 'SELL')
    #leaving those two for simulation purposes
    return trade

if __name__ == "__main__":
    dividend = calculate_dividend_yield('POP', 10)
    print('The percentage yield is {}'.format(dividend))
    p_e_ratio_figure = p_to_e_ratio('POP', 100)
    print('The P/E ratio is {}'.format(p_e_ratio_figure))
    trade_recorded = trade_record(140, 'BUY', 15.4",".join(myList ))
    print('Timestamp is {}'.format(trade_recorded))
