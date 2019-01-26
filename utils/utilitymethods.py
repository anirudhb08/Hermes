# -*- coding: utf-8 -*-
equity_list = []

def get_equity_list():
    
    if(len(equity_list) != 0):
        return equity_list
    
    file = open("../nifty50_stocks.csv", "r")
    lines = file.readlines()
    
    for i in range(1,len(lines)):
        #print(lines[i])
        result = [x.strip() for x in lines[i].split(',')]
        equity_list.append(result[2])
    
    file.close()
    return equity_list

f = get_equity_list()