# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8
import requests
import pandas as pd
#import datetime
import time

def getData(ticker, metric, no_of_days):
    
    ticker = ticker + str('.NS')
    current_time = int(round(time.time()))
    start_time = current_time - (no_of_days)*24*60*60
    
    
    resp = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/'
                        +ticker+'?formatted=true&crumb=3fOAXVz3HoU&lang=en-IN&region=IN&period1='
                        +str(start_time)+'&period2='+str(current_time)
                        +'&interval=1d&events=div%7Csplit&corsDomain=in.finance.yahoo.com')
    
    
    result = resp.json()
    
    
    timestamps = result['chart']['result'][0]['timestamp']
    values = result['chart']['result'][0]['indicators']['quote'][0][metric]
    
    #len(values)
    #datetime.datetime.fromtimestamp(timestamps[len(timestamps) - 1])
    
    
    d = {'timestamp': timestamps, 'value': values}
    dataFrame = pd.DataFrame(data=d)
    
    return dataFrame


#d = getData('MARUTI.NS', 'close', 365)




