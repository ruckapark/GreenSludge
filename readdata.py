# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:11:04 2024

Inspired from previous code
Class that reads data for one individual concentration

@author: George
"""

import os
import json
import pandas as pd
import numpy as np

left = ['left','Left','gauche','Gauche']
right = ['right','Right','droite','Droite','droit','Droit']

class SludgeClass():
    
    def __init__(self,conf):
        self.site = conf['client_name']
        self.batch = conf['date_of_sample']
        
        #add class data for each data file
        
def convarea(string):
    multipliers = {'A':0,'B':1,'C':2,'D':3}
    return str(multipliers[string[0]]*5 + int(string[1]))

def wrangle(df):
    df = df['abstime time type location area data1'.split()][df.type == 101]
    df['data1'] = pd.to_numeric(df['data1'],downcast = 'integer')
    df['plancher'] = df['location'].str[:-2]
    df['time'] = (df['time']/1000).astype(int)
    df['zone'] = df['area'].str[-1] + '_' + df['area'].str.split('-').str[0].apply(convarea)
    return df[['plancher','time','zone','data1']]
        
def read_data(files):
    """
    read all files and return df for raw data
    """
    df = pd.read_csv(files[0], sep = '\t')
    for i in range(len(files)-1):
        df = df.append(pd.read_csv(files[i+1], sep = '\t'),ignore_index = True) 
    #return wrangle(df)
    return df


if __name__ == "__main__":
    
    #read info about test
    config_data = 'config_test.json'
    with open(config_data, 'r') as f:
        config_data = json.load(f)
        
    data = SludgeClass(config_data)
    
    #go to config specific directory and extract relevant datafiles
    os.chdir(config_data['directory'])
    all_datafiles = [f for f in os.listdir() if '0001.xls' in f]
    
    #concentration by concentration identify datafiles for relevant concentration
    concs = [*config_data['concentrations']]
    for conc in concs[:1]:
        
        #read relevant datafiles
        datafiles = config_data['concentrations'][conc]['filename']
        
        #extract relevant plancher side
        side = config_data['concentrations'][conc]['side']
        if side in left:
            side = 'Gauche'
        else:
            side = 'Droit'
            
        df = read_data(datafiles)