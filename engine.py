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
import numpy as np
import sys


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

    # We check if the stock symbol exists in the database
    list_of_symbols = [di['Stock_Symbol'] for di in example_stock_data if 'Stock_Symbol' in di]

    # Otherwise we sound an alarm:
    if symbol not in list_of_symbols:
        raise ValueError('Stock symbol not in database')
        return False

    #We test if the stock symbol is within the provided data..
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
    # Safety measures to ensure what has been passed will be the proper type
    symbol = str(symbol)
    price = float(price)

    # Some sanity checks
    if price < 0:
        raise ValueError(
            "The user needs to enter a positive price")
        return False


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
        try:
            dividend_yield = ((fixed_dividend * par_value) / price)
        except ZeroDivisionError:
            return False
    elif type_of_stock == 'Common':
        try:
            dividend_yield = (last_dividend / price)
        except ZeroDivisionError:
            return False
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
    # Safety measures to ensure what has been passed will be the proper type
    symbol = str(symbol)
    price = float(price)
    p_e_ratio = 0
    # We take the locator from the output of the main_data function above
    locator = main_data(symbol)
    if not locator:
        raise ValueError(
            'Error! The locator could not be found. The file sample_data_gbce.json is probably missing. It is requred for the program to run correctly. Please put it back in the folder where the script is located!\n')
        return False

    # Some sanity checks
    if price < 0.0:
        raise ValueError('Error, the input price the user has given cannot be negative.')

    # We take the variable we need for the calculation of the P/E ratio from the table
    last_dividend = locator['Last_Dividend']
    # We calculate the P/E ratio
    try:
        p_e_ratio = (price / float(last_dividend))
        return round(p_e_ratio, 2)
    except ZeroDivisionError:
        print('The value of {} must have been 0 because division by 0 is detected and is not allowed!'.format(symbol))
        return False

    # And return the P/e ratio


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

    # Safety measures to ensure what has been passed will be the proper type
    symbol = str(symbol)
    quantity_of_shares = int(quantity_of_shares)
    movement = str(movement)
    price = float(price)


    # Some sanity checks
    if price < 0:
        raise ValueError(
            "The user needs to enter a positive price")
        return False

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
            "The user needs to enter a positive price")
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
                print("File trade_{}.json has been written with the trade information provided by the user!".format(symbol))

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

    # Safety measures to ensure what has been passed will be the proper type
    symbol = str(symbol)

    # We create a time marker to know how long was 15 minutes from 'now'
    timenow = datetime.datetime.now()
    delta = datetime.datetime.now() - datetime.timedelta(minutes=15)
    newdelta = delta.replace(microsecond=0)
    # The movement can be either BUY or SELL and it is randomly chosen
    movement_indicator = ['BUY', 'SELL']

    # We create 10 random trades for the sake of simulation where the user only gives the symbol initially. These will surely be included among the chosen trades of last 15 minutes.
    # We call the trade_record() function and instruct it to take random prices, random trade indicator, and random quantity
    for _ in range(3):
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
    This function calculates the GBCE all share index by gathering from the local directory all the trade records files and taking from them the prices to which geometric mean will later be used.
    The user must make sure to first use the functionality which writes down trades and then run this function as sufficient number of price data must be gathered.

    Reason: The definition of the All-Share-Index from the Cambridge Dictionary is as follows:
    a series of numbers which shows the changing average value of the share prices of all companies on a stock exchange, and which is used as a measure of how well a market is performing.


    :return: All share index is returned as output
    """
    # Variable initialization
    price_collection = []
    flag_file_dictionary = []

    # Going over all the files in the current working directory where the python script is located
    list_of_files_locally = [current_element for current_element in os.listdir(os.getcwd()) if os.path.isfile(current_element)]
    for individual_file in list_of_files_locally:
        # Check if we have a valid named record file
        if 'trade_' in individual_file and '.json' in individual_file:
            flag_file_dictionary.append(individual_file)

    # If there is an insufficient number of local simulated trades files, alert the user:
    if len(flag_file_dictionary) < 2:
        raise ValueError(
            'Error! Insufficient number of trades recorded! Please run the trade record option at least twice for DIFFERENT stocks to acquire sufficient price data to calculate the All Share Index meaningfully\n')
        return False


    for file in flag_file_dictionary:
        # We attempt to read the files and more specifically, the prices of the trades placed
        try:
            with open(os.path.join(os.getcwd(), file), 'r') as file:
                timingread = json.load(file)
        except IOError:
            print('Error! The program attempted to read the file trade_{}.json but did not manage to.'.format(symbol))
            return False

    pricesinthisfile = [individual['Price'] for individual in timingread]
    price_collection.append(pricesinthisfile)

    # We calculate the geometric mean of all the prices to get the All Share Index as required
    single_list = [item for sub in price_collection for item in sub]
    log_domain = np.log(single_list)
    gbce_all_share_indx = np.exp(log_domain.sum()/len(log_domain))


    return round(gbce_all_share_indx,2)

def main():
    """
    Command Line Interface menu - argument parsing function

    :return: Nothing, this is a distribution of arguments type of function
    """

    if len(sys.argv[0:])<2:
        sys.exit("""
        Super Simple Stock Market Engine v1.0

        The code supports the following functionality:
        1. Dividend Yield:

        The dividend yield is calculated when the user passes the stock symbol and price desired.

        Example: `python3 engine.py --d POP 149` or `python3 engine.py --dividend-yield POP 149`

        2. P/E ratio:

        The P/E ratio is calculated when the user passes the stock symbol and price desired.

        Example:
        `python3 engine.py --pe POP 140` or `python3 engine.py --p-to-e-ratio POP 140`

        3.  Trade Record Creation:

        The trade record is created as a file and the user receives what information has been recorded when the user passes the stock, quantity of shares, indicator (BUY or SELL) and price.

        Example:
        `python3 engine.py --tr JOE 12 SELL 22.8` or `python3 engine.py --trade-record JOE 12 SELL 22.8`

        4. Volume Weighted Stock Price:

        The volume weighted stock price creates a file (if the stock symbol has not already been used to produce a trade record) and the user receives a figure for the volume weighted stock price when the user passes the stock symbol desired.

        Example:
        `python3 engine.py --vwsp TEA` or `python3 engine.py --volume-weighted-stock-price TEA`

        5. The Global Beverage Commerce Exchange All Share Inex will be automatically calculated, provided the user has recorded trades for MORE THAN 2 stock indices. No input from the user is required otherwise.

        Example:
        `python3 engine.py --asi` or `python3 engine.py --all-share-index`

        To run tests:
        `python3 test_engine.py`

        """)

    if sys.argv[1] == '--d' or sys.argv[1] == '--dividend-yield':
        if sys.argv[2] == 'h':
            sys.exit('Help: The dividend yield is calculated when the user passes the stock symbol and price desired. Example: python3 engine.py --d POP 149 ')
        dividend = calculate_dividend_yield(sys.argv[2], sys.argv[3])
        if not dividend:
            print('Error! \n')
        else:
            print('The dividend yield is {}%'.format(dividend))


    if sys.argv[1] == '--pe' or sys.argv[1] == '--p-to-e-ratio':
        if sys.argv[2] == 'h':
            sys.exit('Help: The P/E ratio is calculated when the user passes the stock symbol and price desired. Example: python3 engine.py --pe POP 140 or --p-to-e-ratio POP 140 ')
        p_e_ratio_figure = p_to_e_ratio(sys.argv[2], sys.argv[3])
        if not p_e_ratio_figure:
            print('Error! \n')
        else:
            print('The P/E ratio is {}'.format(p_e_ratio_figure))


    if sys.argv[1] == '--tr' or sys.argv[1] == '--trade-record':
        if sys.argv[2] == 'h':
            sys.exit('Help: The trade record is created as a file and the user receives what information has been recorded when the user passes the stock, quantity of shares, indicator (BUY or SELL) and price. Example: python3 engine.py --tr JOE, 12, SELL, 22.8 or --trade-record JOE 12 SELL 22.8')
        trade_recorded = trade_record(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        if not trade_recorded:
            print('Error! \n')
        else:
            print('Trade recorded:  {}'.format(trade_recorded))



    if sys.argv[1] == '--vwsp' or sys.argv[1] == '--volume-weighted-stock-price':
        if sys.argv[2] == 'h':
            sys.exit('Help: The volume weighted stock price creates a file (if the stock symbol has not already been used to produce a trade record) and the user receives a figure for the volume weighted stock price when the user passes the stock symbol desired. Example: python3 engine.py --vwsp TEA or --volume-weighted-stock-price TEA')
        vwsp = volume_weighted_stock_price(sys.argv[2])
        if not vwsp:
            print('Error! \n')
        else:
            print('Volume Weighted Stock price: {}'.format(vwsp))



    if sys.argv[1] == '--asi' or sys.argv[1] == '--all-share-index':
        if sys.argv[2] == 'h':
            sys.exit('The Global Beverage Commerce Exchange All Share Inex will be automatically calculated, provided the user has recorded trades for MORE THAN 2 stock indices. No input from the user is required otherwise. Example: python3 engine.py --asi or python3 engine.py --all-share-index')
        gbce_asi = gbce_all_share_index()
        if not gbce_asi:
            print('Error! \n')
        else:
            print('GBCE All Share Index: {}'.format(gbce_asi))


if __name__ == "__main__":
    main()
