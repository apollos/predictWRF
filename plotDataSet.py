from __future__ import division
import shapeFile as sF
import matplotlib  
import matplotlib.pyplot as plt
import numpy as np

files = sF.listAllFiles("Data/sameCompute/")
trainDataList = sF.shapeWrfComputingfile(files)

#trainDataList[0] - task 0 info
#trainDataList[1] - other task info
#trainDataList structure [task size, computing size, computing time, communication time]

xAx = []
yAx = []
cAx = []
color = ['g', 'r', 'b', 'y', 'c', 'k', 'g', 'r', 'b', 'y', 'c', 'k', 'g', 'r', 'b', 'y', 'c', 'k', 'g', 'r', 'b', 'y', 'c', 'k', 'g', 'r', 'b', 'y', 'c', 'k', 'g']

n = np.shape(trainDataList[0])[1]
for DataSet in trainDataList:
    for DataInf in DataSet:        
        tmpX = DataInf[0]
        tmpX2 = DataInf[n - 3]
        tmpY1 = DataInf[n - 2]
        tmpY2 = DataInf[n - 1]
        xAx.append(tmpX)
        yAx.append((tmpY1, tmpY2))
        cAx.append(color[tmpX2%len(color)])

minX = min(xAx)
xAx = np.array(xAx, dtype = float)/float(minX)
yAx = np.array(yAx, dtype = float)

fig = plt.figure(0, figsize=(16,12))
fig.suptitle("Same Computing Hours")   

subplots = range(0, 4)
subplots[0] = plt.subplot(2,2,1)
plt.ylabel('Consumed Time(s)')
plt.xlabel('Task Num')
plt.title('Computing Trend')

subplots[0].scatter(xAx, yAx[:,0],c=cAx, s=25,alpha=0.4,marker='o')


subplots[1] = plt.subplot(2,2,2)
plt.ylabel('Consumed Time(s)')
plt.xlabel('Task Num')
plt.title('Communication Trend')
subplots[1].scatter(xAx, yAx[:,1],c=cAx, s=25,alpha=0.4,marker='o')

predictRst = [[40, 2320.232922334759, 568.2877816141595], [60, 1813.3047008708777, 505.1027439677073], [80, 1632.3314005044258, 513.3756047339241], [100, 1451.7371609435509, 521.7039102051319], [120, 1173.9816998963233, 466.09437955495514], [140, 896.3736432385423, 410.51437793028595], [160, 618.9134433079873, 354.96400268992267], [180, 711.8950306166118, 402.074849015552], [200, 64.43842387826976, 243.95252091977977], [220, 107.87218685454638, 258.9126489852076], [240, 568.3654647109711, 408.1534986387647], [260, 192.50841545557273, 288.43359643106544], [280, 233.71495312665388, 302.9951425900348], [300, 274.18314190673493, 317.4245526536073], [320, 313.9149990250065, 331.7221866474787], [340, 352.912534135187, 345.88840324299076], [360, 391.17774930111227, 359.92355975653527], [380, 428.71263896195455, 373.82801214251833], [400, 465.5191899102306, 387.6021149935512], [420, 453.0265144758787, 369.2548584806019]]


subplots[2] = plt.subplot(2,2,3)
plt.ylabel('Consumed Time(s)')
plt.xlabel('Task Num')
plt.title('Total Time Trend')
subplots[2].scatter(xAx, yAx[:, 0]+yAx[:, 1],c=cAx, s=25,alpha=0.4,marker='o')
predictMat = np.array(predictRst, dtype = float)

xAx = predictMat[:, 0]/float(minX)
'''
yAx = predictMat[:, 1]
subplots[2].scatter(xAx, yAx, c='r',s=25,marker='o')
'''
yAx1 = predictMat[:, 1]
yAx2 = predictMat[:, 2]
yAx3 = yAx1+yAx2
'''
subplots[0].scatter(xAx, yAx1, c='r',s=25,marker='o')
subplots[1].scatter(xAx, yAx2, c='r',s=25,marker='o')
subplots[2].scatter(xAx, yAx3, c='r',s=25,marker='o')
'''
subplots[0].plot(xAx, yAx1, c='r')
subplots[1].plot(xAx, yAx2, c='r')
subplots[2].plot(xAx, yAx3, c='r')

'''
###################################################3
files = sF.listAllFiles("/home/yu/workspace/Data/sameTask/")
trainDataList = sF.shapeWrfComputingfile(files)

xAx = []
yAx = []
cAx = []

for DataSet in trainDataList:
    for DataInf in DataSet:        
        tmpX = DataInf[1]
        tmpY1 = DataInf[2]
        tmpY2 = DataInf[3]
        tmpX2 = DataInf[0]
        xAx.append(tmpX)
        yAx.append((tmpY1, tmpY2))
        cAx.append(color[tmpX2%len(color)])

minX = min(xAx)
xAx = np.array(xAx, dtype = float)/float(minX)
yAx = np.array(yAx, dtype = float)/float(500)

fig = plt.figure(1, figsize=(16,12))
fig.suptitle("Same Task Size")   

subplots = range(0, 2)
subplots[0] = plt.subplot(1,2,1)
plt.ylabel('Consumed Time(500s)')
plt.xlabel('Compute Data Size')
plt.title('Computing Trend')

subplots[0].scatter(xAx, yAx[:,0],s=25,alpha=0.4,marker='o', c=cAx)


subplots[1] = plt.subplot(1,2,2)
plt.ylabel('Consumed Time(500s)')
plt.xlabel('Task Num')
plt.title('Communication Trend')
subplots[1].scatter(xAx, yAx[:,1],s=25,alpha=0.4,marker='o', c=cAx)
'''
plt.show()

