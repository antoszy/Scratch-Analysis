from Scratch import *
from Pass import *

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

