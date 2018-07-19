# -*- coding: utf-8 -*-
#
"""

# Main script governing the trading system

This is a standalone script which emulates a simple stock market.
"""

# ======================================================================
# Library Declarations as needed
import copy
import datetime
import json
import random
import os
import operator
import functools

# ======================================================================


def main_data(symbol):
    """
    This function merely reads the table of the example stock data provided with the task

    :param symbol: The stock symbol the user is interested in investigating
    :return: Returns the locator for further seeking in the example data table given
    """
    # We import the json file where the sample data has been written
    try:
        with open('sample_data_gbce.json') as stock_market_data:
            example_stock_data = json.load(stock_market_data)
        # We create a locator for the rest of the functions to use which helps point to the stock the user needs
    except IOError:
        print(
            'Error! The file sample_data_gbce.json has not been found. It is requred for the program to run correctly. Please put it back in the folder where the script is located!\n')
        return False

    locator = next(item for item in example_stock_data if item["Stock_Symbol"] == symbol)

    # We output the locator
    return locator


def calculate_dividend_yield(symbol, price):
    """
    This function calculates Dividend Yield given a price and the specific stock symbol the user provides

    :param symbol: The stock symbol the user is interested in investigating
    :param price: The user passes the input price that is needed to calculate dividend yield
    :return: The dividend yield is calculated and returned (rounded up to 2 digits)
    """
    # We take the locator from the output of the main_data function above

    locator = main_data(symbol)
    if not locator:
        raise ValueError(
            'Error! The locator could not be found. The file sample_data_gbce.json is probably missing. It is requred for the program to run correctly. Please put it back in the folder where the script is located!\n')
        return False
    # And distribute to the respective variables from the json base
    type_of_stock = locator['Type']
    fixed_dividend = locator['Fixed_Dividend']
    last_dividend = locator['Last_Dividend']
    par_value = locator['Par_Value']

    # We handle the two cases - when we need to calculate by the Dividend Yield formula of Preferred and by the formula of Common stock
    if type_of_stock == 'Preferred':
        dividend_yield = ((fixed_dividend * par_value) / price)
    elif type_of_stock == 'Common':
        dividend_yield = (last_dividend / price)
    else:
        raise ValueError(
            'Not proper type of stock! Stock is {} and it should be either Preferred or Common'.format(type_of_stock))
        return False

    return round(dividend_yield * 100, 2)


def p_to_e_ratio(symbol, price):
    """
    This function calculates the P/E ratio given the stock and a price

    :param symbol: The stock symbol the user is interested in investigating
    :param price: The user passes the input price that is needed to calculate dividend yield
    :return: The P/E ratio is calculated and returned (rounded up to 2 digits after the floating point)
    """
    # We take the locator from the output of the main_data function above
    locator = main_data(symbol)
    if not locator:
        raise ValueError(
            'Error! The locator could not be found. The file sample_data_gbce.json is probably missing. It is requred for the program to run correctly. Please put it back in the folder where the script is located!\n')
        return False
    # We take the variable we need for the calculation of the P/E ratio from the table
    last_dividend = locator['Last_Dividend']
    # We calculate the P/E ratio
    p_e_ratio = (price / last_dividend)

    # And return the P/e ratio
    return p_e_ratio


def trade_record(symbol, quantity_of_shares, movement, price):
    """
    This function aims to emulate the recording of a trade. The recorded trade will be outputed on the screen. A file with the respective stock symbol will be created with a recorded trade as well in the json format, named

    :param symbol: The stock symbol the user is interested in investigating
    :param quantity_of_shares: Quantity of shares the user has bought
    :param movement: The indicator of the trade - has the user bought or sold the stock
    :param price: The price at which the user has bought the given stock
    :return: The function returns a recorded trade.
    """
    # We initialize variables as needed
    tradedict = {}
    list_of_trades = []

    # We take the path to the recorded trade json file so we append to it as needed
    appendtojson = (os.path.realpath(os.path.join(os.getcwd(), "trade_{}.json".format(symbol))))
    # We create a timestamp in the format Year-Month-Day Hours:Minutes:Seconds
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # We make a few sanity checks for the input values
    if quantity_of_shares < 1:
        raise ValueError("Bad number of shares! User cannot buy or sell less than 1 ")
        return False

    if movement not in ['BUY', 'SELL']:
        raise ValueError(
            "The user needs to either enter BUY or SELL for the respective operation they want to perform  for the record of the trade")
        return False

    if price < 0:
        raise ValueError(
            "The user needs to either enter BUY or SELL for the respective operation they want to perform  for the record of the trade")
        return False

    # We fill in the dictionary of the trade to be written. Input is taken from the user.
    tradedict['Stock'] = symbol
    tradedict['Timestamp'] = timestamp
    tradedict['Quantity'] = int(quantity_of_shares)
    tradedict['Indicator'] = movement
    tradedict['Price'] = float(price)

    # We take the contents of the dictionary we just filled and put in a variable for later writing
    list_of_trades.append(copy.deepcopy(tradedict))

    # If there is already such a file for the respective stock, we open it and append to it
    if os.path.isfile(appendtojson):
        try:
            with open("trade_{}.json".format(symbol), 'r') as fileobj:
                tradingdata = json.load(fileobj)
                tradingdata.append(tradedict)
        except IOError:
            print('Error! The File trade_{}.json could not be read.'.format(symbol))
            return False

        try:
            with open("trade_{}.json".format(symbol), 'w') as fileob:
                json.dump(tradingdata, fileob, indent=4)
        except IOerror:
            print('Error! The File trade_{}.json could not be written to.'.format(symbol))
            return False

    # If there is no file that contains trades recorded for this particular stock, we create one and write the contents of the list we created above (list_of_trades)
    if not os.path.isfile(appendtojson):
        try:
            with open("trade_{}.json".format(symbol), 'w') as newj:
                json.dump(list_of_trades, newj, indent=4)
        except IOError:
            print('Error! The program attempted to create the file trade_{}.json but did not manage to.'.format(symbol))
            return False

    # Write the trade recorded to a variable so its contents can be shown to the user
    beautiful = "Stock:{}, Timestamp:{}, Quantity:{}, Indicator:{}, Price:{} ".format(symbol, timestamp,
                                                                                      quantity_of_shares,
                                                                                      movement, price)
    # Return the recorded trade
    return beautiful


