### Explore the potential efficient frontier of a stock portfolio with different weights of custom stocks

Requires a free [Quandl account](https://www.quandl.com/) for an API Key to retrieve historic stock data.  

#### How to use:

1- Clone the repo

2- Install TA-Lib, for financial technical analysis - requires compiling C for your environment, follow instructions here:  https://github.com/mrjbq7/ta-lib 

3- Activate your virtual environment, and install all the project requirements with `pip install -r requirements.txt`

4- Edit the script `retrieve_stock_history.py` with new date ranges and ticker symbols of currently publicly traded companies you are interested in.  Feel free to change the name of the output file to whatever you prefer.

5- Run `python retrieve_stock_history.py` 

6- Launch the jupyter from your terminal with `jupyter lab` or `jupyter notebook`

7- Analyze and explore
