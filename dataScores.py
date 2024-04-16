# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:18:44 2024

Class with scores from vdt results class

@author: George
"""

import os
import numpy as np
import pandas as pd

class Scores:
    
    def __init__(self,sludgeClass):
        
        self.data = sludgeClass.data_
        self.concs = sludgeClass.concs
        self.fps = sludgeClass.fps
        self.active_cols = sludgeClass.active_cols
        self.initialise()
        self.get_scores()
        
    def initialise(self):
        
        #activity normalised by fps for each zone and combined zones
        self.activity = {i: [] for i in self.concs}
        self.activity_left = {i: [] for i in self.concs}
        self.activity_right = {i: [] for i in self.concs}
        
        #max activities
        self.maxampG = {i: [] for i in self.concs}
        self.maxampD = {i: [] for i in self.concs}
        
        #mean activities
        self.meanampG = {i: [] for i in self.concs}
        self.meanampD = {i: [] for i in self.concs}
        
        
        # start_zones = {i: [] for i in self.concs}
        
        
        #other scores
        self.changes = {i: [] for i in self.concs}
        self.pref_zone = {i: [] for i in self.concs}
        self.end_zone = {i: [] for i in self.concs}
        self.zonetime = {i: [] for i in self.concs}
        
    def get_scores():
        
        self.get_activity()
        self.get_amplitudes()
        
        self.get_changes()
        self.get_zones()
        self.get_zonetime()
        
    def get_activity():
        """
        

        Returns
        -------
        None.

        """
        self.activity = None
        self.activity_left = None
        self.activity_right = None
        
    def get_amplitudes():
        """
        

        Returns
        -------
        None.

        """
        self.maxampG = None
        self.maxampD = None
        self.meanampG = None
        self.meanampD = None
        
    def get_changes():
        """
        

        Returns
        -------
        None.

        """
        self.changetimes = None
        self.changes = None
        
    def get_zones():
        """
        

        Returns
        -------
        None.

        """
        self.prefzone = None
        self.endzone = None
        self.zonetime = None