#!/usr/bin/env python
# coding=utf8
__author__ = 'stone'
# the domain logic for third eval.

import pycurl
import cStringIO
import json
import time

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


def flatThirdEvalInfo(inThirdEvalInfo):
    """update the third eval info according the web page show.show the data.

        so we need pull all data in list ,make them flat to show in the page.so in the page, the show will be easy.
        TODO: in future, we need create the function according the config data.2017.10.30.  这个函数感觉也有点多余，要简化.
    """
    logger = getLogger()
    try:
        logger.debug("start flat third eval Info .")

        if inThirdEvalInfo is None:
            return None

        # we only get the message we needed:
        #change the list to flat data.
        localThirdEvalInfo = inThirdEvalInfo

        #basic_page 基本信息
        configPageUsing = configPage['basic_page']
        item = localThirdEvalInfo["basic"]
        addDictItemValue(item,'BASIC_NAME',localThirdEvalInfo,configPageUsing['name']['dataName'])
        addDictItemValue(item,'BASIC_SEX',localThirdEvalInfo,configPageUsing['sex']['dataName'])

        #third_page 第三方评估
        configPageUsing = configPage['third_page']
        item = localThirdEvalInfo["third"]
        addDictItemValue(item,'NORMAL_ADL',localThirdEvalInfo,configPageUsing['normal_adl']['dataName'])
        addDictItemValue(item,'NORMAL_IADL',localThirdEvalInfo,configPageUsing['normal_iadl']['dataName'])
        addDictItemValue(item,'NORMAL_RECOGNIZE',localThirdEvalInfo,configPageUsing['normal_recognize']['dataName'])
        addDictItemValue(item,'THIRDEVAL_CLASS',localThirdEvalInfo,configPageUsing['thirdeval_class']['dataName'])

        #leer_page 乐尔之家评估
        configPageUsing = configPage['leer_page']
        item = localThirdEvalInfo["leer"]
        addDictItemValue(item,"LEER_NORMAL_ADL",localThirdEvalInfo,configPageUsing['normal_adl']['dataName'])
        addDictItemValue(item,"LEER_SPIRIT_DEPRESS",localThirdEvalInfo,configPageUsing['spirit_depress']['dataName'])
        addDictItemValue(item,"LEER_FEEL_SOUL",localThirdEvalInfo,configPageUsing['feel_soul']['dataName'])
        addDictItemValue(item,"LEER_CLASS",localThirdEvalInfo,configPageUsing['leer_class']['dataName'])

        logger.debug("update localOrderInfo success.")

        return localThirdEvalInfo
    except:
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
    finally:
        pass

def zipOrderInfoOrder(inOrderInfo):
    """update the order info according the web page show.post the data.

        so we need pull all data in form ,make them zip to post in the page.
        2017.10.30. 这个函数感觉有点多余啊。
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

def postThirdEvalInfo(storageData):
    logger = getLogger()
    try:
        logger.debug("start PUT Order Info according contact id.")

        jsonData = json.dumps(storageData)
        dictData = json.loads(jsonData)

        # save data to sqlite db.
        import web
        import sqlite3
        dbSqlite = web.database(dbn='sqlite',db='thirdeval.s3db')

        thirdevalid = 0
        if dictData is not None:
            thirdevalid = dbSqlite.insert('thirdeval_detail',
                                 basic_name=dictData['BASIC_NAME'],
                                 basic_sex=dictData['BASIC_SEX'],
                                 third_normal_adl=dictData['NORMAL_ADL'],
                                 third_normal_iadl=dictData['NORMAL_IADL'],
                                 third_normal_recognize=dictData['NORMAL_RECOGNIZE'],
                                 thirdeval_class=dictData['THIRDEVAL_CLASS'],
                                 leer_normal_adl=dictData['LEER_NORMAL_ADL'],
                                 leer_spirit_depress=dictData['LEER_SPIRIT_DEPRESS'],
                                 leer_feel_soul=dictData['LEER_FEEL_SOUL'],
                                 leer_class=dictData['LEER_CLASS']
                                 )
        else:
            pass

        if thirdevalid is 0:
            pass
        else:
            logger.debug("save the third eval info success.")



        retStr = {"RETURNFLAG":True,"OrderID":thirdevalid}

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
        logger = getLogger()
        try:
            logger.debug("start PUT Order Info according contact id.")

            jsonData = json.dumps(storageData)
            dictData = json.loads(jsonData)

            retStr = {"RETURNFLAG":True,"OrderID":1}

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
        finally:
            pass

