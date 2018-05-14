from Pass import *
from scipy.interpolate import interp1d
from copy import copy, deepcopy

class Scratch:
    def __init__(self,sScratch):
        strListPass = sScratch.split("\n\n")
        self.topo1 = Pass(strListPass[0])
        self.scratch = Pass(strListPass[1])
        self.topo2 = Pass(strListPass[2])
        self.__equalLength()
        
    def addBaseline(self):
        self.scratch.depth = self.scratch.depth - self.topo1.depth
        self.topo2.depth = self.topo2.depth - self.topo1.depth
        self.topo1.depth = self.topo1.depth - self.topo1.depth
    
    # this method is for the case that one of the topographys or scratch is of different number of samples than the others, it interpolates the shorter one to correct this   
    def __equalLength(self):
        if (len(self.topo1.depth) < len(self.scratch.depth)):
            self.topo1.distance[0] = 0
            self.topo1.distance[-1] = 501
            fDepth = interp1d(self.topo1.distance, self.topo1.depth, kind = 'cubic')
            fLoad = interp1d(self.topo1.distance, self.topo1.load, kind = 'linear')
            fFriction = interp1d(self.topo1.distance, self.topo1.friction, kind = 'cubic')
            fAcuEmiss = interp1d(self.topo1.distance, self.topo1.acuEmiss, kind = 'cubic')
            fFricCoeff = interp1d(self.topo1.distance, self.topo1.fricCoeff, kind = 'cubic')
            self.topo1.distance = copy(self.scratch.distance)
            self.topo1.depth = fDepth(self.scratch.distance)
            self.topo1.load = fLoad(self.topo1.distance)
            self.topo1.friction = fFriction(self.topo1.distance)
            self.topo1.acuEmiss = fAcuEmiss(self.topo1.distance)
            self.topo1.fricCoeff = fFricCoeff(self.topo1.distance)
        if (len(self.topo2.depth) < len(self.scratch.depth)):
            self.topo2.distance[0] = 0
            self.topo2.distance[-1] = 502
            fDepth = interp1d(self.topo2.distance, self.topo2.depth, kind = 'cubic')
            fLoad = interp1d(self.topo2.distance, self.topo2.load, kind = 'linear')
            fFriction = interp1d(self.topo2.distance, self.topo2.friction, kind = 'cubic')
            fAcuEmiss = interp1d(self.topo2.distance, self.topo2.acuEmiss, kind = 'cubic')
            fFricCoeff = interp1d(self.topo2.distance, self.topo2.fricCoeff, kind = 'cubic')
            self.topo2.distance = copy(self.scratch.distance)
            self.topo2load = fLoad(self.topo2.distance)
            self.topo2.depth = fDepth(self.topo2.distance)
            self.topo2.friction = fFriction(self.topo2.distance)
            self.topo2.acuEmiss = fAcuEmiss(self.topo2.distance)
            self.topo2.fricCoeff = fFricCoeff(self.topo2.distance)
            
    def maxDepthOfTopo2(self):
        return max(self.topo2.depth)
        
        
        
    

    