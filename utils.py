from Scratch import *
from Pass import *
from Wear import *
import colorsys


def read_data(filePath):
    scratch_list = []
    file = open(filePath)
    try:
        sFile = file.read()
    finally:
        file.close()
    
    strList = sFile.split("\n\n\n")
    
    for strScratch in strList:
        scratch_list.append(Scratch(strScratch))
    return scratch_list


def read_wear_data(filePath):
    wearList = []
    file = open(filePath)
    try:
        sFile = file.read()
    finally:
        file.close()
    
    strList = sFile.split("\n\n")
    
    for swear in strList:
        wearList.append(Wear(swear))
        
    return wearList 

    
def read_pass_data(filePath):
    with open(filePath) as file:
        strData = file.read() 
        pas = Pass(strData)
        return pas


def plot_scratch_sample(ax, sample, title, toPlot='d', base='distance'):
    for scratch in sample:
        scratch.addBaseline()
        # scratch.truncate(truncate)
        scratch.topo2.depth = scratch.topo2.depth - scratch.topo2.depth[20]

        if base == 'distance':
            xVar = scratch.scratch.distance
            xLabel = 'Dystans [μm]'
        elif base == 'load':
            xVar = scratch.scratch.load
            xLabel = 'Obciążenie [mN]'
        else:
            raise NotImplementedError()
        
        if toPlot == 'd':
            yVar = scratch.topo2.depth
            yLabel = "Głębokość zarysowania [nm]"
            title = "Głębokość zarysowania (pomiar wykonany po przeprowadzeniu testu zarysowania)"
        elif toPlot == 'f':
            yVar = scratch.scratch.friction
            yLabel = "Siła tarcia [mN]"
            title = "Zmiany siły tarcia na długości zarysowania"
        elif toPlot == 'tf':
            yVar = scratch.topo1.friction
            yLabel = "Siła tarcia [mN]"
            title = ""
        elif toPlot == 'sd':
            yVar = scratch.scratch.depth
            yLabel = "Głębokość [nm]"
            title = ""
        elif toPlot == 'ae':
            yVar = scratch.scratch.acuEmiss
            yLabel = "Emisja akustyczna [mV]"
            title = ""
        elif toPlot == 'fc':
            yVar = scratch.scratch.fricCoeff
            yLabel = "Współczynnik tarcia"
            title = "Zależność współczynnika tarcia dynamicznego od obciążenia wgłębnika"
        elif toPlot == 'l':
            yVar = scratch.scratch.load
            yLabel = "Obciążenie wgłębnika [mN]"
            title = "Zmiany obciążenia wgłębnika na długości zarysowania"
        else:
            raise NotImplementedError

        ax.plot(xVar, yVar)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_title(title)
    #ax.legend(loc='upper left')


def preprocess_samples(sampleList, truncate=-1):
    for i, sample in enumerate(sampleList):
        for scratch in sample:
            scratch.addBaseline()
            scratch.truncate(truncate)
            scratch.topo2.depth = scratch.topo2.depth - scratch.topo2.depth[20]
            scratch.scratch.friction -= scratch.topo1.friction
            scratch.scratch.fricCoeff = scratch.scratch.friction / scratch.scratch.load


