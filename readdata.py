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

class SludgeClass():
    
    def __init__(self,conf):
        self.config = conf
        self.site = conf['client_name']
        self.batch = conf['date_of_sample']
        self.directory = conf['directory']
        self.concs = [int(c) for c in [*conf['concentrations']]] #concentrations
        
        
        #add class data for each data file
        self.data = self.get_data()
        
    def get_data(self):
        
        #go to config specific directory and extract relevant datafiles
        os.chdir(self.directory)
        
        #loop through concentrations anda add to data
        data = {}
        for conc in self.concs:
            
            #read relevant datafiles
            datafiles = self.config['concentrations'][str(conc)]['filename']
            side = find_side(self.config['concentrations'][str(conc)]['side'])
            df = read_data(datafiles,side)
            
            data[conc] = df
            
        return data
            

        
def convarea(string):
    multipliers = {'A':0,'B':1,'C':2,'D':3}
    return str(multipliers[string[0]]*5 + int(string[1]))

def wrangle(df):
    df = df['abstime time type location area data1'.split()][df.type == 101]
    df['data1'] = pd.to_numeric(df['data1'],downcast = 'integer')
    #df['plancher'] = df['location'].str[:-2] #REMOVE
    df['time'] = (df['time']/1000).astype(int) #ms
    df['zone'] = df['area'].str[-1] + '_' + df['area'].str.split('-').str[0].apply(convarea)
    df = df.reset_index(drop=True)
    df = df[['time','zone','data1']]
    return df.pivot_table(index = 'time', columns = 'zone', values = 'data1')
        
def read_data(files,side):
    """
    read all files and return df for raw data
    """
    df = pd.read_csv(files[0], sep = '\t')
    for i in range(len(files)-1):
        df = pd.concat([df,pd.read_csv(files[i+1], sep = '\t')],ignore_index = True)
        
    df = df[df['location'].str.contains(side)]
    return wrangle(df)

def find_side(string):
    left = ['left','Left','gauche','Gauche']
    right = ['right','Right','droite','Droite','droit','Droit']
    if string in left:
        return 'Gauche'
    elif string in right:
        return 'Droit'
    else:
        return None


if __name__ == "__main__":
    
    #read info about test
    config_data = 'config_data.json'
    with open(config_data, 'r') as f:
        config_data = json.load(f)
        
    data = SludgeClass(config_data)
    
    # #go to config specific directory and extract relevant datafiles
    # os.chdir(config_data['directory'])
    # all_datafiles = [f for f in os.listdir() if 'raw_0' in f]
    
    # #concentration by concentration identify datafiles for relevant concentration
    # concs = [*config_data['concentrations']]
    
    # for conc in concs[4:]:
        
    #     #read relevant datafiles
    #     datafiles = config_data['concentrations'][conc]['filename']
        
    #     #extract relevant plancher side and read data
    #     side = find_side(config_data['concentrations'][conc]['side'])
    #     df = read_data(datafiles,side)