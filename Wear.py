from numpy import *
from copy import copy, deepcopy
import pandas as pd
import numpy as np

class Wear:
    
    def __init__(self, sPass= None, correct_drift = True):
        time = []
        depth = []
        load = []
        friction = []
        if type(sPass) is str:
            liStrPass = sPass.split("\n")
            for strLine in liStrPass:
                stringsInLine = strLine.split()
                if (len(stringsInLine) == 4) :
                    time.append(float(stringsInLine[0]))
                    depth.append(float(stringsInLine[1]))
                    load.append(float(stringsInLine[2]))
                    friction.append(float(stringsInLine[3]))
            self.depth = array(depth)
            self.time = array(time)
            self.load = array(load)
            self.friction = array(friction)
            s = pd.Series(self.depth)
            self.depth_max = s.rolling(20, min_periods=1).max().rolling(40).mean().values
            self.depth_min = s.rolling(20, min_periods=1).min().rolling(40).mean().values
        elif type(sPass) is Wear:
            self = deepcopy(sPass)
            
    def truncate(self, start_ind, stop_ind):
        self.time = self.time[start_ind:stop_ind]
        self.load = self.load[start_ind:stop_ind]
        self.depth = self.depth[start_ind:stop_ind]
        self.friction = self.friction[start_ind:stop_ind]
        self.depth_max = self.depth_max[start_ind:stop_ind]
        self.depth_min = self.depth_min[start_ind:stop_ind]
        
    def correct_drift(self, drift_start, drift_stop):
        """ Function for correctig termal drift 

        drift_start - sample number where we start collecting drift data
        drift_stop - sample number where we stop collecting drift correction data """
        
        slope_factor = np.polyfit(self.time[drift_start:drift_stop],
                                  self.depth[drift_start:drift_stop],
                                  1)[0]
        self.depth = self.depth - slope_factor*self.time
        self.depth_max = self.depth_max - slope_factor*self.time
        self.depth_min = self.depth_min - slope_factor*self.time

        
