#-*- coding: utf-8 -*-
""" the helper package for REST client resource.
"""
__author__ = 'stone'

import logging
import json
import pycurl
import io
from common.Cmn import switch
from common.Cmn import dict2querystring

class RESTClientHelper():
    """a class to help for client to call REST web resource"""
    loggerRoot = logging.getLogger('root')
    def __init__(self):
        self.loggerRoot.debug("init RESTClientHelper.")

    def callWebService(self,method=None,url=None,inparaQueryString=None,actualParaQueryString=None,actualParaJson=None,retry=0):
        """ call web service for REST..

        retry default is :0.do not retry
        """
        try:
            self.loggerRoot.debug("start call web service for  REST.")

            retinfo = None
            i=0
            for i in range(0,int(retry)+1) :
                if len(actualParaQueryString)!=len(inparaQueryString):
                    raise TypeError

                localURL = str(url)

                #add  querystring parameters
                localURLDict = {}
                for item in inparaQueryString:
                    updateDict={inparaQueryString[item]['name']:actualParaQueryString[inparaQueryString[item]['name']]}
                    localURLDict.update(updateDict)

                localURL += dict2querystring(localURLDict)

                c = pycurl.Curl()
                buf = io.StringIO() #define in function.

                for case in switch(method):
                    if case('GET'):
                        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
                        c.setopt(pycurl.URL,localURL)
                        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json'])
                        c.setopt(c.WRITEFUNCTION, buf.write)
                        c.setopt(c.SSL_VERIFYPEER, False)
                        c.setopt(c.SSL_VERIFYHOST, False)
                        c.setopt(c.VERBOSE, True)
                        c.perform()
                        http_code = c.getinfo(pycurl.HTTP_CODE)
                        if http_code != 200:
                            return None
                        else:
                            retinfo = json.loads(buf.getvalue())

                        self.loggerRoot.debug("the retinfo is : %s.",str(retinfo))

                        if 'errcode' not in retinfo:
                            #no error do not retry.
                            buf.close()
                            c.close()
                            self.loggerRoot.debug("get wechat API success.")
                            return retinfo
                        else:
                            buf.close()
                            c.close()
                            self.loggerRoot.error("get wechat API failure.")
                            return None
                        break
                    if case('POST'):
                        c.setopt(pycurl.URL,localURL)
                        actualParaJsonStr = json.dumps(actualParaJson)
                        actualParaJsonStr =  str(actualParaJsonStr.decode("unicode_escape"))
                        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(actualParaJsonStr))])
                        c.setopt(c.VERBOSE, True)
                        c.setopt(pycurl.CUSTOMREQUEST,"POST")
                        c.setopt(c.POSTFIELDS,actualParaJsonStr)
                        c.setopt(c.WRITEFUNCTION,buf.write)
                        c.setopt(c.SSL_VERIFYPEER, False)
                        c.setopt(c.SSL_VERIFYHOST, False)
                        #c.setopt(pycurl.USERPWD,getConfig('allowedUser1','UserName','str')+':'+getConfig('allowedUser1','Password','str'))
                        c.perform()

                        http_code = c.getinfo(pycurl.HTTP_CODE)
                        #judge post success.
                        #TODO:why return 200?
                        if http_code != 200:
                            return None
                        else:
                            retinfo = json.loads(buf.getvalue())

                        self.loggerRoot.debug("the retinfo is : %s.",str(retinfo))

                        if 'errcode' not in retinfo:
                            #no error do not retry.
                            buf.close()
                            c.close()
                            self.loggerRoot.debug("post wechat API success.")
                            return retinfo
                        else:
                            if retinfo['errcode'] == int(WechatReturnEnum.SUCCESS):
                                #no error do not retry.
                                buf.close()
                                c.close()
                                self.loggerRoot.debug("post wechat API success.the message is : %s.",retinfo['errmsg'])
                                return retinfo
                            else:
                                buf.close()
                                c.close()
                                self.loggerRoot.error("post wechat API failure. the error code is : %s,the error message is : %s.",str(retinfo['errcode']),retinfo['errmsg'])
                                return retinfo
                        break
                    if case():  # default, could also just omit condition or 'if True'
                        pass
                i+=1
            return retinfo
        except:
            pass
        finally:
            pass

