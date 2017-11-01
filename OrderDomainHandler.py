#!/usr/bin/env python
# coding=utf8
__author__ = 'stone'

import pycurl
import cStringIO
import json
import time

import globalDefine
import traceback
import configData
from configData import getConfig
from logHelper import getLogger
from configObjData import getConfigPage

configPage = getConfigPage()
def addDictItemValue(srcDict,srcName,dstDict,dstName):
    """add value data from srcDict to dstDict .from item data to dic"""


    if srcName in srcDict:
        localVal = srcDict.pop(srcName)
    else:
        localVal = ''
    upDict = {dstName:localVal}
    dstDict.update(upDict)

def addItemDictValue(dstDict,dstName,srcDict,srcName):
    """add value data from srcDict to dstDict .from dic to item data."""

    if srcName in srcDict:
        localVal = srcDict.pop(srcName)
    else:
        localVal = ''
    upDict = {dstName:localVal}
    dstDict.update(upDict)


def flatOrderInfoOrder(inOrderInfo):
    """update the order info according the web page show.show the data.

        so we need pull all data in list ,make them flat to show in the page.so in the page, the show will be easy.
    """
    try:
        logger = getLogger()
        logger.debug("start flat Order Info .")

        if inOrderInfo is None:
            return None

        # we only get the message we needed:
        #change the list to flat data.
        localOrderInfo = inOrderInfo

        #PolicyHolder_Usr 投保人
        configPageUsing = configPage['PolicyHolder_Usr']
        item = localOrderInfo["POLICYHOLDER_USR"]
        addDictItemValue(item,'NAME',localOrderInfo,configPageUsing['name']['dataName'])
        addDictItemValue(item,'SEX',localOrderInfo,configPageUsing['sex']['dataName'])
        addDictItemValue(item,'BIRTHDAY',localOrderInfo,configPageUsing['birthday']['dataName'])
        addDictItemValue(item,'AGE',localOrderInfo,configPageUsing['age']['dataName'])
        addDictItemValue(item,'PROFESSION',localOrderInfo,configPageUsing['profession']['dataName'])
        addDictItemValue(item,'PHONE',localOrderInfo,configPageUsing['phone']['dataName'])
        addDictItemValue(item,'IDCARDTYPE',localOrderInfo,configPageUsing['idcardtype']['dataName'])
        addDictItemValue(item,'IDCARDNO',localOrderInfo,configPageUsing['idcardno']['dataName'])
        addDictItemValue(item,'HEIGHT',localOrderInfo,configPageUsing['height']['dataName'])
        addDictItemValue(item,'WEIGHT',localOrderInfo,configPageUsing['weight']['dataName'])
        addDictItemValue(item,'PROVINCE',localOrderInfo,configPageUsing['briefAddress']['select']['select1']['inDataName'])
        addDictItemValue(item,'CITY',localOrderInfo,configPageUsing['briefAddress']['select']['select2']['inDataName'])
        addDictItemValue(item,'AREA',localOrderInfo,configPageUsing['briefAddress']['select']['select3']['inDataName'])
        addDictItemValue(item,'ADDRESS',localOrderInfo,configPageUsing['detailAddress']['dataName'])
        addDictItemValue(item,'ZIPCODE',localOrderInfo,configPageUsing['postcode']['dataName'])

        #InsurantUsr 被保人
        #a loop for multi data
        i=0
        #数据库的REST Service里面出来的就是按照顺序的,是按照创建时间排序的.

        if len(localOrderInfo["LstINSURANT_USR"]) == 0:
            configLst = {}

        if len(localOrderInfo["LstINSURANT_USR"]) == 1:
            configLst = {0:'InsurantUsr'}

        if len(localOrderInfo["LstINSURANT_USR"]) == 2:
            configLst = {0:'InsurantUsr',1:'InsurantUsrA'}

        if len(localOrderInfo["LstINSURANT_USR"]) == 3:
            configLst = {0:'InsurantUsr',1:'InsurantUsrA',2:'InsurantUsrB'}

        if len(localOrderInfo["LstINSURANT_USR"]) == 4:
            configLst = {0:'InsurantUsr',1:'InsurantUsrA',2:'InsurantUsrB',3:'InsurantUsrC'}

        for item in localOrderInfo["LstINSURANT_USR"]:

            if i==len(configLst) :
                break

            configShowPage = configLst.get(i)

            configPageUsing = configPage[configShowPage]
            addDictItemValue(item,"BENEFICIARIESRELATION",localOrderInfo,configPageUsing['relation']['dataName'])
            addDictItemValue(item,"NAME",localOrderInfo,configPageUsing['name']['dataName'])
            addDictItemValue(item,"SEX",localOrderInfo,configPageUsing['sex']['dataName'])
            addDictItemValue(item,"BIRTHDAY",localOrderInfo,configPageUsing['birthday']['dataName'])
            addDictItemValue(item,"AGE",localOrderInfo,configPageUsing['age']['dataName'])
            addDictItemValue(item,"PROFESSION",localOrderInfo,configPageUsing['profession']['dataName'])
            addDictItemValue(item,"PHONE",localOrderInfo,configPageUsing['phone']['dataName'])
            addDictItemValue(item,"IDCARDTYPE",localOrderInfo,configPageUsing['idcardtype']['dataName'])
            addDictItemValue(item,"IDCARDNO",localOrderInfo,configPageUsing['idcardno']['dataName'])
            addDictItemValue(item,"HEIGHT",localOrderInfo,configPageUsing['height']['dataName'])
            addDictItemValue(item,"WEIGHT",localOrderInfo,configPageUsing['weight']['dataName'])
            addDictItemValue(item,'PROVINCE',localOrderInfo,configPageUsing['briefAddress']['select']['select1']['inDataName'])
            addDictItemValue(item,'CITY',localOrderInfo,configPageUsing['briefAddress']['select']['select2']['inDataName'])
            addDictItemValue(item,'AREA',localOrderInfo,configPageUsing['briefAddress']['select']['select3']['inDataName'])
            addDictItemValue(item,"ADDRESS",localOrderInfo,configPageUsing['detailAddress']['dataName'])
            addDictItemValue(item,"ZIPCODE",localOrderInfo,configPageUsing['postcode']['dataName'])
            i=i+1

        #Lstbeneficiaries 受益人
        #a loop for multi data
        i=0
        for item in localOrderInfo["Lstbeneficiaries"]:
            configLst = {0:'BeneficiaryUsr'}

            #only show 1 BeneficiaryUsr
            #TODO: how to dynamic in page?
            if i==len(configLst) :
                break

            configShowPage = configLst.get(i)

            configPageUsing = configPage[configShowPage]
            addDictItemValue(item,"BENEFICIARIESRELATION",localOrderInfo,configPageUsing['relation']['dataName'])
            addDictItemValue(item,"NAME",localOrderInfo,configPageUsing['name']['dataName'])
            addDictItemValue(item,"SEX",localOrderInfo,configPageUsing['sex']['dataName'])
            addDictItemValue(item,"BIRTHDAY",localOrderInfo,configPageUsing['birthday']['dataName'])
            addDictItemValue(item,"AGE",localOrderInfo,configPageUsing['age']['dataName'])
            addDictItemValue(item,"PHONE",localOrderInfo,configPageUsing['phone']['dataName'])
            addDictItemValue(item,"IDCARDTYPE",localOrderInfo,configPageUsing['idcardtype']['dataName'])
            addDictItemValue(item,"IDCARDNO",localOrderInfo,configPageUsing['idcardno']['dataName'])
            i=i+1

        #InsurantPlan 保险计划
        configPageUsing = configPage['InsurantPlan']
        item = localOrderInfo
        addDictItemValue(item,'INSURANCECODE',localOrderInfo,configPageUsing['product']['dataName'])
        addDictItemValue(item,'SECURITYPLAN',localOrderInfo,configPageUsing['plan']['dataName'])
        addDictItemValue(item,'PREMIUMPLAN',localOrderInfo,configPageUsing['planFamily']['dataName'])
        addDictItemValue(item,'PAYMENTSTATUS',localOrderInfo,configPageUsing['paymentstatus']['dataName'])
        addDictItemValue(item,'DMPAYMODE',localOrderInfo,configPageUsing['dmpaymode']['dataName'])
        addDictItemValue(item,'DMPAYBANK',localOrderInfo,configPageUsing['paybank']['dataName'])
        addDictItemValue(item,'CARDID',localOrderInfo,configPageUsing['cardid']['dataName'])

        #TODO: right 续期帐号
        addDictItemValue(item,'DMPAYCOMPANY',localOrderInfo,configPageUsing['dmpaybankext']['dataName'])
        addDictItemValue(item,'PURCHASECOUNT',localOrderInfo,configPageUsing['purchasecount']['dataName'])
        addDictItemValue(item,'DMCONTINUATIONYEARS',localOrderInfo,configPageUsing['dmcontinuationyears']['dataName'])
        addDictItemValue(item,'DMPAYTYPE',localOrderInfo,configPageUsing['dmpaytype']['dataName'])
        addDictItemValue(item,'DMPOLICYDATES',localOrderInfo,configPageUsing['dmpolicydates']['dataName'])
        addDictItemValue(item,'NOTE',localOrderInfo,configPageUsing['note']['dataName'])

        #delivery 保单配送
        configPageUsing = configPage['delivery']
        item = localOrderInfo
        addDictItemValue(item,'DELIVERYDATE',localOrderInfo,configPageUsing['dateTime']['dataName'])
        addDictItemValue(item,'PROVINCE',localOrderInfo,configPageUsing['deliveryAddress']['select']['select1']['inDataName'])
        addDictItemValue(item,'CITY',localOrderInfo,configPageUsing['deliveryAddress']['select']['select2']['inDataName'])
        addDictItemValue(item,'AREA',localOrderInfo,configPageUsing['deliveryAddress']['select']['select3']['inDataName'])
        addDictItemValue(item,'DELIVERYADDRESS',localOrderInfo,configPageUsing['detailAddress']['dataName'])

        logger.debug("update localOrderInfo success.")

        return localOrderInfo
    except:
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
    else:
        pass
    finally:
        pass

