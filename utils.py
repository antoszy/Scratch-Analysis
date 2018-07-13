from Scratch import *
from Pass import *
import colorsys

def read_data(filePath):
    scratchList = []
    file = open(filePath)
    try:
        sFile = file.read()
    finally:
        file.close()
    
    strList = sFile.split("\n\n\n")
    
    for strScratch in strList:
        scratchList.append(Scratch(strScratch))
        
    #print( str(len(scratchList)) + " scratches imported")
    
    return scratchList


    
def read_pass_data(filePath):
    with open(filePath) as file:
        strData = file.read() 
        pas = Pass(strData)
        return pas


def plot_scratch_samples(ax, sampleList, nameList, truncate=-1):
    meanScratches = []
    num = len(sampleList)
    i = 0
    for sample in sampleList:
        for scratch in sample:
            scratch.addBaseline()
            scratch.truncate(truncate)
            scratch.topo2.depth = scratch.topo2.depth - scratch.topo2.depth[20]
        meanScratches.append(Scratch.meanScratchList(sample))
        col = create_color(i, num)
        label = nameList[i][ nameList[i].rfind("/")+1: ]
        label = nameList[i][ nameList[i].rfind("\\")+1: ]
        ax.plot( meanScratches[-1].topo2.distance, meanScratches[-1].topo2.depth, label=label, color = col)
        i = i + 1    
    ax.legend(loc='upper left')
    

def create_color(index, maxindex):
    h = 0.9
    if (index < maxindex/2):
        s = 1 
        v = index / (maxindex/2)
    else:
        s = 2 - index / (maxindex/2)
        v = 1
    #print ( [s,v])
    return colorsys.hsv_to_rgb(h,s,v)

def plot_scratch_individual(ax, scratchList, truncate=-1):
    num = len(scratchList)
    for idx,scratch in scratchList:
        scratch.addBaseline()
        scratch.truncate(truncate)
        scratch.topo2.depth = scratch.topo2.depth - scratch.topo2.depth[20]
        col = create_color(i, num)
        label = "scratch: " + str(idx)
        ax.plot( meanScratches[-1].topo2.distance, meanScratches[-1].topo2.depth, label=label, color = col) 





    
    
    
    
    
