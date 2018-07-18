# -*- coding: utf-8 -*-
#
"""

# Main script governing the trading system

This is a single, standalone script which emulates a simple stock market. Many things can be configured in the code to change the possible parameters.
"""

#======================================================================
#Library Declarations as needed
import copy
import datetime
import json
import random
import os
#======================================================================

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
    locator = next(element for element in data if element["Stock_Symbol"] == symbol)
    dividend = locator['Last_Dividend']
    p_e_ratio = (price/dividend)

    return p_e_ratio

def trade_record(symbol, quantity_of_shares, movement, price):
    tradedict = {}
    list_of_trades = []
    appendtojson = (os.path.realpath(os.path.join(os.getcwd(), "trade_{}.json".format(symbol))))
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")


    if quantity_of_shares < 1:
        return "Bad number of shares"
    if movement not in ['BUY', 'SELL']:
        return "Operation is not correct"
    if price < 0:
        return "Price is not ok, check the price"

    #filling in the dictionary

    tradedict['Stock'] = symbol
    tradedict['Timestamp'] = timestamp
    tradedict['Quantity'] = int(quantity_of_shares)
    tradedict['Indicator'] = movement
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


    beautiful = "Stock:{},Timestamp:{},Quantity:{},Indicator:{},Price:{}".format(symbol,timestamp,quantity_of_shares,movement,price)

    return beautiful

def volume_weighted_stock_price(symbol):
    volumes_of_trades = []
    quantities = []
    #check number of trades in last 15 minutes, if there are sufficient for that tick/symbol, use them, else create 10 trades randomly and use them
    timenow = datetime.datetime.now()
    delta = datetime.datetime.now() - datetime.timedelta(minutes=15)
    newdelta = delta.replace(microsecond=0)
    movement_indicator = ['BUY', 'SELL']

    #We create 10 random trades for the sake of simulation

    for _ in range(10):
        trade_record(symbol, random.randint(1, 1000), random.choice(movement_indicator), round(random.uniform(0.1, 100.0),2))


    with open("trade_{}.json".format(symbol), 'r') as fi:
        timingread = json.load(fi)

    for stamp in timingread:
        current_element_stamp = stamp['Timestamp']
        new = current_element_stamp.replace('/', '-')
        compare = datetime.datetime.strptime(new, '%Y-%m-%d %H:%M:%S')
        if compare > delta:
            # print('delta is ', newdelta, 'compare is', compare, 'trade price is', stamp['Price'], 'Quantity is', stamp['Quantity'])
            price_current = stamp['Price']
            quantity_current = stamp['Quantity']
            current_volume = price_current*quantity_current
            volumes_of_trades.append(current_volume)
            quantities.append(quantity_current)

    volume_weighted_stock = (sum(volumes_of_trades)/sum(quantities))
    return round(volume_weighted_stock, 2)

def gbce_all_share_index():
    price_collection = []
    for file in os.listdir(os.getcwd()):
        if 'trade_' in file and '.json' in file:
            with open(os.path.join(os.getcwd(), file), 'r') as file:
                timingread = json.load(file)
                pricesinthisfile = [individual['Price'] for individual in timingread]
                price_collection.append(pricesinthisfile)

    single_list = [item for sub in price_collection for item in sub]
    geo_round = round(sum(single_list) ** (1.0/len(single_list)),2)

    return geo_round




if __name__ == "__main__":
    dividend = calculate_dividend_yield('POP', 86.12378676)
    print('The percentage yield is {}'.format(dividend))
    p_e_ratio_figure = p_to_e_ratio('POP', 100)
    print('The P/E ratio is {}'.format(p_e_ratio_figure))
    trade_recorded = trade_record('JOE', 12, 'SELL', 22.8)
    print('Trade recorded:  {}'.format(trade_recorded))
    vwsp = volume_weighted_stock_price('TEA')
    print('Volume Weighted Stock price: {}'.format(vwsp))
    gbce_asi = gbce_all_share_index()
    print('GBCE All Share Index: {}'.format(gbce_asi))
