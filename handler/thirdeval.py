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
            self.render("thirdeval.html",orderid = orderid,queryDict = query_dict)
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

    def post(self):
        try:
            self.loggerRoot.info("start thirdeval post API.")

            data = self.get_arguments()

            retStr = ThirdEvalDomainHandler.postThirdEvalInfo(data)

            if retStr is None:
                self.write('add failure.')

            #according the response
            #retDict = json.loads(retStr)
            retDict = retStr
            if (retDict["RETURNFLAG"] == True):
                #refresh the order.
                orderidStr = retDict["OrderID"]
                self.render("thirdeval.html",orderid = orderid)
            else:
                self.write('add failure.')
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

