# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 15:56:49 2021

Functions to be used for vdts

Read in as vdt to use functions

@author: Admin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import os

LIMIT = 3000

def find_startzone(df,active_cols):
    """ Gauche = 0, Droite = 1"""
    vals = {'G':0,'D':1}
    startzones = np.zeros(20)
    for i in range(1,21):
        if 'G_{}'.format(i) not in active_cols: continue
        tempdata = df[['G_{}'.format(i),'D_{}'.format(i)]]
        start_act = {'G':0,'D':0}
        start_act['G'] = sum(tempdata.iloc[:150,0] > 0)
        start_act['D'] = sum(tempdata.iloc[:150,1] > 0)
        startzones[i-1] = vals[max(start_act, key = start_act.get)]
        
    return startzones

def find_site(s):
    if 'Pierre Bénite' in s:
        site = 1
    else:
        site = 2
    return site


def find_startzones():
    #ensure order or missing vdt are accounted for here
    return None

def find_prefzone(df):
    """
    Find zone most visited by the vdt :
        Count instances on each side - not amplitude.
    """
    column = df.columns
    gauche = sum(df[column[0]] > 0)
    droite = sum(df[column[1]] > 0)
    if gauche > droite:
        return 0
    else:
        return 1
    
def find_all_prefzone(df, fps, active_cols, conc = 20, window = 60):
    """
    Find the zone in which orgnaism spends most time after first minute (window)
    
    Parameters
    ----------
    df : pd.DataFrame
        dataframe of greensludge test at given concentration.
    fps : int
        fps of video or recording.
    active_cols : list
        active columns.

    Returns
    -------
    array of preferred sides.

    """
    
    #at conc 0 only 10 organisms
    if conc:
        pref_zone = np.zeros(20)
    else:
        pref_zone = np.zeros(10)
    
    #loop through indidivudals
    for i in range(1,len(pref_zone)+1):
        if "G_{}".format(i) not in active_cols:
            continue
        cols = ["G_{}".format(i),"D_{}".format(i)]
        pref = find_prefzone(df[cols].iloc[window*fps:])
        pref_zone[i-1] = pref
        
    return pref_zone
    
    
def find_zonetime(changes,start_zone,window = 10):
    """ 
    Use changepoints to correctly identify time spent in each zone
    
    changes : np.array of changepoint times (miliseconds into experiment)
    times : insert changes in between 0 and 900000 for later calculation
    if start_zone (righthand side)
    else (lefthand side)
    """
    if len(changes):
        times = np.insert(np.array([0,window*60000]),1,changes)
        time_diff = times[1:] - times[:-1]
        if start_zone:
            return np.sum(time_diff[0::2])/900000
        else:
            return np.sum(time_diff[1::2])/900000
    else:
        return start_zone
    

def find_zonetime2(sign):
    """ 
    Use sign from changes function to calculate time spent in each zone
    """
    return len(sign[sign == 0])/len(sign)
    
def find_all_zonetime(signs,active_cols,conc = 20):
    """

    Parameters
    ----------
    df : pd.DataFrame
        dataframe of greensludge test at given concentration.
    fps : int
        fps of video or recording.
    active_cols : list
        active columns.
        
    Returns
    -------
    array of total activities.

    """
    
    #at conc 0 only 10 organisms
    if conc:
        zonetimes = np.zeros(20)
    else:
        zonetimes = np.zeros(10)
    
    #loop through indidivudals
    for i in range(1,len(zonetimes)+1):
        sign = signs[i-1]
        zonetime = find_zonetime2(sign)
        zonetimes[i-1] = zonetime
    
    return zonetimes
   
find_totalact = lambda df: np.sum(np.array(df))

