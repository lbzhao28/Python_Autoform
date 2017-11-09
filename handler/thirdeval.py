#!/usr/bin/env python
# coding=utf8
""" the entrance for third eval handler.

# prerequisite:
    1.  based on Python 3.5.x

# usage:
    1)  the url route for autoform
    2)  the handler entrance for autoform

# other:
    None

"""

from lib.route import route
import logging
import json
from handler import BaseHandler
from domain.ThirdEvalDomainHandler import postThirdEvalInfo
import configObjData
from configObjData import getConfigPage

@route(r'/thirdevalList', name='thirdevalList') #第三方评估列表页面
class ThirdevalListHandler(BaseHandler):
    """ third eval list.
    """
    loggerRoot = logging.getLogger('root')
    def check_xsrf_cookie(self):
        """
        rest api do not check the xsrf.
        :return:
        """
        pass

    def get(self):
        try:
            self.loggerRoot.debug("start thirdevalList Page GET response")

            orderid = self.get_argument("orderid",None)
            query_dict = self.get_arguments()


            pageindex = self.get_argument("pageindex",None)

            self.render("thirdevalList.html",orderid = orderid,pageindex=pageindex)
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

@route(r'/thirdeval', name='thirdeval') #第三方评估录入页面
class ThirdevalHandler(BaseHandler):
    """ third eval.
    """
    loggerRoot = logging.getLogger('root')
    def check_xsrf_cookie(self):
        """
        rest api do not check the xsrf.
        :return:
        """
        pass

    def get(self):
        try:
            self.loggerRoot.info("start thirdeval get API.")
            #if no querey string.  show blank file
            orderid = None
            query_dict = None

            orderid = self.get_argument("orderid",None)
            query_dict = self.get_arguments()

            #get the config data
            configPage = getConfigPage()

            #render the page.
            self.render("thirdeval.html",orderid = orderid,queryDict = query_dict)

        except Exception as ex:
            logging.error(ex)
        finally:
            pass

    def post(self):
        try:
            self.loggerRoot.info("start thirdeval post API.")

            data = self.get_arguments()

            retStr = postThirdEvalInfo(data)

            if retStr is None:
                self.write('add failure.')

            #according the response
            #retDict = json.loads(retStr)
            retDict = retStr
            if (retDict["RETURNFLAG"] == True):
                #refresh the order.
                orderidStr = retDict["OrderID"]
                self.render("thirdeval.html",orderid = orderidStr)
            else:
                self.write('add failure.')
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

