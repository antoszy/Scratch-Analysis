from matplotlib import pyplot
from read_data import *
from Scratch import *
from numpy import *

scratchList = read_data("C:\\Users\\ja\\Desktop\\Aleksander\\Scratch\\cer biala\\wynik-ce-bi.txt")
scratchList1 = read_data("C:\\Users\\ja\\Desktop\\Aleksander\\Scratch\\cer czarna\\wynik-ce-cz.txt")
# scratchList2 = read_data("I:\OneDrive\\doktorat\\praca doktorska\\badania\\scratch\\2\\krzywe.txt")
# scratchList3 = read_data("I:\OneDrive\\doktorat\\praca doktorska\\badania\\scratch\\3\\krzywe.txt")
# scratchList4 = read_data("I:\OneDrive\\doktorat\\praca doktorska\\badania\\scratch\\4\\krzywe.txt")

sampleList = [scratchList, scratchList1]
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
        scratchObject.topo2.depth = convolve(scratchObject.topo2.depth, ones(1,)/1, mode='full')
        
        #computing max dephts
        sum1 = sum1 + scratchObject.maxDepthOfTopo2()
        maxList.append(scratchObject.maxDepthOfTopo2())
    avgMaxDepth.append(sum1/len(scratchList))
    maxDepth.append(maxList)



print('\nśrednie dla każdej próbki:')  
print(avgMaxDepth)

print('\ndla każdej próbki, dla każdego zarysowania')
print(array(maxDepth))

for scratchObject in sampleList[0]:
    pyplot.plot( scratchObject.topo2.depth, "red")
    
for scratchObject in sampleList[1]:
    pyplot.plot( scratchObject.topo2.depth, "blue")

    

#2pyplot.plot(scratchList[0].topo1.depth)

#pyplot.plot( scratchElement.topo2.depth)

#pyplot.ylim([0,1500])
pyplot.ylabel("depth [nm]")

pyplot.show()



#sampleList - list of all the samples, contains scratchList elements
#scratchList - list of all the experiments on the sample
#scratchObject - experiment, consist of 3 Pass elements topo1, scratch and topo2
#pass - each pass element consist of 6 arrays(vectors): distance, depth, load, friction, acuEmiss, fricCoeff[]

#sampleList[0][1].scratch.depth - vector of depth signal of scratch pass of second ([1]) scratch of first ([0]) sample



    
        