def zipOrderInfoOrder(inOrderInfo):
    """update the order info according the web page show.post the data.

        so we need pull all data in form ,make them zip to post in the page.
    """
    try:
        logger = getLogger()
        logger.debug("start zip Order Info .")

        if inOrderInfo is None:
            return None

        # we only get the message we needed:
        #change the flat to list data.
        localOrderInfo = inOrderInfo

        localCrdt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        #PolicyHolder_Usr 投保人
        configPageUsing = configPage['PolicyHolder_Usr']

        item = {}

        addItemDictValue(item,'NAME',localOrderInfo,configPageUsing['name']['dataName'])
        addItemDictValue(item,'SEX',localOrderInfo,configPageUsing['sex']['dataName'])
        addItemDictValue(item,'BIRTHDAY',localOrderInfo,configPageUsing['birthday']['dataName'])
        addItemDictValue(item,'AGE',localOrderInfo,configPageUsing['age']['dataName'])
        addItemDictValue(item,'PROFESSION',localOrderInfo,configPageUsing['profession']['dataName'])
        addItemDictValue(item,'PHONE',localOrderInfo,configPageUsing['phone']['dataName'])
        addItemDictValue(item,'IDCARDTYPE',localOrderInfo,configPageUsing['idcardtype']['dataName'])
        addItemDictValue(item,'IDCARDNO',localOrderInfo,configPageUsing['idcardno']['dataName'])
        addItemDictValue(item,'HEIGHT',localOrderInfo,configPageUsing['height']['dataName'])
        addItemDictValue(item,'WEIGHT',localOrderInfo,configPageUsing['weight']['dataName'])
        addItemDictValue(item,'PROVINCE',localOrderInfo,configPageUsing['briefAddress']['select']['select1']['inDataName'])
        addItemDictValue(item,'CITY',localOrderInfo,configPageUsing['briefAddress']['select']['select2']['inDataName'])
        addItemDictValue(item,'AREA',localOrderInfo,configPageUsing['briefAddress']['select']['select3']['inDataName'])
        addItemDictValue(item,'ADDRESS',localOrderInfo,configPageUsing['detailAddress']['dataName'])
        addItemDictValue(item,'ZIPCODE',localOrderInfo,configPageUsing['postcode']['dataName'])

        #创建人和创建时间
        upDict = {'CRUSR':inOrderInfo['CRUSR']}
        item.update(upDict)
        upDict = {'CRDT':localCrdt}
        item.update(upDict)

        upDict = {'POLICYHOLDER_USR':item}
        localOrderInfo.update(upDict)

        #InsurantUsr 被保人
        #a loop for multi data
		#total save 4 Insurant, the 4 Insurant DIV saved in html file.
        #only save used Insurant.
        if 'INSURANT_USR_NAMEA' in localOrderInfo:
            configDict = {0:'InsurantUsr',1:'InsurantUsrA'}
        else:
            configDict = {0:'InsurantUsr'}

        if 'INSURANT_USR_NAMEB' in localOrderInfo:
            upDict = {2:'InsurantUsrB'}
            configDict.update(upDict)
        else:
            pass

        if 'INSURANT_USR_NAMEC' in localOrderInfo:
            upDict = {3:'InsurantUsrC'}
            configDict.update(upDict)
        else:
            pass

        localLst =[]

        #a dictionary list
        step=len(configDict)
        for i in range(step):
            item = {}

            configShowPage = configDict.get(i)

            configPageUsing = configPage[configShowPage]
            addItemDictValue(item,"BENEFICIARIESRELATION",localOrderInfo,configPageUsing['relation']['dataName'])
            addItemDictValue(item,"NAME",localOrderInfo,configPageUsing['name']['dataName'])
            addItemDictValue(item,"SEX",localOrderInfo,configPageUsing['sex']['dataName'])
            addItemDictValue(item,"BIRTHDAY",localOrderInfo,configPageUsing['birthday']['dataName'])
            addItemDictValue(item,"AGE",localOrderInfo,configPageUsing['age']['dataName'])
            addItemDictValue(item,"PROFESSION",localOrderInfo,configPageUsing['profession']['dataName'])
            addItemDictValue(item,"PHONE",localOrderInfo,configPageUsing['phone']['dataName'])
            addItemDictValue(item,"IDCARDTYPE",localOrderInfo,configPageUsing['idcardtype']['dataName'])
            addItemDictValue(item,"IDCARDNO",localOrderInfo,configPageUsing['idcardno']['dataName'])
            addItemDictValue(item,"HEIGHT",localOrderInfo,configPageUsing['height']['dataName'])
            addItemDictValue(item,"WEIGHT",localOrderInfo,configPageUsing['weight']['dataName'])
            addItemDictValue(item,'PROVINCE',localOrderInfo,configPageUsing['briefAddress']['select']['select1']['inDataName'])
            addItemDictValue(item,'CITY',localOrderInfo,configPageUsing['briefAddress']['select']['select2']['inDataName'])
            addItemDictValue(item,'AREA',localOrderInfo,configPageUsing['briefAddress']['select']['select3']['inDataName'])
            addItemDictValue(item,"ADDRESS",localOrderInfo,configPageUsing['detailAddress']['dataName'])
            addItemDictValue(item,"ZIPCODE",localOrderInfo,configPageUsing['postcode']['dataName'])

            #创建人和创建时间
            upDict = {'CRUSR':inOrderInfo['CRUSR']}
            item.update(upDict)
            upDict = {'CRDT':localCrdt}
            item.update(upDict)

            localLst.append(item)

        upDict = {'LstINSURANT_USR':localLst}
        localOrderInfo.update(upDict)

        #Lstbeneficiaries 受益人
        #a loop for multi data
        #only show 1 BeneficiaryUsr
        #TODO: every time ,save 1 data?

        if 'Lstbeneficiaries_NAME' in localOrderInfo:
            configDict = {0:'BeneficiaryUsr'}
        else:
            configDict = {}

        localLst = []

        #a dictionary list
        step=len(configDict)
        #TODO: how to dynamic in page?多个受益人还没有实现，参考多个被保人.
        for i in range(step):
            item = {}

            configShowPage = configDict.get(i)

            configPageUsing = configPage[configShowPage]
            addItemDictValue(item,"BENEFICIARIESRELATION",localOrderInfo,configPageUsing['relation']['dataName'])
            addItemDictValue(item,"NAME",localOrderInfo,configPageUsing['name']['dataName'])
            addItemDictValue(item,"SEX",localOrderInfo,configPageUsing['sex']['dataName'])
            addItemDictValue(item,"BIRTHDAY",localOrderInfo,configPageUsing['birthday']['dataName'])
            addItemDictValue(item,"AGE",localOrderInfo,configPageUsing['age']['dataName'])
            addItemDictValue(item,"PHONE",localOrderInfo,configPageUsing['phone']['dataName'])
            addItemDictValue(item,"IDCARDTYPE",localOrderInfo,configPageUsing['idcardtype']['dataName'])
            addItemDictValue(item,"IDCARDNO",localOrderInfo,configPageUsing['idcardno']['dataName'])

            #创建人和创建时间
            upDict = {'CRUSR':inOrderInfo['CRUSR']}
            item.update(upDict)
            upDict = {'CRDT':localCrdt}
            item.update(upDict)

            localLst.append(item)

        upDict = {'Lstbeneficiaries':localLst}
        localOrderInfo.update(upDict)

        #InsurantPlan 保险计划
        configPageUsing = configPage['InsurantPlan']
        item = localOrderInfo
        addItemDictValue(item,'INSURANCECODE',localOrderInfo,configPageUsing['product']['dataName'])
        addItemDictValue(item,'SECURITYPLAN',localOrderInfo,configPageUsing['plan']['dataName'])
        addItemDictValue(item,'PREMIUMPLAN',localOrderInfo,configPageUsing['planFamily']['dataName'])
        addItemDictValue(item,'PAYMENTSTATUS',localOrderInfo,configPageUsing['paymentstatus']['dataName'])
        addItemDictValue(item,'DMPAYMODE',localOrderInfo,configPageUsing['dmpaymode']['dataName'])
        addItemDictValue(item,'DMPAYBANK',localOrderInfo,configPageUsing['paybank']['dataName'])
        addItemDictValue(item,'CARDID',localOrderInfo,configPageUsing['cardid']['dataName'])

        #TODO: right 续期帐号
        addItemDictValue(item,'DMPAYCOMPANY',localOrderInfo,configPageUsing['dmpaybankext']['dataName'])
        addItemDictValue(item,'PURCHASECOUNT',localOrderInfo,configPageUsing['purchasecount']['dataName'])
        addItemDictValue(item,'DMCONTINUATIONYEARS',localOrderInfo,configPageUsing['dmcontinuationyears']['dataName'])
        addItemDictValue(item,'DMPAYTYPE',localOrderInfo,configPageUsing['dmpaytype']['dataName'])
        addItemDictValue(item,'DMPOLICYDATES',localOrderInfo,configPageUsing['dmpolicydates']['dataName'])
        addItemDictValue(item,'NOTE',localOrderInfo,configPageUsing['note']['dataName'])

        #delivery 保单配送
        configPageUsing = configPage['delivery']
        item = localOrderInfo
        addItemDictValue(item,'DELIVERYDATE',localOrderInfo,configPageUsing['dateTime']['dataName'])
        addItemDictValue(item,'PROVINCE',localOrderInfo,configPageUsing['deliveryAddress']['select']['select1']['inDataName'])
        addItemDictValue(item,'CITY',localOrderInfo,configPageUsing['deliveryAddress']['select']['select2']['inDataName'])
        addItemDictValue(item,'AREA',localOrderInfo,configPageUsing['deliveryAddress']['select']['select3']['inDataName'])
        addItemDictValue(item,'DELIVERYADDRESS',localOrderInfo,configPageUsing['detailAddress']['dataName'])

        logger.debug("update localOrderInfo success.")

        return localOrderInfo
    except:
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
    else:
        pass
    finally:
        pass

