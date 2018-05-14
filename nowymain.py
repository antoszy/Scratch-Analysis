from matplotlib import pyplot
from read_data import *
from Scratch import *
from numpy import *

scratchList = read_data("C:\\Users\\Michał\\Desktop\\Aleksander\\Scratch\\cer biala\\wynik-ce-bi.txt")
scratchList1 = read_data("C:\\Users\\Michał\\Desktop\\Aleksander\\Scratch\\cer czarna\\wynik-ce-cz.txt")
scratchList2 = read_data("C:\\Users\\Michał\\Desktop\\Aleksander\\Scratch\\alu cylinder\\wynik-al-cy.txt")
scratchList3 = read_data("C:\\Users\\Michał\\Desktop\\Aleksander\\Scratch\\alu gwint\\wynik-al-gw.txt")


# sampleList = [scratchList, scratchList1]
# sampleList = [scratchList2, scratchList3]
sampleList = [scratchList, scratchList1, scratchList2, scratchList3]
labelList = [ 'white coating', 'black coating', '5056 aluminium', '7075 aluminium']
colorList = [ 'red', 'black', 'blue', 'green']
avgMaxDepth = []
maxDepth = []


#for each sample
for scratchList in sampleList:
    sum1 = 0
    maxList = []
    #for each scratch
    for scratchObject in scratchList:
        #adding base line
        scratchObject.addBaseline()
        
        #moving average for depth for topography 2 (after scratch)
        scratchObject.topo2.depth = convolve(scratchObject.topo2.depth, ones(5,)/5, mode='same')
        
        #computing max dephts
        sum1 = sum1 + scratchObject.maxDepthOfTopo2()
        maxList.append(scratchObject.maxDepthOfTopo2())
    avgMaxDepth.append(sum1/len(scratchList))
    maxDepth.append(maxList)



print('\nśrednie dla każdej próbki:')  
print(avgMaxDepth)

print('\ndla każdej próbki, dla każdego zarysowania')
print(array(maxDepth))

## all scratches
# for i in range(2,4):
#     flag = 0
#     for scratchObject in sampleList[i]:
#         if flag == 0:
#             flag = 1
#             pyplot.plot( scratchObject.topo2.distance, scratchObject.topo2.depth,  colorList[i], label=labelList[i])
#         else:
#             pyplot.plot( scratchObject.topo2.distance, scratchObject.topo2.depth,  colorList[i])
# pyplot.legend(loc='upper left')
# pyplot.xlim(0,500)
# pyplot.ylabel("depth [nm]")
# pyplot.xlabel("distance [um]")
# pyplot.show()

## mean scratch depth of each sample
# meanScratchList = []
# for scratchList in sampleList:
#     meanScratchList.append( scratchList[0].meanScratch( [scratchList[1], scratchList[2]]))
#     
# for i in range(0,2):
#     pyplot.plot( meanScratchList[i].topo2.distance ,meanScratchList[i].topo2.depth,  colorList[i], label=labelList[i])
# pyplot.legend(loc='upper left')
# pyplot.xlim(0,500)
# pyplot.ylabel("depth [nm]")
# pyplot.xlabel("distance [um]")
# pyplot.show()

## mean scratch fric coef of each sample
meanScratchList = []
for scratchList in sampleList:
    meanScratchList.append( scratchList[0].meanScratch( [scratchList[1], scratchList[2]]))
    
for i in range(2,4):
    pyplot.plot( meanScratchList[i].scratch.distance ,meanScratchList[i].scratch.fricCoeff,  colorList[i], label=labelList[i])
pyplot.legend(loc='upper left')
pyplot.xlim(25,500)
pyplot.ylim(0,0.8)
pyplot.ylabel("depth [nm]")
pyplot.xlabel("distance [um]")
pyplot.show()

##

#sampleList - list of all the samples, contains scratchList elements
#scratchList - list of all the experiments on the sample
#scratchObject - experiment, consist of 3 Pass elements topo1, scratch and topo2
#pass - each pass element consist of 6 arrays(vectors): distance, depth, load, friction, acuEmiss, fricCoeff[]

#sampleList[0][1].scratch.depth - vector of depth signal of scratch pass of second ([1]) scratch of first ([0]) sample



    
        