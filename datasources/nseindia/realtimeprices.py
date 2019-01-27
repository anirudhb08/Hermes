# -*- coding: utf-8 -*-

import requests
import pandas as pd

def get_real_time_data(metric):
    val = requests.get('https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json').json()
    
    symbols = []
    metric_values = []
    for i in range(0,len(val['data'])):
        symbols.append(val['data'][i]['symbol'])
        metric_values.append(val['data'][i][metric])
    
    d = {'symbol': symbols, 'metric': metric_values}
    dataFrame = pd.DataFrame(data = d)
    return dataFrame

g = get_real_time_data('ltP')

