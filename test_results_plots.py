# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 00:11:23 2024

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
    
    plt.close('all')
    
    #%% read in results
    file = r"D:\VP_vdt\SYSEG - STEP Givors\Results\Boues_results.csv"
    df_results = pd.read_csv(file)
    
    for date in df_results['Date'].unique():
        
    
        results = df_results[df_results['Date'] == date]
        concs = results['Concentration'].unique()
        
        #plots for each measure
        for measure in results['Measure'].unique():
            df = vdt.single_frame(results, measure)
            fig = plt.figure(figsize = (14,8))
            axe = fig.add_axes([0.1,0.1,0.8,0.8])
            sns.barplot(x=df.index.values, y=df[measure].values, color="r",ax = axe)
            axe.set_title('{},{}'.format(measure,date))