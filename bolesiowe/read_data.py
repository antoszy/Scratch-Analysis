from Scratch import *

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
    
