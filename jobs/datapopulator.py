# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
 
import utils.utilitymethods as utilities
import datasources.yahoofinance.historicaldata as datafetcher

def populate_historical_data():
    equities = utilities.get_equity_list()
    for i in range(0,1):
        datafetcher.getData(equities[i]+'.NS', 'open', 365)
        #push_data_to_db

#populate_historical_data()
        