def plot_scratch_samples(ax, sampleList, nameList, toPlot='d', base='distance', legend="upper left"):
    meanScratches = []
    num = len(sampleList)
    for i, sample in enumerate(sampleList):
        meanScratches.append(Scratch.meanScratchList(sample))
        # col = create_color(i, num, hue=0.1)
        col = create_color_hue(i, num)
        label = nameList[i][ nameList[i].rfind("/")+1: ]
        # label = nameList[i][ nameList[i].rfind("\\")+1: ]

        if base == 'distance':
            xVar = meanScratches[-1].scratch.distance
            xLabel = 'Dystans [μm]'
        elif base == 'load':
            xVar = meanScratches[-1].scratch.load
            xLabel = 'Obciążenie [mN]'
        else:
            raise NotImplementedError()
        
        if toPlot == 'd':
            yVar = meanScratches[-1].topo2.depth
            yLabel = "Głębokość zarysowania [nm]"
            title = "Głębokość zarysowania (pomiar wykonany po przeprowadzeniu testu zarysowania)"
        elif toPlot == 'f':
            yVar = meanScratches[-1].scratch.friction
            yLabel = "Siła tarcia [mN]"
            title = "Zależność siły tarcia od obciążenia wgłębnika"
        elif toPlot == 'tf':
            yVar = meanScratches[-1].topo1.friction
            yLabel = "Siła tarcia [mN]"
            title = ""
        elif toPlot == 'sd':
            yVar = meanScratches[-1].scratch.depth
            yLabel = "Głębokość [nm]"
            title = ""
        elif toPlot == 'ae':
            yVar = meanScratches[-1].scratch.acuEmiss
            yLabel = "Emisja akustyczna [mV]"
            title = ""
        elif toPlot == 'fc':
            yVar = meanScratches[-1].scratch.fricCoeff
            yLabel = "Współczynnik tarcia"
            title = "Zależność współczynnika tarcia dynamicznego od obciążenia wgłębnika"
        elif toPlot == 'l':
            yVar = meanScratches[-1].scratch.load
            yLabel = "Obciążenie wgłębnika [mN]"
            title = "Zmiany obciążenia wgłębnika na długości zarysowania"
        else:
            raise NotImplementedError
                
        ax.plot(xVar, yVar, label=label, color=col, linestyle=create_linestyle(i))
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_title(title)
        i = i + 1
    if legend:
        ax.legend(loc=legend)
    
def plot_wear_samples(ax, sampleList, nameList, color = 0.9, color_offset=0, xaxis = "time", yaxis="min"):
    meanWear = []
    num = len(sampleList)
    i = 0
    for ind, sample in enumerate(sampleList):
        for wear in sample:
            col = create_color(ind+color_offset, num+color_offset, hue=color)
            if yaxis == "min":
                ydata = wear.depth_min
            else:
                ydata = wear.depth_max
            if (xaxis == "time"):
                ax.plot(wear.time, ydata, label=nameList[ind], color=col)
            else:
                ax.plot(ydata, label=nameList[ind], color=col)
            #ax.legend(loc='upper left')


def plot_mean_wear_samples(ax, sampleList, nameList, color = 0.9, color_offset=0, xaxis="time", yaxis="min"):
    meanWear = []
    num = len(sampleList)
    i = 0
    for ind,wear in enumerate(sampleList):
        col = create_color(ind+color_offset, num+color_offset, hue=color)
        if yaxis == "min":
            ydata = wear.depth_min
        else:
            ydata = wear.depth_max
        if (xaxis == "time"):
            ax.plot(wear.time, ydata, label=nameList[ind], color = col)
        else:
            ax.plot(ydata, label=nameList[ind], color = col)
        ax.legend(loc='upper left')


def create_color(index, maxindex, hue = 0.9):
    if (index < maxindex/2):
        s = 1 
        v = index / (maxindex/2)
    else:
        s = 2 - index / (maxindex/2)
        v = 1
    return colorsys.hsv_to_rgb(hue, s, v)


def create_color_hue(index, maxindex):
    step = 1 / maxindex
    s = 1
    v = 0.8
    hue = index * step
    return colorsys.hsv_to_rgb(hue, s, v)


def create_linestyle(index):
    LINESTYLES = ['solid', 'dashed', 'dotted']
    return LINESTYLES[index % 2]


def plot_scratch_individual(ax, scratchList, toPlot='depth', truncate=-1):
    num = len(scratchList)
    for i,scratch in enumerate(scratchList):
        scratch.addBaseline()
        scratch.truncate(truncate)
        scratch.topo2.depth = scratch.topo2.depth - scratch.topo2.depth[20]
        col = create_color(i, num)
        label = "scratch: " + str(i)
        ax.plot( scratch.topo2.distance, scratch.topo2.depth, label=label, color = col) 
    ax.legend(loc='upper left')

