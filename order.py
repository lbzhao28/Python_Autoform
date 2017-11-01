#!/usr/bin/env python
# coding=utf8
__author__ = 'stone'
import web
from web.contrib.template import render_mako

import globalDefine
import traceback
import configData
from configData import getConfig
from logHelper import getLogger

import re
import base64

import json

import urlparse
import OrderDomainHandler

web.config.debug = False

urls = (
        '/login/(.*)/(.*)/(.*)','login',
        '/order/(.*)','order',
        '/orderTemp/(.*)','orderTemp',
        '/orderProduct','orderProduct',
        '/orderUpdate/(.*)/(.*)','orderUpdate',
        '/orderUpdateTemp/(.*)/(.*)','orderUpdateTemp',
        '/orderStatusUpdate/(.*)/(.*)/(.*)','orderStatusUpdate',
        '/orderList/(.*)/(.*)','orderList'
        )

app = web.application(urls,globals(),autoreload=True)
session = web.session.Session(app,web.session.DiskStore('sessions'),
initializer={'session_grpid':'','session_usrid':'','session_loginned':'','session_pwd':''})

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

allowed = (
    (getConfig('allowedUser1','UserName','str'),getConfig('allowedUser1','Password','str')),
    (getConfig('allowedUser2','UserName','str'),getConfig('allowedUser2','Password','str'))
    )

# input_encoding and output_encoding is important for unicode
# template file. Reference:
# http://www.makotemplates.org/docs/documentation.html#unicode
render = render_mako(
        directories = ['templates'],
        input_encoding = 'utf-8',
        output_encoding = 'utf-8',
        )

class orderList:
    def GET(self,session_usr,session_grpid):
        try:
            logger = getLogger()
            logger.debug("start OrderList Page GET response")

            web.ctx.session.session_usrid =  session_usr
            web.ctx.session.session_grpid =  session_grpid

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
#            authreq = checkUserAuth(web)
#
#            if authreq:
#                web.header('WWW-Authenticate','Basic realm="Auth example"')
#                web.ctx.status = '401 Unauthorized'
#                logger.debug("no right HTTP_AUTHORIZATION")
#                return render.error(error = web.ctx.status)

            parsed_url = urlparse.urlparse(web.ctx.fullpath)
            query_url = parsed_url.query
            if (query_url != ''):
                query_dict = dict(urlparse.parse_qsl(query_url))

                if 'ROLE' in query_dict:
                    role = str(query_dict['ROLE'])
                else:
                    role = None
                web.ctx.session.session_role =  role

                if 'GRPID' in query_dict:
                    grpid = query_dict['GRPID']
                else:
                    grpid = None

                if 'CRUSR' in query_dict:
                    crusr = query_dict['CRUSR']
                else:
                    crusr = None

                if 'STARTDT' in query_dict:
                    startdt = query_dict['STARTDT']
                else:
                    startdt = None

                if 'ENDDT' in query_dict:
                    enddt = query_dict['ENDDT']
                else:
                    enddt = None

                if 'ORDERSTATUS' in query_dict:
                    orderstatus = query_dict['ORDERSTATUS']
                    #special for show all ,do not judge orderstatus.
                    if orderstatus == 'SHOWALL':
                        orderstatus = None
                else:
                    orderstatus = None

                if 'CONTACTID' in query_dict:
                    contactid = query_dict['CONTACTID']
                else:
                    contactid = None

                if 'ORDERID' in query_dict:
                    orderid = query_dict['ORDERID']
                else:
                    orderid = None

                if 'PAGEINDEX' in query_dict:
                    pageindex = query_dict['PAGEINDEX']
                else:
                    pageindex = None

                return render.orderList(session_usr=session_usr,session_grpid =  session_grpid,grpid=grpid,crusr=crusr,contactid = contactid,orderid=orderid,orderstatus=orderstatus,startdt=startdt,enddt=enddt,pageindex=pageindex,outrole=role)
            else:
                grpid = None
                crusr = None
                contactid = None
                orderid = None
                startdt = None
                enddt = None
                orderstatus = None
                pageindex  = None
                role = None
                return render.orderList(session_usr=session_usr,session_grpid =  session_grpid,grpid=grpid,crusr=crusr,contactid = contactid,orderid=orderid,orderstatus=orderstatus,startdt=startdt,enddt=enddt,pageindex=pageindex,outrole=role)
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

