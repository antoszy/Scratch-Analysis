from typing import List

from numpy import *
from copy import copy, deepcopy
import pandas as pd
import numpy as np

INDENTER_RADIUS = 5000 #nm
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
            self.fric_coeff = self.friction / self.load
        elif type(sPass) is Wear:
            self = deepcopy(sPass)

    def process_depth_and_friction(self):
        s = pd.Series(self.depth)
        self.depth_max = s.rolling(20, min_periods=1).max().rolling(40, min_periods=1).mean().values
        self.depth_min = s.rolling(20, min_periods=1).min().rolling(40, min_periods=1).mean().values
        self.friction_abs = np.abs(self.friction)
        self._calculate_friction_from_peak2peak()
        self._calculate_friction_as_abs_min()

    def calculate_wear_area(self):
        self.xsection_radius = np.sqrt(INDENTER_RADIUS**2 - (INDENTER_RADIUS - self.depth_max)**2 )
        self.wear_width = 2 * self.xsection_radius
        self.delta_depth = np.insert(self.depth_max[1:] - self.depth_max[:-1], 0, 0)
        self.delta_area = self.delta_depth * self.wear_width
        self.wear_area = np.cumsum(self.delta_area) / 10**6
        # self.xsection_radius_min = np.sqrt(INDENTER_RADIUS**2 - (INDENTER_RADIUS - self.depth_min)**2 )
        self.xsection_radius_min = np.sqrt(INDENTER_RADIUS**2 - (INDENTER_RADIUS - np.max(self.depth_min, 0))**2 )
        self.wear_width_min = 2 * self.xsection_radius
        self.delta_depth_min = np.insert(self.depth_min[1:] - self.depth_min[:-1], 0, 0)
        self.delta_area_min = self.delta_depth_min * self.wear_width_min
        self.wear_area_min = np.cumsum(self.delta_area_min) / 10**6

    def _calculate_friction_from_peak2peak(self):
        friction_series = pd.Series(self.friction)
        friction_max = friction_series.rolling(40, min_periods=1).max()
        friction_min = friction_series.rolling(40, min_periods=1).min()
        self.friction_peak = ((friction_max - friction_min) / 2).values
        fric_coeff_series = pd.Series(self.friction)
        fric_coeff_max = fric_coeff_series.rolling(40, min_periods=1).max()
        fric_coeff_min = fric_coeff_series.rolling(40, min_periods=1).min()
        self.fric_coeff_peak = ((fric_coeff_max - fric_coeff_min) / 2).values

    def _calculate_friction_as_abs_min(self):
        friction_abs_series = pd.Series(self.friction_abs)
        self.friction_abs_min = friction_abs_series.rolling(100, min_periods=1).min()


    def truncate(self, start_ind, stop_ind):
        self.time = self.time[start_ind:stop_ind]
        self.load = self.load[start_ind:stop_ind]
        self.depth = self.depth[start_ind:stop_ind]
        self.friction = self.friction[start_ind:stop_ind]
        self.depth_max = self.depth_max[start_ind:stop_ind]
        self.depth_min = self.depth_min[start_ind:stop_ind]
        self.friction_abs = self.friction_abs[start_ind:stop_ind]
        self.friction_peak = self.friction_peak[start_ind:stop_ind]
        self.fric_coeff = self.fric_coeff[start_ind:stop_ind]
        self.fric_coeff_peak = self.fric_coeff_peak[start_ind:stop_ind]
        self.friction_abs_min = self.friction_abs_min[start_ind:stop_ind]

    def trim_to_time(self, trim_time=6000):
        end_index = np.argmax(self.time >= trim_time)
        self.truncate(0, end_index)

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
        #print(slope_factor*self.time[12000])


def average_time_series(time_series_list: List[np.array]):
    return np.mean(np.array(time_series_list), axis=0)


def mix_wears(wear_list: List[Wear]):
    wear_mix = Wear(wear_list[0])
    samples_number = np.min([len(wear.depth) for wear in wear_list])
    wear_attributes = ["depth", "time", "load", "friction", "fric_coeff"]
    for wear_attribute in wear_attributes:
        time_series_list = [getattr(wear, wear_attribute)[0:samples_number] for wear in wear_list]
        setattr(wear_mix, wear_attribute, average_time_series(time_series_list))
    return wear_mix

