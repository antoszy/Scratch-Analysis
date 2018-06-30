from Pass import *
from scipy.interpolate import interp1d
from copy import copy, deepcopy
import numpy as np

class Scratch:
    def __init__(self,sScratch):
        if type(sScratch) is str:
            strListPass = sScratch.split("\n\n")
            self.topo1 = Pass(strListPass[0])
            self.scratch = Pass(strListPass[1])
            self.topo2 = Pass(strListPass[2])
            self.__equalLength()
        else:
            raise NameError('no such constructor')
        
    def meanScratch(self, scratchList):
        #mean depth from topo2 and mean fricCoeff from scratch  self and scratches from scratchList
        meanScr = deepcopy(self)
        print(meanScr.topo2)
        for scratch in scratchList:
            meanScr.topo2.depth = meanScr.topo2.depth + scratch.topo2.depth
            meanScr.scratch.fricCoeff = meanScr.scratch.fricCoeff + scratch.scratch.fricCoeff
        meanScr.topo2.depth = meanScr.topo2.depth/(len(scratchList)+1)
        meanScr.scratch.fricCoeff = meanScr.scratch.fricCoeff/(len(scratchList)+1)
        return meanScr
        
    @staticmethod
    def meanScratchList( scratchList):
        #mean depth from topo2 and mean fricCoeff from scratch  self and scratches from scratchList
        desLen = len(scratchList[0].topo1.distance)
        for scratch in scratchList[1:]:
            desLen = min(desLen, len(scratch.topo1.distance))
        meanScr = deepcopy(scratchList[0])
        meanScr.truncate(desLen)
        for scratch in scratchList[1:]:
            scratch.truncate(desLen)
            meanScr.topo2.depth = meanScr.topo2.depth + scratch.topo2.depth
            meanScr.scratch.fricCoeff = meanScr.scratch.fricCoeff + scratch.scratch.fricCoeff
        meanScr.topo2.depth = meanScr.topo2.depth/(len(scratchList))
        meanScr.scratch.fricCoeff = meanScr.scratch.fricCoeff/(len(scratchList))
        return meanScr

    def truncate(self, desLen):
        for pas in [ self.topo1, self.scratch, self.topo2 ]:
            pas.distance = pas.distance[:desLen]
            pas.load = pas.load[:desLen]
            pas.depth = pas.depth[:desLen]
            pas.friction = pas.friction[:desLen]
            pas.acuEmiss = pas.acuEmiss[:desLen]
            pas.fricCoeff = pas.fricCoeff[:desLen]


    def addBaseline(self):
        self.scratch.depth = self.scratch.depth - self.topo1.depth
        self.topo2.depth = self.topo2.depth - self.topo1.depth
        self.topo1.depth = self.topo1.depth - self.topo1.depth
    
    # this method is for the case that one of the topographys or scratch is of different number of samples than the others, it interpolates the shorter one to correct this   
    def __equalLength(self):
        desLen = min( len(self.topo1.distance), len(self.scratch.distance), len(self.topo2.distance) )
        self.truncate(desLen)

    def maxDepthOfTopo2(self):
        return max(self.topo2.depth)
        
    def meanFrictCoeffOfScratch(self):
        return mean(self.scratch.fricCoeff[15:])
        
        
        
    

    
