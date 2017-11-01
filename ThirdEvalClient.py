#!/usr/bin/env python
# coding=utf8
__author__ = 'stone'

import cStringIO
import json

import traceback
from configData import getConfig
from logHelper import getLogger
from ThirdEvalDomainHandler import flatThirdEvalInfo

from configObjData import getConfigPage

configPage = getConfigPage()

def getThirdEvalInfo(inOrderid):
    """
        get the third eval info from DB
        now, we simulate some json data.
    """
    logger = getLogger()
    try:
        logger.debug("start GET Order Info according order id.")

        if inOrderid is None:
            return None

        #from db to get the data.
        import web
        import sqlite3
        dbSqlite = web.database(dbn='sqlite',db='thirdeval.s3db')

        myvar = dict(id=inOrderid)
        results = dbSqlite.select('thirdeval_detail', myvar, where="id = $id")

        for item in results:
            localOrderInfo = {
                "basic":{
                 "BASIC_NAME":item['basic_name'],
                 "BASIC_SEX":item['basic_sex'],
                },
                "third":{
                "NORMAL_ADL":item['third_normal_adl'],
                "NORMAL_IADL":item['third_normal_iadl'],
                "NORMAL_RECOGNIZE":item['third_normal_recognize'],
                "THIRDEVAL_CLASS":item['thirdeval_class']
            },
                              "leer":{
                                  "LEER_NORMAL_ADL":item['leer_normal_adl'],
                                  "LEER_SPIRIT_DEPRESS":item['leer_spirit_depress'],
                                  "LEER_FEEL_SOUL":item['leer_feel_soul'],
                                  "LEER_CLASS":item['leer_class']
                              }
                              }

        logger.debug("get localOrderInfo success.")

        #we need change the data structure, so the html show simple.
        if localOrderInfo is not None:
            localOrderInfo = flatThirdEvalInfo(localOrderInfo)

        return localOrderInfo
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

def getThirdEvalInfoLst(inOrderid,inPageIndex):
    logger = getLogger()
    try:
        logger.debug("start GET ThirdEval Info according query condition.")

        localURL = ''

        #from db to get the data.
        import web
        import sqlite3
        dbSqlite = web.database(dbn='sqlite',db='thirdeval.s3db')

        if inOrderid is None:
            results = dbSqlite.select('thirdeval_detail')
            inOrderid = ''
            for item in results:
               localThirdEvalInfoLst = {"ThirdEvalInfoLst":[{'orderid':item['id'],
                                                              'name':item['basic_name'],
                                                              'normal_adl':item['third_normal_adl'],
                                                              'thirdeval_class':item['thirdeval_class'],
                                                              'leer_normal_adl':item['leer_normal_adl'],
                                                              'leer_class':item['leer_class']}],
                             "PageManager":{
                                 "DataCount":5,
                                 "PageSize":5,
                                 "PageCount":1,
                                 "PageIndex":1,
                             }
                             }

        if inOrderid != '':
            myvar = dict(id=inOrderid)
            results = dbSqlite.select('thirdeval_detail', myvar, where="id = $id")

            for item in results:
               localThirdEvalInfoLst = {"ThirdEvalInfoLst":[{'orderid':inOrderid,
                                                              'name':item['basic_name'],
                                                              'normal_adl':item['third_normal_adl'],
                                                              'thirdeval_class':item['thirdeval_class'],
                                                              'leer_normal_adl':item['leer_normal_adl'],
                                                              'leer_class':item['leer_class']}],
                             "PageManager":{
                                 "DataCount":5,
                                 "PageSize":5,
                                 "PageCount":1,
                                 "PageIndex":1,
                             }
                             }

        logger.debug("get localThirdEvalInfoLst List success.")

        return localThirdEvalInfoLst
    except :
        logger.error("exception occur, see the traceback.log")

        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()

    finally:
        pass

def addItemDictValue(dstDict,dstName,srcDict,srcName):
    """add value data from srcDict to dstDict .from dic to item data."""

    localVal = srcDict.pop(srcName)
    upDict = {dstName:localVal}
    dstDict.update(upDict)