def find_all_activity(df,fps,active_cols,side = None,conc = 20):
    """

    Parameters
    ----------
    df : pd.DataFrame
        dataframe of greensludge test at given concentration.
    fps : int
        fps of video or recording.
    active_cols : list
        active columns.
    side : str
        'G' for left side 'D' for right side or None for both

    Returns
    -------
    array of total activities.

    """
    
    #filter if only for one side
    if side == 'G':
        cols = [c for c in df.columns if 'G' in c]
    elif side == 'D':
        cols = [c for c in df.columns if 'D' in c]
    else:
        cols = df.columns
    
    #redefine side to use for active cols
    df = df[cols].copy()
    
    #at conc 0 only 10 organisms
    if conc:
        activity = np.zeros(20)
    else:
        activity = np.zeros(10)
    
    #loop through indidivudals
    for i in range(1,len(activity)+1):
        if "G_{}".format(i) not in active_cols:
            continue
        if side == None:
            cols = ["G_{}".format(i),"D_{}".format(i)]
        else:
            cols = ["{}_{}".format(side,i)]
        act = find_totalact(df[cols])
        act = act / fps #BUG : is it necessary to normalise?
        activity[i-1] = act
    
    return activity
        
        
    
def find_maxamp(serie):
    """
    find max amplitude in a series of non zero values
    take the 90th percentile (there could be anomalies)
    """
    try:
        return np.quantile(serie[serie > 0],0.9)
    except IndexError:
        return 0.0
    
def find_meanamp(serie):
    """ 
    Take the mean all values inside 95% 
    """
    if np.quantile(serie,0.98) > 0:
        return np.mean(serie[serie < np.quantile(serie,0.98)])
    else:
        return 0.0
    
def find_all_maxamp(df,fps,active_cols,side = 'G',conc = 20,window = 60):
    
    #at conc 0 only 10 organisms
    if conc:
        amplitudes = np.zeros(20)
    else:
        amplitudes = np.zeros(10)
        
    for i in range(1,len(amplitudes)+1):
        col = "{}_{}".format(side,i)
        amplitude = find_maxamp(df[col].iloc[window*fps:].values)
        amplitudes[i-1] = amplitude
        
    return amplitudes

def find_all_meanamp(df,fps,active_cols,side = 'G',conc = 20,window = 60):
    
    #at conc 0 only 10 organisms
    if conc:
        amplitudes = np.zeros(20)
    else:
        amplitudes = np.zeros(10)
        
    for i in range(1,len(amplitudes)+1):
        col = "{}_{}".format(side,i)
        amplitude = find_meanamp(df[col].iloc[window*fps:].values)
        amplitudes[i-1] = amplitude
        
    return amplitudes
    
def filter_signs(series:pd.Series,window = 5,fps = 3):
    
    """ Only keep zone changes if longer than window (minutes) """
    
    window = window*fps
    arr = series.copy().values
    current_state = arr[0]
    
    #loop through array to sliding window before end
    i = 0
    while i < len(arr)-window:
        if arr[i+1] == current_state:
            i+=1
        else:
            if np.sum(arr[i+1:i+window] == arr[i+1]) == window-1:
                current_state = arr[i+1]
                i+=(window-1)
            else:
                arr[i+1:i+window] = current_state
                i+=(window-1)
    return pd.Series(arr,index = series.index)

def find_changes(ser,window = 5,fps = 15):
    """ 
    Fps should be given for any replay data files
    Take rolling average;
    np where > 0 : 1,0
    Take shift 1 sum and check where != 0
    """
    window = window*fps
    data = ser.rolling(window).mean().dropna()
    signs = pd.Series(np.where(np.array(data) > 0,1,0), index = data.index)
    signs = filter_signs(signs)
    changes = pd.Series(np.array(signs)[1:] - np.array(signs)[:-1],index = signs.index[:-1])
    return changes[changes != 0],signs