class orderProduct:
    def GET(self):
        try:
            logger = getLogger()
            logger.debug("start OrderProduct Page GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
            #            authreq = checkUserAuth(web)
            #
            #            if authreq:
            #                web.header('WWW-Authenticate','Basic realm="Auth example"')
            #                web.ctx.status = '401 Unauthorized'
            #                logger.debug("no right HTTP_AUTHORIZATION")
            #                return render.error(error = web.ctx.status)

            parsed_url = urlparse.urlparse(web.ctx.fullpath)
            query_url = parsed_url.query
            if (query_url != ''):
                query_dict = dict(urlparse.parse_qsl(query_url))

                if 'INSURANCECODE' in query_dict:
                    insurancecodeid = query_dict['INSURANCECODE']
                else:
                    insurancecodeid = None

                if 'SECURITYPLAN' in query_dict:
                    securityplanid = query_dict['SECURITYPLAN']
                else:
                    securityplanid = None

                if 'PREMIUMPLAN' in query_dict:
                    premiumplanid = query_dict['PREMIUMPLAN']
                else:
                    premiumplanid = None

                if 'AGEPLAN' in query_dict:
                    ageplan = query_dict['AGEPLAN']
                else:
                    ageplan = None

                return render.orderProduct(insurancecodeid = insurancecodeid,securityplanid=securityplanid,premiumplanid=premiumplanid,ageplan=ageplan)
            else:
                insurancecodeid = None
                securityplanid = None
                premiumplanid = None
                ageplan = None
                return render.orderProduct(insurancecodeid = insurancecodeid,securityplanid=securityplanid,premiumplanid=premiumplanid,ageplan=ageplan)
        except :
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

#in JS, can not use put directly, so we use POST　to simulate it.
class orderUpdate:
    def POST(self,contactid,orderid):
        try:
            logger = getLogger()
            logger.debug("start Order Update POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
#            authreq = checkUserAuth(web)
#
#            if authreq:
#                web.header('WWW-Authenticate','Basic realm="Auth example"')
#                web.ctx.status = '401 Unauthorized'
#                logger.debug("no right HTTP_AUTHORIZATION")
#                return render.error(error = web.ctx.status)

            if orderid is None:
                return render.error(error = 'no orderid')
            else:
                #get POST form data
                data = web.input()
                #call REST post data
                #TODO: 1 待审核订单
                status = '1'
                retStr = OrderDomainHandler.putOrderInfoContact(orderid,data,status,web.ctx.session.session_usrid)

                #according the response

                if retStr is None:
                    return render.error(error = 'update failure!')

                retDict = json.loads(retStr)
                if (retDict["RETURNFLAG"] == True):
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderid,outrole = role)
                else:
                    return render.error(error = 'update failure!')

        except :
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

#in JS, can not use put directly, so we use POST　to simulate it.
class orderUpdateTemp:
    def POST(self,contactid,orderid):
        try:
            logger = getLogger()
            logger.debug("start Order Update Temp POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
            #            authreq = checkUserAuth(web)
            #
            #            if authreq:
            #                web.header('WWW-Authenticate','Basic realm="Auth example"')
            #                web.ctx.status = '401 Unauthorized'
            #                logger.debug("no right HTTP_AUTHORIZATION")
            #                return render.error(error = web.ctx.status)

            if orderid is None:
                return render.error(error = 'no orderid')
            else:
                #get POST form data
                data = web.input()
                #call REST post data
                #TODO: 6 means 暂存订单
                status = '6'
                retStr = OrderDomainHandler.putOrderInfoContact(orderid,data,status,web.ctx.session.session_usrid)

                #according the response
                if retStr is None:
                    return render.error(error = 'update failure!')

                retDict = json.loads(retStr)
                if (retDict["RETURNFLAG"] == True):
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderid,outrole = role)
                else:
                    return render.error(error = 'update failure!')

        except :
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

#in JS, can not use put directly, so we use POST　to simulate it.
class orderStatusUpdate:
    def POST(self,contactid,orderid,status):
        try:
            logger = getLogger()
            logger.debug("start Order Status Update POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
#            authreq = checkUserAuth(web)
#
#            if authreq:
#                web.header('WWW-Authenticate','Basic realm="Auth example"')
#                web.ctx.status = '401 Unauthorized'
#                logger.debug("no right HTTP_AUTHORIZATION")
#                return render.error(error = web.ctx.status)

            if orderid is None:
                return render.error(error = 'no orderid')
            else:
                #get POST form data
                data = web.input()
                #call REST post data
                retStr = OrderDomainHandler.putOrderStatusInfoContact(orderid,status,data,web.ctx.session.session_usrid)

                #according the response
                if retStr is None:
                    return render.error(error = 'update failure!')

                retDict = json.loads(retStr)
                if (retDict["RETURNFLAG"] == True):
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderid,outrole=role)
                else:
                    return render.error(error = 'update failure!')

        except :
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

class login:
    def POST(self):
        try:
            logger = getLogger()
            logger.debug("start login POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

        except :
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

    def GET(self,page,usrid,pwd):
        try:
            logger = getLogger()
            logger.debug("start login GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO:传过来的usrid和pwd要是加密的.未来完成权限的取得.
            #如何加密usrid,pwd

            #连接逻辑层验证用户信息.
            retDict = OrderDomainHandler.getUsrPurview(usrid,pwd)

            if (retDict["right"] is True):
                #保存用户信息到session里面
                web.ctx.session.session_loginned = True
                web.ctx.session.session_usrid = usrid
                return retDict
                pass
            else:
                return render.error(error = retDict["log"])

            #如何跳转登录到其它页面?传入页面的参数.

            #直接登录其它页面是需要登录信息的.

        except :
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

class orderTemp:
    def POST(self,contactid):
        try:
            logger = getLogger()
            logger.debug("start Order Temp Page POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
            #            authreq = checkUserAuth(web)
            #
            #            if authreq:
            #                web.header('WWW-Authenticate','Basic realm="Auth example"')
            #                web.ctx.status = '401 Unauthorized'
            #                logger.debug("no right HTTP_AUTHORIZATION")
            #                return render.error(error = web.ctx.status)

            if contactid is None:
                return render.error(error = 'no contactid')
            else:
                #get POST form data
                data = web.input()
                #call REST post data
                #TODO: 6 means 暂存订单
                status = '6'
                retStr = OrderDomainHandler.postOrderInfoContact(contactid,data,status,web.ctx.session.session_usrid,web.ctx.session.session_grpid)

                if retStr is None:
                    return render.error(error = 'add failure.')

                #according the response
                retDict = json.loads(retStr)
                if (retDict["RETURNFLAG"] == True):
                    #refresh the order.
                    orderidStr = retDict["OrderID"]
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderidStr,outrole = role)
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
        else:
            pass
        finally:
            pass

    def GET(self,contactid):
    #must have contactid, otherwise,the data will be wrong.
        try:
            logger = getLogger()
            logger.debug("start Order Temp Page GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
            #            authreq = checkUserAuth(web)
            #
            #            if authreq:
            #                web.header('WWW-Authenticate','Basic realm="Auth example"')
            #                web.ctx.status = '401 Unauthorized'
            #                logger.debug("no right HTTP_AUTHORIZATION")
            #                return render.error(error = web.ctx.status)

            if contactid is None:
                return render.error(error = 'no contactid')
            else:
                #if has orderid according the orderid to get the order info.
                #query_dict = dict(urlparse.parse_qsl(web.ctx.env['QUERY_STRING']))
                parsed_url = urlparse.urlparse(web.ctx.fullpath)
                query_url = parsed_url.query
                query_url = query_url.encode('utf-8')
                if (query_url != ''):
                    query_dict = dict(urlparse.parse_qsl(query_url))

                    if 'orderid' in query_dict:
                        orderid = query_dict['orderid']
                        role = web.ctx.session.session_role;
                        return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole = role)
                    else:
                        #if no orderid, according the query_dict to show a file.
                        orderid = None
                        role = web.ctx.session.session_role;
                        return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole = role)
                else:
                    #if no querey string.  show blank file
                    orderid = None
                    query_dict = None
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole = role)
        except :
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


class order:
    def POST(self,contactid):
        try:
            logger = getLogger()
            logger.debug("start Order Page POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
#            authreq = checkUserAuth(web)
#
#            if authreq:
#                web.header('WWW-Authenticate','Basic realm="Auth example"')
#                web.ctx.status = '401 Unauthorized'
#                logger.debug("no right HTTP_AUTHORIZATION")
#                return render.error(error = web.ctx.status)

            if contactid is None:
                return render.error(error = 'no contactid')
            else:
                #get POST form data
                data = web.input()
                #call REST post data
                #TODO: 1 means 待审核订单
                status = '1'

                retStr = OrderDomainHandler.postOrderInfoContact(contactid,data,status,web.ctx.session.session_usrid,web.ctx.session.session_grpid)

                if retStr is None:
                    return render.error(error = 'add failure.')

                #according the response
                retDict = json.loads(retStr)
                if (retDict["RETURNFLAG"] == True):
                    #refresh the order.
                    orderidStr = retDict["OrderID"]
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderidStr,outrole = role)
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
        else:
            pass
        finally:
            pass

    def GET(self,contactid):
    #must have contactid, otherwise,the data will be wrong.
        try:
            logger = getLogger()
            logger.debug("start Order Page GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            #TODO: open the auth in future.also need purview.
#            authreq = checkUserAuth(web)
#
#            if authreq:
#                web.header('WWW-Authenticate','Basic realm="Auth example"')
#                web.ctx.status = '401 Unauthorized'
#                logger.debug("no right HTTP_AUTHORIZATION")
#                return render.error(error = web.ctx.status)

            if contactid is None:
                return render.error(error = 'no contactid')
            else:
                #if has orderid according the orderid to get the order info.
                #query_dict = dict(urlparse.parse_qsl(web.ctx.env['QUERY_STRING']))
                parsed_url = urlparse.urlparse(web.ctx.fullpath)
                query_url = parsed_url.query
                query_url = query_url.encode('utf-8')
                if (query_url != ''):
                    query_dict = dict(urlparse.parse_qsl(query_url))


                    if 'orderid' in query_dict:
                        orderid = query_dict['orderid']
                        role = web.ctx.session.session_role;
                        return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole =role)
                    else:
                        #if no orderid, according the query_dict to show a file.
                        orderid = None
                        role = web.ctx.session.session_role;
                        return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole = role)
                else:
                    #if no querey string.  show blank file
                    orderid = None
                    query_dict = None
                    role = web.ctx.session.session_role;
                    return render.order(contactid = contactid,orderid = orderid,queryDict = query_dict,outrole =role)
        except :
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

def checkUserAuth(inWeb):
    logger = getLogger()
    auth = inWeb.ctx.env.get('HTTP_AUTHORIZATION')
    authreq = False
    if auth is None:
        authreq = True
    else:
        auth = re.sub('^Basic ','',auth)
        username,password = base64.decodestring(auth).split(':')
        if (username,password) in allowed:
            logger.debug("has right HTTP_AUTHORIZATION")
            pass
        else:
            authreq = True
    return authreq

if __name__ == "__main__":
    app.run()