def updateDictSingleValue(srcDict,dstName,dstValue):
    if dstName in srcDict:
        srcDict[dstName] = dstValue
        pass
    else:
        #add value data to dscName to srcDict
        upDict = {dstName:dstValue}
        srcDict.update(upDict)

def postOrderInfoContact(inContactid,storageData,inStatus,inCrusr,inGrpid):
    try:
        logger = getLogger()
        logger.debug("start POST Order Info according contact id.")

        if inCrusr == '':
            logger.debug("no input crusr.")
            return None

        if inGrpid == '':
            logger.debug("no input group.")
            return None

        jsonData = json.dumps(storageData)
        dictData = json.loads(jsonData)

        #add contactid
        updateDictSingleValue(dictData,"CONTACTID",inContactid)

        #add addressid
        #TODO: still need this?
        updateDictSingleValue(dictData,"ADDRESSID",'1')

        #add crusr
        updateDictSingleValue(dictData,"CRUSR",inCrusr)

        #add grpid
        updateDictSingleValue(dictData,"GRPID",inGrpid)

        #update status
        updateDictSingleValue(dictData,"STATUS",inStatus)

        #zip the dict
        dictData = zipOrderInfoOrder(dictData)

        jsonData =  json.dumps(dictData)

        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        localURL = getConfig('RESTService','orderInfoUrl','str')
        localURL = str(localURL)
        c.setopt(pycurl.URL,localURL)
        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(jsonData))])
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CUSTOMREQUEST,"POST")
        c.setopt(pycurl.POSTFIELDS,jsonData)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(pycurl.USERPWD,getConfig('allowedUser1','UserName','str')+':'+getConfig('allowedUser1','Password','str'))
        c.perform()

        #TODO: how to show succes code? 200 or OK?
        http_code = c.getinfo(pycurl.HTTP_CODE)
        #judge post success.
        if http_code != 201:
            return None

        logger.debug(buf.getvalue())
        retStr = buf.getvalue()

        buf.close()
        c.close()

        logger.debug("post OrderInfo success.")
        return retStr

    except pycurl.error, error:
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()

        errno, errstr = error
        print 'An error occurred: ', errstr
    else:
        pass
    finally:
        pass

