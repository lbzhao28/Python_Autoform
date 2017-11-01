__author__ = 'stone'

from configobj import ConfigObj
import os

def getConfigPage():
    """get the page config file"""


    #print os.getcwd()
    #os.chdir('..')
    #os.chdir('D:\Stone\Python\Python_Insurance')
    #print os.getcwd()

    #configPage = ConfigObj('pagesConf.conf')
    configPage = ConfigObj('thirdevalConf.conf')

    #configPagePolicyHolder_Usr = configPage['PolicyHolder_Usr']
    #dictFirst = configPagePolicyHolder_Usr.dict()
    #print dictFirst
    #j = 2
    #for j in range(j):
    #    for member in dictFirst:
    #        if 'titleText' in dictFirst[member]:
    #            print member
    #            dictSecond = dictFirst[member]
    #            print dictSecond
    #            break
    #    dictFirst.pop(member)
            #i = i+1
            #print i
        #for item in configPagePolicyHolder_Usr[member]:
        #    print configPagePolicyHolder_Usr[member][item]
        #for item in member:
        #    print member[item]
    #print configPage
    #print configPagePolicyHolder_Usr
    #configPagePolicyHolder_Usr = configPage['PolicyHolder_Usr']
    #print configPagePolicyHolder_Usr

    #print configPagePolicyHolder_Usr.as_int( 'rowNumber')
    #print configPage.as_bool("hasPolicyHolder_Usr")
    return configPage

def getConfigFile(inFileName):
    """get the Static config file"""

    configFile = ConfigObj(inFileName)
    return configFile

if __name__ == "__main__":
    getConfigPage()
