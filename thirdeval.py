#!/usr/bin/env python
# coding=utf8
__author__ = 'stone'
#2017.10.29.    add for test the third eval program.
import web
from web.contrib.template import render_mako

import configData
from configData import getConfig
from logHelper import getLogger
import traceback

import re
import base64

import json

import urlparse
import ThirdEvalDomainHandler

web.config.debug = False

urls = (
        '/thirdeval','thirdeval',
        '/thirdevalList','thirdevalList'
        )

app = web.application(urls,globals(),autoreload=True)

# input_encoding and output_encoding is important for unicode
# template file. Reference:
# http://www.makotemplates.org/docs/documentation.html#unicode
render = render_mako(
        directories = ['templates'],
        input_encoding = 'utf-8',
        output_encoding = 'utf-8',
        )

class thirdevalList:
    def GET(self):
        logger = getLogger()
        try:
            logger.debug("start thirdevalList Page GET response")

            parsed_url = urlparse.urlparse(web.ctx.fullpath)
            query_url = parsed_url.query
            if (query_url != ''):
                query_dict = dict(urlparse.parse_qsl(query_url))

                if 'orderid' in query_dict:
                    orderid = query_dict['orderid']
                else:
                    orderid = None

                if 'pageindex' in query_dict:
                    pageindex = query_dict['pageindex']
                else:
                    pageindex = None

                return render.thirdevalList(orderid=orderid,pageindex=pageindex)
            else:
                orderid = None
                pageindex  = None
                return render.thirdevalList(orderid=orderid,pageindex=pageindex)
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

class thirdeval:
    def POST(self):
        logger = getLogger()
        try:
            logger.debug("start Order Page POST response")

            #get POST form data
            data = web.input()

            retStr = ThirdEvalDomainHandler.postThirdEvalInfo(data)

            if retStr is None:
                return render.error(error = 'add failure.')

            #according the response
            #retDict = json.loads(retStr)
            retDict = retStr
            if (retDict["RETURNFLAG"] == True):
                #refresh the order.
                orderidStr = retDict["OrderID"]
                return render.thirdeval(orderid = orderidStr)
            else:
                return render.error(error = 'add failure.')
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

    def GET(self):
        logger = getLogger()
        try:
            logger.debug("start thirdval Page GET response")

            parsed_url = urlparse.urlparse(web.ctx.fullpath)
            query_url = parsed_url.query
            query_url = query_url.encode('utf-8')
            if (query_url != ''):
                query_dict = dict(urlparse.parse_qsl(query_url))

                if 'orderid' in query_dict:
                    orderid = query_dict['orderid']
                    return render.thirdeval(orderid = orderid,queryDict = query_dict)
                else:
                    #if no orderid, according the query_dict to show a file.
                    orderid = None
                    return render.thirdeval(orderid = orderid,queryDict = query_dict)
            else:
                #if no querey string.  show blank file
                orderid = None
                query_dict = None
                return render.thirdeval(orderid = orderid,queryDict = query_dict)
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

if __name__ == "__main__":
    app.run()

