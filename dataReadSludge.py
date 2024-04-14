# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 12:11:04 2024

dataread class for test: Green Sludge

@author: George
"""

import os
import numpy as np
import pandas as pd
import functions_vdt as vdt

"""
conf: json file containing info on events. copy and paster relevant config to working directory
"""


class SludgeClass:

    def __init__(self, conf):
        self.config = conf
        self.site = conf["client_name"]
        self.batch = conf["date_of_sample"]
        self.directory = conf["directory"]
        self.concs = [int(c) for c in [*conf["concentrations"]]]  # concentrations

        # add class data for each data file
        self.data = self.get_data()
        self.active_cols = self.get_active_cols()
        self.adjust_starts()
        self.remove_noise()

    def get_data(self):

        # go to config specific directory and extract relevant datafiles
        os.chdir(self.directory)

        # loop through concentrations anda add to data
        data = {}
        for conc in self.concs:

            # read relevant datafiles
            datafiles = self.config["concentrations"][str(conc)]["filename"]
            side = find_side(self.config["concentrations"][str(conc)]["side"])
            df = read_data(datafiles, side)

            data[conc] = df

        return data

    def get_active_cols(self):

        active_cols = {}
        for conc in self.concs:
            active_cols[conc] = vdt.find_activecols(self.data[conc])
            if conc == 0:
                active_cols[conc] = [
                    "G_1",
                    "D_1",
                    "G_2",
                    "D_2",
                    "G_3",
                    "D_3",
                    "G_4",
                    "D_4",
                    "G_5",
                    "D_5",
                    "G_6",
                    "D_6",
                    "G_7",
                    "D_7",
                    "G_8",
                    "D_8",
                    "G_9",
                    "D_9",
                    "G_10",
                    "D_10",
                ]

        return active_cols

    def adjust_starts(self):

        for conc in self.concs:
            starts = self.config["concentrations"][str(conc)]["starts"]
            if starts:
                starts = self.check_starts(starts) #convert to miliseconds if in mm.ss format
                max_end = self.data[conc].index[-1]  # max possible index
                # ends = [min(x,max_end) + (15*60*1000) for x in starts]
                self.data[conc] = vdt.adjust_starts(
                    self.data[conc], starts, self.active_cols[conc]
                )
            else:
                print("No Start Data!!")
                
    def check_starts(self,starts):
        
        """ Return milisecond integers if start format written in m.ss format """
        
        if starts[-1] < 25:
            for i,s in enumerate(starts):
                s = "{:.2f}".format(s)
                starts[i] = int(s.split('.')[0]) * 60000 + int(s.split('.')[-1]) * 1000
        return starts

    def remove_noise(self):

        threshold_value = 250
        for conc in self.concs:
            # BUG !! what if active vols missed one in the middle? (extract numbers)
            for i in range(len(self.active_cols[conc]) // 2):
                col = i + 1
                diffs = np.diff(
                    np.abs(self.data[conc]["G_{}".format(col)])
                    + np.abs(self.data[conc]["D_{}".format(col)])
                )
                indices_to_zero = np.where(diffs > threshold_value)[0]
                for ind in indices_to_zero:
                    # account for diff index shift -1
                    self.data[conc]["G_{}".format(col)].iloc[ind + 1] = 0
                    self.data[conc]["D_{}".format(col)].iloc[ind + 1] = 0


def convarea(string):
    multipliers = {"A": 0, "B": 1, "C": 2, "D": 3}
    return str(multipliers[string[0]] * 5 + int(string[1]))


def wrangle(df):
    df = df["abstime time type location area data1".split()][df.type == 101]
    df["data1"] = pd.to_numeric(df["data1"], downcast="integer")
    # df['plancher'] = df['location'].str[:-2] #REMOVE
    df["time"] = (df["time"] / 1000).astype(int)  # ms
    df["zone"] = (
        df["area"].str[-1] + "_" + df["area"].str.split("-").str[0].apply(convarea)
    )
    df = df.reset_index(drop=True)
    df = df[["time", "zone", "data1"]]
    return df.pivot_table(index="time", columns="zone", values="data1")


def read_data(files, side):
    """
    read all files and return df for raw data
    """
    df = pd.read_csv(files[0], sep="\t")
    for i in range(len(files) - 1):
        df = pd.concat([df, pd.read_csv(files[i + 1], sep="\t")], ignore_index=True)

    df = df[df["location"].str.contains(side)]
    return wrangle(df)


def find_side(string):
    left = ["left", "Left", "gauche", "Gauche"]
    right = ["right", "Right", "droite", "Droite", "droit", "Droit"]
    if string in left:
        return "Gauche"
    elif string in right:
        return "Droit"
    else:
        return None


#debug
if __name__ == "__main__":
    
    print('Script for debugging class')