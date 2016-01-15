# -*- coding: utf-8 -*-
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels
def classify0(inX,dataSet,labels,k):
    #shape会获得矩阵的维数，是一个元组，比如n*m的矩阵，返回的是（n,m）
    dataSetSize=dataSet.shape[0]
    #title第一个参数是矩阵,第二个参数是一个数字是表示对矩阵重复次数，不会增加矩阵维数，第二个参数是一个二元组时
    #二元组的第二个数，表示重复次数，不会增加矩阵维数，第一个数表示重复多个矩阵，会增加维数
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    #**表示N次幂
    sqDiffMat=diffMat**2
    #sum函数中axis=0表示按列求和 axis=1表示按行求和，并会降至一维
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    #argsort返回列表从小到大排序的索引
    #eg:a=[5,10,3]
    #a.argsort()
    #[1,2,0]
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        #字典的get（key,def）当key不存在时，返回def
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    #operator.itemgetter(n)获得对象的第n个域
    #sorter()第一个参数为迭代对象，按key排序，reverse=True表示倒序排列即从大到小排列,返回的是一个列表，里面存放元组
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    #zeros（（n,m））函数的作用返回一个n*m的全零矩阵
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    #dic={'largeDoses':3,'smallDoses':2,'didntLike':1}
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
def autoNorm(dataSet):
    #找出当前列中的最小值
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('H:\pythonfornumber\ch02\datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d,the real answer is: %d"%(classifierResult,datingLabels[i])
        if (classifierResult!=datingLabels[i]):errorCount+=1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
def classifyPerson():
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("precentage of time spent playing video games"))
    ffMiles=float(raw_input("frequent fliter miles earned per year?"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels=file2matrix('H:\pythonfornumber\ch02\datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person:",resultList[classifierResult-1]
if __name__ == '__main__':
    classifyPerson()
    # datingDataMat,classLabelVector=file2matrix('H:\pythonfornumber\ch02\datingTestSet.txt')
    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(classLabelVector),15.0*array(classLabelVector))
    # plt.show()