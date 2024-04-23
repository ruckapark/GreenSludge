# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 08:41:26 2024

Calculate scores only using the left side to calculate the zones

@author: George
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
import functions_vdt as vdt

date1 = '23/09/11'
date2 = '23/12/14'
date3 = '23/10/18'

right_na_starts = {
    0:np.arange(5),
    20:np.arange(10),
    40:np.arange(10),
    60:np.arange(10),
    80:np.arange(10),
    100:np.arange(10)
     }

left_na_starts = {
    0:np.arange(5,10),
    20:np.arange(10,20),
    40:np.arange(10,20),
    60:np.arange(10,20),
    80:np.arange(10,20),
    100:np.arange(10,20)
     }

scores_measures = ['changes','preferred_zone','zone_time','max_amplitude_left']

scores = dict(zip(scores_measures,np.zeros(len(scores_measures))))
        
if __name__ == "__main__":
    
    plt.close('all')
    
    #%% read in results
    file = r"D:/VP_vdt/SYSEG - STEP Givors/Results/Boues_results.csv"
    results_dir = r"D:/VP_vdt/SYSEG - STEP Givors/Results"
    df_results = pd.read_csv(file)
    
    #define different measures, sides of interests and concentrations
    measures = scores_measures
    concs = df_results['Concentration'].unique()
    
    #intialise side_dictionary 
    side_dict = left_na_starts
    
    for measure in measures:
        
        #plotting space to compare measures
        fig,axe = plt.subplots(1,3,sharex = True,figsize = (8,3),sharey=True)
        results = df_results[df_results['Measure'] == measure]
        
        #loop through dates and plot choosing three side possibilities
        for col,date in enumerate(df_results['Date'].unique()):
            
            #define dataframe overall
            df_measure = results[results['Date'] == date]
            axe[col].set_title(date)
            
            
            #define subset df only with leftside start organisms
            df = df_measure.copy()
            side_dict = left_na_starts
                    
            
            #filter results to only retain values from one side
            for conc in concs:
                
                if side_dict != None:
                    na_locs = np.ones(20)
                    na_locs[side_dict[conc]] = np.nan
                    original_values = df.loc[results['Concentration'] == conc, [str(i) for i in range(1,21)]].values
                    temp = original_values.flatten()*na_locs
                    cols = [str(i) for i in range(1,21)]
                    
                    df.loc[df['Concentration'] == conc, [str(i) for i in range(1,21)]] = original_values.flatten()*na_locs
                        
            #plot filtered data on multi plots
            df_plot = vdt.single_frame(df, measure)
            sns.barplot(x=df_plot.index.values, y=df_plot[measure].values, color='red',ax = axe[col])
            
            #calculate scores
            score = 0
            if measure == 'changes':
            
                #temoin value
                arr = df.loc[df['Concentration'] == 0, [str(i) for i in range(1,21)]].values
                arr = arr[~np.isnan(arr)]
                median_zero = np.median(arr)
                
                #negative changes are positive avoidance from temoin
                for conc in concs[1:]:
                    arr = df.loc[df['Concentration'] == conc, [str(i) for i in range(1,21)]].values
                    arr = arr[~np.isnan(arr)]
                    median = np.median(arr)
                    
                    avoidance = median/median_zero - 1 
                    score += avoidance
                    
                print(date,measure,-score/5)
                
            elif measure == 'zone_time':
                
                #temoin value
                arr = df.loc[df['Concentration'] == 0, [str(i) for i in range(1,21)]].values
                arr = arr[~np.isnan(arr)]
                median_zero = np.median(arr)
                
                #negative changes are positive avoidance from temoin
                for conc in concs[1:]:
                    arr = df.loc[df['Concentration'] == conc, [str(i) for i in range(1,21)]].values
                    arr = arr[~np.isnan(arr)]
                    median = np.median(arr)
                    
                    avoidance = median/median_zero - 1 
                    score += avoidance
                    
                print(date,measure,score/5)
                
            elif measure == 'max_amplitude_left':
                
                #+ve is avoidance from temoin
                #temoin value
                arr = df.loc[df['Concentration'] == 0, [str(i) for i in range(1,21)]].values
                arr = arr[~np.isnan(arr)]
                median_zero = np.median(arr)
                
                #negative changes are positive avoidance from temoin
                for conc in concs[1:]:
                    arr = df.loc[df['Concentration'] == conc, [str(i) for i in range(1,21)]].values
                    arr = arr[~np.isnan(arr)]
                    median = np.median(arr)
                    
                    avoidance = median - median_zero
                    score += avoidance
                    
                print(date,measure,score/5)
        
            fig.suptitle('{}'.format(measure))
            plt.tight_layout()