def find_all_changes(df,fps,active_cols,window = 5,conc = 20):
    """
    Parameters
    ----------
    df : dataframe
        datafram containing all active columns.
    fps : int
        frames per second.
    window : int, optional
        moving average window in minutes. The default is 5.

    Returns
    -------
    changes: number of changes per vdt.
    """
    
    #at conc 0 only 10 vdt
    if conc:
        changes = np.zeros(20)
    else:
        changes = np.zeros(10)
        
    signs = []
    
    #loop through each organism and calculate number of changes
    for i in range(1,len(changes)+1):
        if "G_{}".format(i) not in active_cols: 
            continue
        cols = ["G_{}".format(i),"D_{}".format(i)]
        series = (df[cols[1]] - df[cols[0]])
        change,sign = find_changes(series,window = window,fps = fps)
        changes[i-1] = len(change)
        signs.append(sign)
        
    return changes,signs
    
def find_endzone(df):
    """ 
    from two column dataframe find final zone
    """
    column = df.columns
    
    #count nonzero
    series = df[column[1]] - df[column[0]]
    return 1*(series.sum()>=0)

def find_all_endzone(df, fps, active_cols,conc = 20,window = 300):
    
    #at conc 0 only 10 organisms
    if conc:
        end_zone = np.zeros(20)
    else:
        end_zone = np.zeros(10)
    
    #loop through indidivudals
    for i in range(1,len(end_zone)+1):
        if "G_{}".format(i) not in active_cols:
            continue
        cols = ["G_{}".format(i),"D_{}".format(i)]
        end = find_endzone(df[cols].iloc[window*fps:])
        end_zone[i-1] = end
        
    return end_zone

def find_activecols(df):
    """
    check for unused petri dishes or immobile worms
    """
    activecols = []
    for i in range(1,21):
        temp = df['G_{}'.format(i)] + df['D_{}'.format(i)]
        temp[temp <= 2] = 0
        if temp.value_counts()[0]/(len(df['G_1'])) < 0.95:
            activecols.append('G_{}'.format(i))
            activecols.append('D_{}'.format(i))
            
    return activecols


def find_starts(df,active_cols,all_start):
    
    #preallocate for start and end times
    start_times,end_times = np.zeros(20),np.zeros(20)
    
    for zone in range(1,21):
            
        #define zone area
        cols = ['G_{}'.format(zone),'D_{}'.format(zone)]
        
        #check if col active
        if cols[0] not in active_cols: continue
    
        #add start data to temp array for given col
        temp = df[cols]
        
        #find start of test for given column
        if zone == 1: start = all_start
        temp = temp.loc[start:].iloc[:81]
        end = temp[temp.max(axis=1) > LIMIT].index[-1]
        start_times[zone - 1] = start
        end_times[zone - 1] = end
        
        start_old = start
        start = end - 2000
        if start_old + 1000> start:
            start = start_old + 1000
            
    return start_times,end_times


def adjust_starts(df,start_times,active_cols,time = 10,fps=15):
    
    final_df = pd.DataFrame(index = np.linspace(0,time*60000,time*60*fps + 1,dtype = int),columns = active_cols)
    for i in range(20):
        if 'G_{}'.format(i+1) not in active_cols: continue
        cols = ['G_{}'.format(i+1),'D_{}'.format(i+1)]
        temp = df[cols]
        #print(start_times[i],':',temp.index[:5])
        temp = temp[temp.index > start_times[i]]
        if temp.shape[0] > time*60*fps + 1:
            temp = temp.iloc[:time*60*fps + 1]
        final_df[cols] = np.array(temp)
        
    #remove values above 1000 and 1s
    final_df[final_df > 1000] = 0
    final_df[final_df == 1] = 0
    
    return final_df

def get_auto_starts(df_agg,cutoff,fps,timestep):
    
    bout = 8*60*fps
    
    df = df_agg.copy()
    df[df < cutoff] = 0
    
    #BUG should be for col in active cols.....
    starts = np.zeros(20)
    for i in range(20):
        
        arr = df[i+1].values
        zero_indices = np.where(arr == 0)[0]
        
        for x in range(len(zero_indices) - bout):
            if zero_indices[x+bout] - zero_indices[x] == bout:
                starts[i] = x*timestep + 2000
                break
            
    return starts