def putOrderStatusInfoContact(inOrderid,inStatus,storageData,inCrusr):
    try:
        logger = getLogger()
        logger.debug("start PUT Order Status Info according contact id.")

        jsonData = json.dumps(storageData)
        dictData = json.loads(jsonData)

        #update status
        updateDictSingleValue(dictData,"STATUS",inStatus)

        #add orderid
        updateDictSingleValue(dictData,"ORDERID",inOrderid)

        #add crusr
        updateDictSingleValue(dictData,"CRUSR",inCrusr)

        dictData = zipOrderInfoOrder(dictData)

        jsonData =  json.dumps(dictData)

        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        localURL = getConfig('RESTService','orderInfoUrl','str')
        localURL = str(localURL)
        c.setopt(pycurl.URL,localURL)
        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(jsonData))])
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CUSTOMREQUEST,"PUT")
        c.setopt(pycurl.POSTFIELDS,jsonData)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(pycurl.USERPWD,getConfig('allowedUser1','UserName','str')+':'+getConfig('allowedUser1','Password','str'))
        c.perform()

        #TODO: how to show succes code? 200 or OK?
        http_code = c.getinfo(pycurl.HTTP_CODE)
        #judge put success.
        if http_code != 201:
            return None

        logger.debug(buf.getvalue())
        retStr = buf.getvalue()

        buf.close()
        c.close()

        logger.debug("put OrderInfo success.")
        return retStr

    except pycurl.error, error:
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()

        errno, errstr = error
        print 'An error occurred: ', errstr
    else:
        pass
    finally:
        pass

