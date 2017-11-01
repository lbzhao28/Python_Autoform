__author__ = 'stone'
#encoding:utf-8
#File:settingTools.py
#this file to get the db to create js file.
import time
import string

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def writeArrayCityJs():
    f = open('./static/js/localAddressList.js','w')
    try:
        writeLst = []

        strData = '/**\n'
        writeLst.append(strData)

        strData = '* Created by python tools\n'
        writeLst.append(strData)

        strData = '* User: stone\n'
        writeLst.append(strData)

        strData = '* Date: ' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '\n'
        writeLst.append(strData)

        strData = '* Time: ' + time.strftime('%H-%M-%S',time.localtime(time.time())) + '\n'
        writeLst.append(strData)

        strData = '* only change the file by tools.\n'
        writeLst.append(strData)

        strData = '*/\n'
        writeLst.append(strData)

        strData = 'function createArrayCity()\n'
        writeLst.append(strData)

        strData = '{\n'
        writeLst.append(strData)

        strData = '     var arrayCity=new Array();\n'
        writeLst.append(strData)

        #TODO: a loop to get data from db.
        addressList = getAddressListOracle()
        i = 0
        for item in addressList:
            strData = '     arrayCity['+str(i)+']=new Array('
            strData = strData + str(item[0])+','
            strData = strData + str(item[1])+','
            strData = strData + str(item[2])+','
            strData = strData +'"'+ str(item[3])+'"'
            strData = strData + ');\n'
            writeLst.append(strData)
            i = i+1


        strData = '     return arrayCity;\n'
        writeLst.append(strData)

        strData = '}\n'
        writeLst.append(strData)

        f.writelines(writeLst)
        pass
    finally:
        f.close()

if __name__ == "__main__":
    writeArrayCityJs()

