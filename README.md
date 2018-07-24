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
