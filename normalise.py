# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:11:04 2024

Read one sludge test with Sludge class (only one concentration)

@author: George
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# import dataread class
import dataReadSludge as dR

sns.set_style("whitegrid")
import functions_vdt as vdt

def get_upper_quantile(dataset: dR.SludgeClass):
    
    data_arr = np.array([],dtype = int)
    for conc in dataset.concs:
        df = dataset.data[conc].copy()
        arr = np.array(df.values).flatten()
        arr = arr[arr!=0]
        data_arr = np.concatenate((data_arr,arr))
        
    return np.nanquantile(data_arr,0.975)

if __name__ == "__main__":

    plt.close("all")

    # read json info about test - for each new test, copy config_data file to working directory
    config_data = r"config_data.json"  # test3
    with open(config_data, "r") as f:
        config_data = json.load(f)

    data = dR.SludgeClass(config_data)

    # %% test active columns

    for conc in data.concs:
        vdt.plotgraphs(data.data[conc], 20, data.active_cols[conc], title=conc)

    # %% Sort to order of concentration
    dataset_scores = {i: {} for i in data.concs}
    start_zones = {i: [] for i in data.concs}
    
    # %% Normalise data #(G is boue) #(D is water)
    data_arr = {'G':np.array([],dtype = int),'D':np.array([],dtype = int)}
    for side in ['G','D']:
        for conc in data.concs:
            df = data.data[conc].copy()
            cols = [c for c in list(df.columns) if side in c]
            df = df[cols]
            arr = np.array(df.values).flatten()
            arr = arr[arr != 0]
            data_arr[side] = np.concatenate((data_arr[side], arr))
            
    fig_hist,axe_hist = plt.subplots(ncols = 2, sharex = True, figsize = (14,8))
    for i,side in enumerate(data_arr):
        axe_hist[i].hist(data_arr[side],bins=40)
        axe_hist[i].axvline(np.nanquantile(data_arr[side], 0.975),color = 'r',linestyle = '--')
        
    # %% Show all the dataset can be taken without effect
    data_arr = np.array([],dtype = int)
    for conc in data.concs:
        df = data.data[conc].copy()
        arr = np.array(df.values).flatten()
        arr = arr[arr!=0]
        data_arr = np.concatenate((data_arr,arr))
        
    fig = plt.figure(figsize = (14,7))
    axe = fig.add_axes([0.1,0.1,0.8,0.8])
    axe.hist(data_arr,bins = 40)
    upper_quantile = np.nanquantile(data_arr,0.975)
    axe.axvline(upper_quantile,color = 'r',linestyle = '--')
    
    #add to data class
    print('Upper quantile: ', get_upper_quantile(data))
    
    # %% Plot normalised data
    for conc in data.concs:
        vdt.plotgraphs(data.data_[conc], 20, data.active_cols[conc], title=conc)