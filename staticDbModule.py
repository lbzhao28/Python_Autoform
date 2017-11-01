__author__ = 'stone'

import configObjData
from configObjData import getConfigFile

import OrderClient
from OrderClient import getStaticLst

def getDictStatic(inSourceID):
    """get the static data from the different source

        Source may be: web cache,db,REST and web service , config file.
        Now ,we user cache to accelerate the speed.
        return a dictionary.
    """

    #TODO: use cache or Redis to finish this function.

    #TODO: use global to get data from db or web service.

    #TODO: two data value OK to select,how about radio?


    #get data from configfile.
    #configFile = getConfigFile("staticConf.conf")
    #retDict = configFile.dict()
    #tDict = retDict[inSourceID]

    #get data from service.
    localStaticLst = getStaticLst(inSourceID)
    retDict = convertDict(localStaticLst)

    return retDict

def convertDict(inLst):
    if inLst is None:
        return None
    retDict = {};
    i = 0
    for item in inLst:
        dictName = 'data'+str(i)
        localVal = item["ID"]
        localText = item["DSC"]
        upDict = {'value':localVal,'text':localText}
        upDict = {dictName:upDict}
        retDict.update(upDict)
        i = i+1
    return retDict


if __name__ == "__main__":
    print getDictStatic("CON.ORDER.STATUS")
