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
    activity = {i: [] for i in data.concs}
    activity_left = {i: [] for i in data.concs}
    activity_right = {i: [] for i in data.concs}
    pref_zone = {i: [] for i in data.concs}
    end_zone = {i: [] for i in data.concs}
    zonetime = {i: [] for i in data.concs}

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
        changes[conc] = vdt.find_all_changes(data.data_[conc], data.fps, data.active_cols[conc], conc = conc)
        
        #total activity measures (and left and right)
        activity[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], conc = conc)
        activity_left[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], side = 'G', conc = conc)
        activity_right[conc] = vdt.find_all_activity(data.data_[conc], data.fps, data.active_cols[conc], side = 'D', conc = conc)
        
        #prevalent zone
        pref_zone[conc] = vdt.find_all_prefzone(data.data_[conc], data.fps, data.active_cols[conc])
        
        #finalzone
        end_zone[conc] = vdt.find_all_endzone(data.data_[conc], data.fps, data.active_cols[conc])
        
        #zonetime
        #zonetime[conc] = vdt.find_all_zonetime(data.data_[conc], data.fps, data.active_cols[conc])
        
        #max amps
        
        
        #mean amps (evaluate deleting value)
        
        
        #dataset_scores[conc] = vdt.testscores(df, 20, active_cols, start_zones[conc])
        
        
    # # %% save results
    # date1 = config_data["date_of_sample"]
    # date2 = config_data["date_of_test"]
    # vdt.write(
    #     dataset_scores,
    #     data.site,
    #     date1,
    #     date2,
    #     r"D:\VP_vdt\SYSEG - STEP Givors\Results\Boues_results.csv",
    # )

    # # %% Plot results
    # file = r"D:\VP_vdt\SYSEG - STEP Givors\Results\Boues_results.csv"
    # results = pd.read_csv(file)

    # def extract(df, date, site):
    #     return df[(df["Site"] == site) & (df["Date"] == date)].drop(
    #         columns=["Site", "Date"]
    #     )

    # def single_frame(df, measure):
    #     # return df with one column conc. one column measure
    #     data = pd.DataFrame(columns=["Concentration", measure])
    #     temp = df[df["Measure"] == measure].drop(columns=["Date_test", "Measure"])
    #     for i in temp["Concentration"]:
    #         tempData = pd.DataFrame(columns=["Concentration", measure])
    #         tempData[measure] = [
    #             *np.array(
    #                 temp[temp["Concentration"] == i]
    #                 .drop(columns="Concentration")
    #                 .dropna(axis=1)
    #             )[0]
    #         ]
    #         tempData["Concentration"] = i
    #         data = pd.concat([data, tempData], ignore_index=True)
    #     return data

    # measures = [
    #     "totalact",
    #     "zonetime",
    #     "changes",
    #     "meanampG",
    #     "meanampD",
    #     "maxampG",
    #     "maxampD",
    # ]
    # others = ["prefzone"]

    # temp = extract(results, date1, data.site)

    # for measure in measures:

    #     tempdf = single_frame(temp, measure)
    #     plt.figure()
    #     sns.boxplot(x="Concentration", y=measure, data=tempdf, color="r")

    # for other in others:

    #     tempdf = single_frame(temp, other)
    #     temp = (
    #         tempdf.groupby("Concentration").sum()
    #         / tempdf.groupby("Concentration").count()
    #     )
    #     plt.figure()
    #     sns.barplot(x=temp.index.values, y=temp[other].values, color="r")
