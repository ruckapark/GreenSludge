# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 08:41:26 2024

Decide which measures are of interest

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
        
if __name__ == "__main__":
    
    plt.close('all')
    
    #%% read in results
    file = r"D:/VP_vdt/SYSEG - STEP Givors/Results/Boues_results.csv"
    results_dir = r"D:/VP_vdt/SYSEG - STEP Givors/Results"
    df_results = pd.read_csv(file)
    
    #define different measures, sides of interests and concentrations
    measures = df_results['Measure'].unique()
    sides = [None,'leftside','rightside']
    concs = df_results['Concentration'].unique()
    colors = ['orange','red','blue']
    
    #intialise side_dictionary 
    side_dict = None
    
    for measure in measures:
        
        #plotting space to compare measures
        fig,axe = plt.subplots(3,3,sharex = True,figsize = (14,8))
        
        results = df_results[df_results['Measure'] == measure]
        
        #loop through dates and plot choosing three side possibilities
        for col,date in enumerate(df_results['Date'].unique()):
            
            #define dataframe overall
            df_measure = results[results['Date'] == date]
            axe[0,col].set_title(date)
            
            for row,side in enumerate(sides):
                
                #define subset df
                df = df_measure.copy()
                if col == 0:
                    axe[row,col].set_ylabel(side)
                
                #select columns of interest
                if side:
                    if side == 'leftside':
                        side_dict = left_na_starts
                    else:
                        side_dict = right_na_starts
                        
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
                sns.barplot(x=df_plot.index.values, y=df_plot[measure].values, color=colors[row],ax = axe[row,col])
            fig.suptitle('{}'.format(measure))
            
            #calculate