def volume_weighted_stock_price(symbol):
    """
    This function takes the recorded trades of the last 15 minutes for a given stock from the local file and calculates the Volume Weighted Stock Price

    :param symbol: The stock symbol the user is interested in investigating
    :return: Output is the calculated volume weighted stock price
    """

    # We initialize variables as needed
    volumes_of_trades = []
    quantities = []

    # We create a time marker to know how long was 15 minutes from 'now'
    timenow = datetime.datetime.now()
    delta = datetime.datetime.now() - datetime.timedelta(minutes=15)
    newdelta = delta.replace(microsecond=0)
    # The movement can be either BUY or SELL and it is randomly chosen
    movement_indicator = ['BUY', 'SELL']

    # We create 10 random trades for the sake of simulation where the user only gives the symbol initially. These will surely be included among the chosen trades of last 15 minutes.
    # We call the trade_record() function and instruct it to take random prices, random trade indicator, and random quantity
    for _ in range(10):
        trade_record(symbol, random.randint(1, 1000), random.choice(movement_indicator),
                     round(random.uniform(0.1, 100.0), 2))

    # We read the file with the 10 trades written just now so as to gather the needed data
    try:
        with open("trade_{}.json".format(symbol), 'r') as fi:
            timingread = json.load(fi)
    except IOError:
        print('Error! The program attempted to read the file trade_{}.json but did not manage to.'.format(symbol))
        return False

    # We iterate over the json to find out the data needed
    for stamp in timingread:
        # We reformat datetime format of the data we need
        current_element_stamp = stamp['Timestamp']
        new = current_element_stamp.replace('/', '-')
        compare = datetime.datetime.strptime(new, '%Y-%m-%d %H:%M:%S')
        # If the trades are from last 15 minutes, append to a list of the trade volumes of all the trades of the last 15 minutes (by multiplying price times quantity of the trade) and a list of the quantities of shares
        if compare > delta:
            price_current = stamp['Price']
            quantity_current = stamp['Quantity']
            current_volume = price_current * quantity_current
            volumes_of_trades.append(current_volume)
            quantities.append(quantity_current)

    # Calculate the Volume Weighted Stock and return it as output, rounded up to 2 digits after the floating point)
    volume_weighted_stock = (sum(volumes_of_trades) / sum(quantities))
    return round(volume_weighted_stock, 2)


def gbce_all_share_index():
    """
    This function calculates the GBCE all share index by gathering from the local directory all the trade records files and taking from them the prices to which geometric mean will later be used

    :return: All share index is returned as output
    """
    # Variable initialization
    price_collection = []
    # Going over all the files in the current working directory where the python script is located
    for file in os.listdir(os.getcwd()):
        # Check if we have a valid named record file
        if 'trade_' in file and '.json' in file:
            # We attempt to read the files and more specifically, the prices of the trades placed
            try:
                with open(os.path.join(os.getcwd(), file), 'r') as file:
                    timingread = json.load(file)
                    pricesinthisfile = [individual['Price'] for individual in timingread]
                    price_collection.append(pricesinthisfile)
            except IOError:
                print('Error! The program attempted to read the file trade_{}.json but did not manage to.'.format(symbol))
                return False



    # We calculate the geometric mean of all the prices to get the All Share Index as required
    single_list = [item for sub in price_collection for item in sub]
    print(single_list)
    elements_multiplied = functools.reduce(operator.mul, single_list, 1)
    print(elements_multiplied)
    gbce_all_share_indx = (elements_multiplied**(1.0/len(single_list)))

    return gbce_all_share_indx




if __name__ == "__main__":
    dividend = calculate_dividend_yield('JOE', 5.5455)
    print('The dividend yield is {}%'.format(dividend))
    p_e_ratio_figure = p_to_e_ratio('POP', 100)
    print('The P/E ratio is {}'.format(p_e_ratio_figure))
    trade_recorded = trade_record('JOE', 12, 'SELL', 22.8)
    print('Trade recorded:  {}'.format(trade_recorded))
    vwsp = volume_weighted_stock_price('TEA')
    print('Volume Weighted Stock price: {}'.format(vwsp))
    gbce_asi = gbce_all_share_index()
    print('GBCE All Share Index: {}'.format(gbce_asi))
