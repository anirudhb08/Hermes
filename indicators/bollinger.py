# -*- coding: utf-8 -*-

import pandas as pd

def get_bollinger_bands(data, window_length, variation):
    sma = data['value'].rolling(window = window_length).mean()
    std = data['value'].rolling(window = window_length).std()

    d = {'timestamp': data['timestamp'], 'sma': sma, 'std': std}
    dataFrame = pd.DataFrame(data=d)
    
    dataFrame['upper_band'] = dataFrame['sma'] + variation*dataFrame['std']
    dataFrame['lower_band'] = dataFrame['sma'] - variation*dataFrame['std']
    
    return dataFrame