def adjust_starts_old(df,end_times,active_cols):
    
    final_df = pd.DataFrame(index = np.linspace(0,900000,4501,dtype = int),columns = active_cols)
    for i in range(20):
        if 'G_{}'.format(i+1) not in active_cols: continue
        cols = ['G_{}'.format(i+1),'D_{}'.format(i+1)]
        temp = df[cols].loc[end_times[i]:].iloc[:4501]
        #temp = temp[temp.index < [end_times[i]+900250]].iloc[1:]
        #temp.index = temp.index - temp.index[0]
        final_df[cols] = np.array(temp)
        
    #remove values above 1000 and 1s
    final_df[final_df > 1000] = 0
    final_df[final_df == 1] = 0
    
    return final_df

def plotgraphs(df,active_cols,title = 'No known concentration'):
    
    fig,ax = plt.subplots(4,5,figsize = (19.2,10.8),sharex = True,sharey = True)
    for i in range(20):
        if 'G_{}'.format(i+1) not in active_cols: continue
        row,col = i//5,i%5
        ax[row,col].plot(-df['G_{}'.format(i+1)],color = 'r')
        ax[row,col].plot(df['D_{}'.format(i+1)],color = 'b')
        
    fig.suptitle(title)
    
    return fig,ax

def testscores(df,numvdt,active_cols,start_zones):
    
    totalact = np.zeros(numvdt)
    changes = np.zeros(numvdt)
    finalzone = np.zeros(numvdt)
    prefzone = np.zeros(numvdt)
    zonetime = np.zeros(numvdt)
    maxampG = np.zeros(numvdt)
    maxampD = np.zeros(numvdt)
    meanampG = np.zeros(numvdt)
    meanampD = np.zeros(numvdt)
    
    #dictionary to return
    scores = {}
    vdt_n = 0
    
    for i in range(1,21):
        
        if 'G_{}'.format(i) not in active_cols: continue
    
        #select data for each worm
        start_zone = start_zones[i-1]
        cols = ['G_{}'.format(i),'D_{}'.format(i)]
        temp = df[cols]
        
        #changes calculation - put into function
        series = (temp[cols[1]] - temp[cols[0]])
        change = find_changes(series)
        changes[vdt_n] = len(change)
        
        #total activity
        totalact[vdt_n] = find_totalact(temp.iloc[150:])
        
        #preference zone
        prefzone[vdt_n] = find_prefzone(temp.iloc[1000:])
        
        #final zone calc - take last 5 minutes and train machine learning model on it?
        finalzone[vdt_n] = find_endzone(temp.iloc[3500:])
        
        #zone time - 0 means all time left. 1 means all time on right - could be better from 3 mins onwards
        zonetime[vdt_n] = find_zonetime(np.array(change.index),start_zone)
        
        #put all these into a class
        maxampG[vdt_n] = find_maxamp(np.array(temp[cols[0]]))
        maxampD[vdt_n] = find_maxamp(np.array(temp[cols[1]]))
        
        #remove extreme values from this (values that have high influence on the mean - like cooks distance)
        meanampG[vdt_n] = find_meanamp(np.array(temp[cols[0]]))
        meanampD[vdt_n] = find_meanamp(np.array(temp[cols[1]]))
        
        vdt_n+=1
        
    
    #prefzone = np.where(prefzone > 0, 'D','G')
    #finalzone = np.where(finalzone > 0, 'D','G')
    
    scores.update({
        'totalact':totalact,
        'prefzone':prefzone,
        'finalzone':finalzone,
        'zonetime':zonetime,
        'changes':changes,
        'maxampG':maxampG,
        'maxampD':maxampD,
        'meanampG':meanampG,
        'meanampD':meanampD
        })
    
    return scores

