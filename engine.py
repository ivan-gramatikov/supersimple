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
import copy
import os
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
        return "Not Proper Type of Stock"

    return dividend_yield*100

def p_to_e_ratio(symbol, price):
    locator = next(item for item in data if item["Stock_Symbol"] == symbol)
    dividend = locator['Last_Dividend']
    p_e_ratio = (price/dividend)
    return p_e_ratio

def trade_record(symbol, quantity_of_shares, movement, price):
    tradedict = {}
    list_of_trades = []
    appendtojson = (os.path.realpath(os.path.join(os.getcwd(), "trade_{}.json".format(symbol))))
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    if quantity_of_shares < 1:
        return "Bad number of shares"
    if movement not in ['BUY', 'SELL']:
        return "Operation is not correct"
    if price < 0:
        return "Price is not ok, check the price"

    tradedict['Stock'] = symbol
    tradedict['Timestamp'] = timestamp
    tradedict['Quantity'] = quantity_of_shares
    tradedict['Movement'] = movement
    tradedict['Price'] = float(price)

    list_of_trades.append(copy.deepcopy(tradedict))

    if os.path.isfile(appendtojson):
        with open("trade_{}.json".format(symbol), 'r') as fileobj:
            tradingdata = json.load(fileobj)
            tradingdata.append(tradedict)

        with open("trade_{}.json".format(symbol), 'w') as fileob:
            json.dump(tradingdata, fileob, indent=4)


    if not os.path.isfile(appendtojson):
        with open("trade_{}.json".format(symbol), 'w') as newj:
            json.dump(list_of_trades, newj, indent=4)



    #return singleline

def volume_weighted_stock_price():
    pass

if __name__ == "__main__":
    dividend = calculate_dividend_yield('POP', 86.12378676)
    print('The percentage yield is {}'.format(dividend))
    p_e_ratio_figure = p_to_e_ratio('POP', 100)
    print('The P/E ratio is {}'.format(p_e_ratio_figure))
    trade_recorded = trade_record('ALE', 40, 'BUY', 41)
    print('Trade recorded: {}'.format(trade_recorded))
