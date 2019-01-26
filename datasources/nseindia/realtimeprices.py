# -*- coding: utf-8 -*-

import requests
import pandas as pd

def get_real_time_data():
    val = requests.get('https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json').json()
    
    symbols = []
    last_trading_prices = []
    for i in range(0,len(val['data'])):
        symbols.append(val['data'][i]['symbol'])
        last_trading_prices.append(val['data'][i]['ltP'])
    
    d = {'symbol': symbols, 'last_trading_price': last_trading_prices}
    dataFrame = pd.DataFrame(data = d)
    return dataFrame

g = get_real_time_data()