def write_results(data,s,d1,d2,c,res_dir = None):
    """
    data : dictionary
        Dictionary of scores for given c.
    s : str
        SITE - 1-PB 2-F.
    d1 : str
        date of prélèvement
    d2 : str
        date of test
    c : int
        Concentration of boue

    Returns
    -------
    None.

    """
    if res_dir:
        res = res_dir
    else:
        res = r'D:\VP_vdt\boue\Results\Boues_results.csv'
    for key in data:
        
        arr = np.empty(20)
        arr[:] = np.nan
        arr[:len(data[key])] = data[key]
        
        line = [s,d1,d2,c,key]
        line.extend(arr)
        line = [str(i) for i in line]
        
        with open(res,'r',newline = '') as file:
            existingLines = [line for line in csv.reader(file, delimiter=',')]
            file.close()
        
        if line[:5] not in [x[:5] for x in existingLines]:
            with open(res,'a',newline = '') as file:
                w = csv.writer(file)
                w.writerow(line)
                file.close()
        # elif line not in existingLines:
        # BUG replace entire line if values have changed...    

def create_csv_file(file_path):
    # Check if the file already exists
    if not os.path.exists(file_path):
        # Create the CSV file and write the header
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            header = ['Site','Date','Date_test','Concentration','Measure'] + [str(i) for i in range(1, 21)]
            writer.writerow(header)
        print(f"CSV file '{file_path}' created successfully.")
    else:
        print(f"CSV file '{file_path}' already exists.")

def write_res(scores,site,date1,date2,results_file):
    
    #check if results file already exists
    create_csv_file(results_file)
    
    #read existing lines of file
    with open(results_file,'r',newline = '') as file:
        existingLines = [line for line in csv.reader(file, delimiter=',')]
        file.close()
    
    for conc in scores:
        
        #concentration scores dictionary
        scores_conc = scores[conc]
        for measure in scores_conc:
            
            #preallocate and write results
            arr = np.empty(20)
            arr[:] = np.nan
            arr[:len(scores_conc[measure])] = scores_conc[measure]
            
            #add array to a line of values for results dir
            line = [site,date1,date2,conc,measure]
            line.extend(arr)
            line = [str(i) for i in line]
            
            #check if line already in file, if not write to file in append mode
            if line[:5] not in [x[:5] for x in existingLines]:
                with open(results_file,'a',newline = '') as file:
                    w = csv.writer(file)
                    w.writerow(line)
                    file.close()
            

def write(scores,site,date1,date2,res_file):
    
    for conc in scores:
        write_results(scores[conc],site,date1,date2,conc,res_file)

def write_old(scores,site,root):
    date1 = root.split('\\')[-1].split()[-1].replace('.','/')
    date2 = root.split('\\')[4].replace('.','/')
    if site == 1:
        s = 'PB'
    elif site == 2:
        s = 'F'
    for conc in scores:
        write_results(scores[conc],s,date1,date2,conc)
        
def savefig(fig,name,direc,conc = None):
    root = os.getcwd()
    os.chdir(direc)
    if conc:
        fig.savefig('{}_{}.jpg'.format(conc,name))
    else:
        fig.savefig('{}.jpg'.format(name))
    os.chdir(root)
    
def single_frame(df, measure):
    # return df with one column conc. one column measure
    data = pd.DataFrame(columns=["Concentration", measure])
    temp = df[df["Measure"] == measure].drop(columns=["Date_test", "Measure","Site","Date"])
    for i in temp["Concentration"]:
        tempData = pd.DataFrame(columns=["Concentration", measure])
        tempData[measure] = [
            *np.array(
                temp[temp["Concentration"] == i]
                .drop(columns="Concentration")
                .dropna(axis=1)
            )[0]
        ]
        tempData["Concentration"] = i
        data = pd.concat([data, tempData], ignore_index=True)
    return data.set_index('Concentration')
    