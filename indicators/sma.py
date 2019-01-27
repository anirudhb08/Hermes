# -*- coding: utf-8 -*-
import pandas as pd

def get_simple_moving_average(data, window_length):
    sma = data['value'].rolling(window = window_length).mean()
    d = {'timestamp': data['timestamp'], 'sma': sma}
    dataFrame = pd.DataFrame(data=d)
    
    return dataFrame


