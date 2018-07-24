# supersimple

Requirements
1. Provide working source code that will :-
a. For a given stock,
i. Given any price as input, calculate the dividend yield
ii. Given any price as input,  calculate the P/E Ratio
iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
Constraints & Notes
1. Written in one of these languages:
	· Java, C#, C++, [Python]
2. No database or GUI is required, all data need only be held in memory
3. No prior knowledge of stock markets or trading is required – all formulas are provided below.


-----------------------------------------------------------------
Stock Symbol | Type | Last Dividend | Fixed Dividend | Par Value|
| ---------- |:----:|:-------------:|:--------------:|---------:|
TEA          |Common|             0 |                |       100|
POP          |Common|             8 |                |       100|
ALE          |Common|            23 |                |        60|
GIN       |Preferred|             8 |              2%|       100|
JOE          |Common|            13 |                |       250|
-----------------------------------------------------------------
#All number values in pennies


Dividend Yield:
Common: `(Last Dividend)/Price`

Preferred: `(Fixed Dividend*Par Value)/Price`

P/E Ratio: `Price/Dividend`

Geometric Mean: `Squareroot(n)[p1p2p3...pn]`

Volume Weighted Stock Price: `SUM(i)[Traded Price(i) x Quantity(i)]/Sum(i)[Quantity]`

NB: The output of Dividend Yield is multiplied by 100 to give a percentage figure, as in:
Last dividend = 8, Price = 100, DY for Common type of stock = 8/100 = 0.08 and then the output would be 0.08*100 = 8
Part of the definition:  "Dividend yield is represented as a percentage [..]"
Source: https://www.investopedia.com/terms/d/dividendyield.asp

-----------------------------------------------------------------
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
`python3 engine.py --asi <path_to_script_directory>` or `python3 engine.py --all-share-index <path_to_script_directory>`

To run tests:
`python3 test_engine.py`

One can also run the script like
`python3 engine.py <switch> h` as in: `python3 engine.py --d h` to get help of a certain function or do `python3 engine.py` to view this help message