def putOrderInfoContact(inOrderid,storageData,inStatus,inCrusr):
        try:
            logger = getLogger()
            logger.debug("start PUT Order Info according contact id.")

            jsonData = json.dumps(storageData)
            dictData = json.loads(jsonData)

            #add orderid
            updateDictSingleValue(dictData,"ORDERID",inOrderid)

            updateDictSingleValue(dictData,"STATUS",inStatus)

            #add crusr
            updateDictSingleValue(dictData,"CRUSR",inCrusr)

            dictData = zipOrderInfoOrder(dictData)

            jsonData =  json.dumps(dictData)

            buf = cStringIO.StringIO()
            c = pycurl.Curl()
            localURL = getConfig('RESTService','orderInfoUrl','str')
            localURL = str(localURL)
            c.setopt(pycurl.URL,localURL)
            c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(jsonData))])
            c.setopt(c.VERBOSE, True)
            c.setopt(pycurl.CUSTOMREQUEST,"PUT")
            c.setopt(pycurl.POSTFIELDS,jsonData)
            c.setopt(c.WRITEFUNCTION,buf.write)
            c.setopt(pycurl.USERPWD,getConfig('allowedUser1','UserName','str')+':'+getConfig('allowedUser1','Password','str'))
            c.perform()


            #TODO: how to show succes code? 200 or OK?
            http_code = c.getinfo(pycurl.HTTP_CODE)
            #judge put success.
            if http_code != 201:
                return None


            logger.debug(buf.getvalue())
            retStr = buf.getvalue()

            buf.close()
            c.close()

            logger.debug("put OrderInfo success.")
            return retStr

        except pycurl.error, error:
            logger.error("exception occur, see the traceback.log")

            #异常写入日志文件.
            f = open('traceback.txt','a')
            traceback.print_exc()
            traceback.print_exc(file = f)
            f.flush()
            f.close()

            errno, errstr = error
            print 'An error occurred: ', errstr
        else:
            pass
        finally:
            pass

