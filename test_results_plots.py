# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 00:11:23 2024

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
    
    for date in df_results['Date'].unique():
        
    
        results = df_results[df_results['Date'] == date]
        concs = results['Concentration'].unique()
        measures = results['Measure'].unique()
        
        side = 'rightside'
        if side:
            if side == 'leftside':
                side_dict = left_na_starts
            else:
                side_dict = right_na_starts
                
            #filter results to only retain values from one side
            for conc in concs:
                na_locs = np.ones((len(measures),20))
                na_locs[:,side_dict[conc]] = np.nan
                original_values = results.loc[results['Concentration'] == conc, [str(i) for i in range(1,21)]].values
                results.loc[results['Concentration'] == conc, [str(i) for i in range(1,21)]] = original_values*na_locs
            
        
        #plots for each measure
        for measure in measures:
            df = vdt.single_frame(results, measure)
            fig = plt.figure(figsize = (14,8))
            axe = fig.add_axes([0.1,0.1,0.8,0.8])
            sns.barplot(x=df.index.values, y=df[measure].values, color="r",ax = axe)
            axe.set_title('{},{}'.format(measure,date))
            
            if side:
                fname = "{}_{}_{}.PNG".format(measure,side,date.replace('/','_'))
            else:
                fname = "{}_{}.PNG".format(measure,date.replace('/','_'))
                
            fig.savefig(os.path.join(results_dir,fname))