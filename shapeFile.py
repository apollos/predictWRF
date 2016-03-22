import os
import os.path
import myDebug
import re
import numpy as np

def listAllFiles(fullPath):

    fullPath=fullPath.strip()
    fileList = []
    try:
        for parentPath,dirNames,fileNames in os.walk(fullPath, topdown=True):
            #for dirName in dirNames:
            #    fileList.extend(listAllFiles(os.path.join(parentPath+dirName)))
            for fileName in fileNames:
                fileList.insert(len(fileList), os.path.join(parentPath, fileName))

    except IOError as err:
        print("IO Error: "+str(err))
    
    return fileList

def shapeWrfIOfile(fileList, fileExt, keyWord):
    dataKey = "domain"
    wrfIODict = {}
    for filePath in fileList:
        if filePath.endswith(fileExt):
            domain = {}
            #This place, we can use ML to check what is the data character by word segmetation, like how many domain to seperate and so on
            #but now, to simplify, I just think there are 4 domain
            fr = open(filePath)
            for line in fr.readlines():
                if (line.find(keyWord) >= 0) and (line.find(dataKey) >= 0):
                    tmpStr = line[line.find(dataKey)+len(dataKey):]
                    pattern = re.compile(r'\D*(\d+):\D*(\d+\.*\d*)') # not good, I will change it by word segmetation method
                    match = pattern.findall(tmpStr)
                    if len(match) > 0 and len(match[0]) == 2:
                        if match[0][0] in domain.keys():
                            domain[match[0][0]].append(match[0][1])
                        else:
                            tmpList = []
                            tmpList.append(match[0][1])
                            domain[match[0][0]] = tmpList
                    else:
                        print("%s  %d: Error Pattern [%s]" %(myDebug.file(), myDebug.line(), line))
            # sort keys
            if domain:                
                wrfIODict[filePath] = domain    
    return wrfIODict


def shapeWrfComputingfile(fileList):
    #To be enhance, now it is fixed
    #Read .000file to konw the computing size
    #read .0 file to know task number and consumed time
    wrfOutFileExt = ".0000"
    wrfProfileExt = ".0"
    wrfComputeList = []#4 columns: task number, nTaskX, nTaskY, consumed computing time, consumed communication time
    taskNumMark = "Data for MPI rank"

    domainNum = 0
    writeNum = 0
    taskNum = 0
    nTaskX = np.inf
    nTaskY = np.inf
    compInfo = []
    currentDir = ""
    filePath = ""

    for filePath in fileList:
        if currentDir != "" and currentDir != os.path.dirname(filePath):# change folder, save current data
            tmpList = fillComputList(domainNum, writeNum, taskNum, nTaskX, nTaskY, compInfo, os.path.dirname(filePath))
            if not tmpList:
                return
            wrfComputeList = fillwrfComputeList(wrfComputeList, tmpList)
        currentDir = os.path.dirname(filePath)
        #read .000 file
        if os.path.splitext(filePath)[1] == wrfOutFileExt:
            keyWord = "wrfout"
            dataKey = "domain"
            domainNum = 0
            writeNum = 0
            fr = open(filePath)
            for line in fr.readlines():
                if (line.find(keyWord) >= 0) and (line.find(dataKey) >= 0):
                    tmpStr = line[line.find(dataKey)+len(dataKey):]
                    pattern = re.compile(r'\D*(\d+):\D*(\d+\.*\d*)') # not good, I will change it by word segmetation method
                    match = pattern.findall(tmpStr)
                    if len(match[0]) == 2:
                        if int(match[0][0]) > domainNum:
                            domainNum = int(match[0][0])
                        writeNum += 1
                    else:
                        print("%s  %d: Error Pattern [%s]" %(myDebug.file(), myDebug.line(), line))
                if (line.lower().find("ntasks") >= 0):
                    tmpStr = line
                    #Ntasks in X  5 , ntasks in Y  8
                    pattern = re.compile(r'\D*(\d+)\ *,\D*(\d+)') # not good, I will change it by word segmetation method
                    match = pattern.findall(tmpStr)
                    if len(match[0]) == 2:
                        nTaskX = int(match[0][0])
                        nTaskY = int(match[0][1])
                    else:
                        print("%s  %d: Error Pattern [%s]" %(myDebug.file(), myDebug.line(), line))
            fr.close()
        #read .0 file
        elif os.path.splitext(filePath)[1] == wrfProfileExt:
            fr = open(filePath)
            keyWord = taskNumMark
            taskNum =0
            compInfo = []
            fillF = False
            count = 0
            for line in fr.readlines():
                if fillF:#start to fill the tasks information into the list
                    tmpData = line.split() 
                    compInfo.append([float(tmpData[2]) - float(tmpData[1]), float(tmpData[1])])#Computing time, communication time
                    count += 1
                    if count == taskNum:
                        fillF = False #end
                else:
                    if (line.find(keyWord) >= 0):
                        pattern = re.compile(r'\D*(\d+)\D*(\d+):')
                        match = pattern.findall(line)
                        if int(match[0][0]) != 0: #Just according to current log, it is may not right
                            print("%s  %d: Find a not expected record [%s] [%d]" %(myDebug.file(), myDebug.line(), line, match[0][0]))
                        else:
                            taskNum = int(match[0][1])
                    if(line.find("taskid") >= 0 and line.find("comm(s)") >= 0 and line.find("elapsed(s)") >= 0):
                        #start to read time information
                        fillF = True
            fr.close()
    #last dataset to be filled
    if filePath != "":
        tmpList = fillComputList(domainNum, writeNum, taskNum, nTaskX, nTaskY, compInfo, os.path.dirname(filePath))
        if not tmpList:
            return
        wrfComputeList = fillwrfComputeList(wrfComputeList, tmpList)
    return wrfComputeList              
            
def fillComputList(domainNum, writeNum, taskNum, nTaskX, nTaskY, compInfo, currentDir):
    tmpComputeList = []
    if domainNum == 0 or writeNum == 0 or writeNum%domainNum != 0 or taskNum ==0 or nTaskX == np.inf or nTaskY == np.inf or not compInfo:
        print("%s  %d: Failed read profiling information in %s [Domanin:%d   WriteNum:%d   TaskNum:%d]" %(myDebug.file(), myDebug.line(), currentDir, domainNum, writeNum, taskNum))
    else:
        #print("Domanin:%d   WriteNum:%d   TaskNum:%d" %(domainNum, writeNum, taskNum))
        for i in range(0,taskNum):
            tmpList = [taskNum, nTaskX, nTaskY, writeNum/domainNum - 1]#writeNum/domainNum is the true write time, but seems the first write is a specaill write shall not be caculated
            tmpList.extend(compInfo[i])
            tmpComputeList.append(tmpList)   
    return tmpComputeList

def fillwrfComputeList(wrfComputeList, tmpList):
    #task 0 seems very special, so I seperate it, it may change in future, it is not a good machine learning method here
    if not wrfComputeList:
        wrfComputeList.append([tmpList[0]])
        wrfComputeList.append(tmpList[1:])
    else:
        wrfComputeList[0].extend([tmpList[0]])
        wrfComputeList[1].extend(tmpList[1:])
    return wrfComputeList

