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
        scratchObject.scratch.depth = convolve(scratchObject.scratch.depth, ones(5,)/5, mode='same')
        
        #computing max dephts
        sum1 = sum1 + scratchObject.maxDepthOfTopo2()
        maxList.append(scratchObject.maxDepthOfTopo2())
    avgMaxDepth.append(sum1/len(scratchList))
    maxDepth.append(maxList)



print('\nśrednie dla każdej próbki:')  
print(avgMaxDepth)

print('\ndla każdej próbki, dla każdego zarysowania')
print(array(maxDepth))

for i in range(0,4):
    flag = 0
    for scratchObject in sampleList[i]:
        if flag == 0:
            flag = 1
            pyplot.plot( scratchObject.scratch.distance, scratchObject.scratch.depth,  colorList[i], label=labelList[i])
        else:
            pyplot.plot( scratchObject.scratch.distance, scratchObject.scratch.depth,  colorList[i])
pyplot.legend(loc='upper left')
pyplot.xlim(0,500)
pyplot.ylabel("depth [nm]")
pyplot.xlabel("distance [um]")
pyplot.show()




#sampleList - list of all the samples, contains scratchList elements
#scratchList - list of all the experiments on the sample
#scratchObject - experiment, consist of 3 Pass elements topo1, scratch and topo2
#pass - each pass element consist of 6 arrays(vectors): distance, depth, load, friction, acuEmiss, fricCoeff[]

#sampleList[0][1].scratch.depth - vector of depth signal of scratch pass of second ([1]) scratch of first ([0]) sample



    
        