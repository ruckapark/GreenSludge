# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:19:45 2024

Datapoints were generated using test_avoidance_scores in develop branch

Perform sum of changes and left max amplitude

Values
18/10/2023 - 206.66
09/11/2023 - 224.54
14/12/2023 - 33.26


@author: George
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

dates = ["18/10/2023","09/11/2023","14/12/2023"]
values = np.array([206.66,224.54,33.26])

#define reference toxicity
ref_value = 1000

#determine whether to rescale
rescale = False
if max(values) < 400: rescale = True

#define figure for plotting
tox_fig = plt.figure()
tox_axe = tox_fig.add_axes([0.1,0.1,0.8,0.8])

#figure control
title = "GreenSludge Indices - SYSEG"
ylabel = "GreenSludge Indice"
xlabel = ""

tox_axe.plot(dates,values,'ko')

tox_axe.set_ylabel(ylabel)
tox_axe.set_xlabel(xlabel)
tox_axe.set_xticklabels(dates, rotation=30)
plt.tight_layout()

if not rescale:
    tox_axe.axhline(1000,color = 'r',linestyle = '--',label = "Reference de toxicite")
else:
    tox_axe.axhline(max(values)*1.25,color = 'r',linestyle = '--',label = "Reference de toxicite = 1000")
    
    tox_axe.plot([-0.3, -0.2], [260, 270], 'black')
    tox_axe.plot([-0.3, -0.2], [253, 263], 'black')
    tox_axe.set_xlim([-0.3,2.5])
    
tox_fig.legend(loc = 'upper right',fontsize = 12)
tox_axe.grid(True)
    
    
    