from numpy import *
from copy import copy, deepcopy

class Pass:
    
    def __init__(self, sPass= None):
        distance = []
        depth = []
        load = []
        friction = []
        acuEmiss = []
        fricCoeff = []
        if type(sPass) is str:
            liStrPass = sPass.split("\n")
            for strLine in liStrPass:
                strListLine = strLine.split()
                if len(strListLine)==6:
                    distance.append(float(strListLine[0]))
                    depth.append(float(strListLine[1]))
                    load.append(float(strListLine[2]))
                    friction.append(float(strListLine[3]))
                    acuEmiss.append(float(strListLine[4]))
                    fricCoeff.append(float(strListLine[5]))
            #print(str(len(distance)) +' '+ str(len(depth)) )
            self.distance = array(distance)
            self.depth = array(depth)
            self.load = array(load)
            self.friction = array(friction)
            self.acuEmiss = array(acuEmiss)
            self.fricCoeff = array(fricCoeff)
        elif type(sPass) is Pass:
            self = deepcopy(sPass)
        

        