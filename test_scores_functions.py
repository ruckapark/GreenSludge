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


if __name__ == "__main__":

    plt.close("all")

    # read json info about test - for each new test, copy config_data file to working directory
    config_data = r"config_data.json"  # test3
    with open(config_data, "r") as f:
        config_data = json.load(f)

    data = dR.SludgeClass(config_data)

    # %% test active columns

    for conc in data.concs:
        vdt.plotgraphs(data.data[conc], data.active_cols[conc], title=conc)

    # %% Sort to order of concentration
    dataset_scores = {i: {} for i in data.concs}
    start_zones = {i: [] for i in data.concs}
    changes = {i: [] for i in data.concs}
    signs = {i: [] for i in data.concs}
    activity = {i: [] for i in data.concs}
    activity_left = {i: [] for i in data.concs}
    activity_right = {i: [] for i in data.concs}
    pref_zone = {i: [] for i in data.concs}
    end_zone = {i: [] for i in data.concs}
    zonetime = {i: [] for i in data.concs}
    
    maxampG = {i: [] for i in data.concs}
    maxampD = {i: [] for i in data.concs}
    
    meanampG = {i: [] for i in data.concs}
    meanampD = {i: [] for i in data.concs}

    # calculate scores for tests
    #this should in itself be a class called scores
    for conc in data.concs:

        # extract data
        df = data.data[conc].copy()
        active_cols = data.active_cols[conc]

        # determine if worm starts on right or left
        start_zones[conc] = vdt.find_startzone(data.data[conc], data.active_cols[conc])
        if conc == 0:
            start_zones[0] = start_zones[0][:10]
        
        
        #individually calculate scores
        
        #changes
        changes[conc],signs[conc] = vdt.find_all_changes(data.data_[conc], data.fps, data.active_cols[conc], conc = conc)
        
        #total activity measures (and left and right)
        activity[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], conc = conc)
        activity_left[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], side = 'G', conc = conc)
        activity_right[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], side = 'D', conc = conc)
        
        #prevalent zone
        pref_zone[conc] = vdt.find_all_prefzone(data.data_[conc], data.fps, data.active_cols[conc],conc = conc)
        
        #finalzone
        end_zone[conc] = vdt.find_all_endzone(data.data_[conc], data.fps, data.active_cols[conc],conc = conc)
        
        #zonetime
        zonetime[conc] = vdt.find_all_zonetime(signs[conc], data.active_cols[conc], conc = conc)
        
        #amplitudes
        maxampG[conc] = vdt.find_all_maxamp(data.data_[conc], data.fps, data.active_cols[conc], side = 'G', conc = conc)
        maxampD[conc] = vdt.find_all_maxamp(data.data_[conc], data.fps, data.active_cols[conc], side = 'D', conc = conc)
        
        meanampG[conc] = vdt.find_all_meanamp(data.data_[conc], data.fps, data.active_cols[conc], side = 'G', conc = conc)
        meanampD[conc] = vdt.find_all_meanamp(data.data_[conc], data.fps, data.active_cols[conc], side = 'D', conc = conc)