# -*- coding: utf-8 -*-
"""the common handler for python packages
"""
__author__ = 'Long'

import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import py
import uuid
import pycurl
try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO
import json
import math
import logging
from common.Cfg import Config
import time
import datetime
import decimal
import xml.dom.minidom
from xml.dom import *
from  xml.dom.minidom import *
import types
import re
import functools

cfg = Config(filename="config4service.conf")


def dict2querystring(indict):
    """
    convert dictionary to querystring
    for example:{'name':name} convert to
    ?name=name
    """
    loggerRoot = logging.getLogger('root')
    try:
        loggerRoot.debug("start dictionary 2 querystring.")
        localURL = ''
        l = list()
        for p in indict:
            l.append(str(p) + "=" + str(indict[p]))
        u = "&".join(l)
        if len(u) > 0:
            localURL = localURL + "?" + u
        return localURL
    except pycurl.error as e:
        loggerRoot.error("exception occur, the error message is: %s.", e)
    finally:
        pass


def convertDictLst2Dict(inDictLst):
    """convert the dictionary list to dictionary.

    only accept 1 row list dictionary.
    inDictLst   -> input dictionary list.
    return dictionary arguments.
    """
    retDict = {}
    if not isinstance(inDictLst, dict):
        return retDict
    for item in inDictLst:
        if len(inDictLst[item]) > 1:
            return retDict
        else:
            retDict.update({item: inDictLst[item][0]})

    return retDict


def timestamp_datetime(value):
    """convert the timestamp to datetime.

    """
    format = '%Y-%m-%d %H:%M:%S'
    # value:1332888820
    value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # strftime to transfer.
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    """convert datetime to timestamp.

    """
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    #将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def DataMapping(para={}, md={}):
    """map the data and md

        Keyword arguments:
        para -- parameters
        md  -- {key:para,value:mapping}
    """
    d = dict()
    for p in para:
        if p in md:
            d[md[p]] = para.get(p)
    return d


def SendRequest(method="GET", url=None, para={}):
    """call pycurl to call REST web service"""
    try:
        buf = io.StringIO()
        c = pycurl.Curl()
        if method == "GET":
            l = list()
            for p in para:
                l.append(str(p) + "=" + str(para[p]))
            u = "&".join(l)
            if len(u) > 0:
                url = url + "?" + u
            c.setopt(pycurl.CUSTOMREQUEST, method)
        else:
            postData = json.dumps(para)
            if len(para) > 0:
                c.setopt(pycurl.POSTFIELDS, postData)
            c.setopt(pycurl.CUSTOMREQUEST, method)
            c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Content-Length: ' + str(len(postData))])
        c.setopt(pycurl.URL, str(url))
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.VERBOSE, True)
        c.perform()
        http_code = c.getinfo(pycurl.HTTP_CODE)
        if http_code != 200:
            retinfo = {"code": -1, "message": "SendRequest fail,url: %s,para: %s" % (url, str(para))}
        else:
            retinfo = json.loads(buf.getvalue())
    except Exception as e:
        logging.error("SendRequest GET->exception occur,error:[%s]" % e)
        retinfo = {"code": -1, "message": e}
    finally:
        return retinfo


def xml_node_to_dict(node):
    """ convert XML node to dict

    """
    out = {}
    if node.nodeType != Node.ELEMENT_NODE:
        return None
    for item in node.childNodes:
        if item.nodeType == Node.TEXT_NODE or item.nodeType == Node.CDATA_SECTION_NODE:
            if node.childNodes.length == 1:
                return item.nodeValue.encode('utf-8')
            else:
                continue
        if item.nodeType != Node.ELEMENT_NODE:
            continue
        temp_data = xml_node_to_dict(item)
        if out.has_key(item.tagName):
            if type(out[item.tagName]) == types.ListType:
                out[item.tagName].append(temp_data)
            else:
                out[item.tagName] = [out[item.tagName], temp_data]
        else:
            out[item.tagName] = temp_data
    return out


def xml_to_dict(str_xml):
    """ convert xml file to dictionary

    """
    loggerRoot = logging.getLogger('root')
    loggerRoot.debug("start dictionary 2 querystring.")
    try:
        dom = parseString(str_xml)
    except Exception as e:
        loggerRoot.error("exception occur, the error message is: %s.", e)
        return None
    root = dom.documentElement
    return {root.tagName: xml_node_to_dict(root)}


class DateTimeEncoder(json.JSONEncoder):
    """
    a class to encode date time format.
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(obj, datetime.date):
            return obj.strftime(self.DATE_FORMAT)
        elif isinstance(obj, datetime.time):
            return obj.strftime(self.TIME_FORMAT)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        # TODO: I can not read all source for json, so I do not confirm need this json.JSONEncoder.default(self,obj).
        else:
            return json.JSONEncoder.default(self, obj)

class UuidEncoder(json.JSONEncoder):
    """
    a class to encode uuid format.
    """

    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            localStr = str(obj)
            # TODO: now directly return uuid string, maybe in future, return detai data.
            # according the info from this file: Converting a UUID to a string with str() yields something in the form
            # '12345678-1234-1234-1234-123456789abc'.
            return localStr
        # TODO: I can not read all source for json, so I do not confirm need this json.JSONEncoder.default(self,obj).
        else:
            return json.JSONEncoder.default(self, obj)

class ORMSectionEnum:
    """ the Enum for ORM sections, all used in code_conf config file.

    """
    allEnum = (ConDetail, RetDetail, ParaDetail) = ('conditionDetail', 'resultDetail', 'paraDetail')


class RESTEnum:
    """ the Enum for REST, all used in code_conf config file.

    """
    allRESTEnum = (GET, POST, PUT, DELETE) = ('get', 'post', 'put', 'delete')


class SQLStatusEnum:
    """ the Enum for sql status, the sql text execute status.

    """
    allSQLStatusEnum = (NOTREADY, READY, SUCCESS, FAILURE) = ('notready', 'ready', 'success', 'failure')


class WechatMessasgeModeEnum:
    """ the Enum for wechat message mode.

    """
    allMessageEnum = (INSTANT, ASYNC) = ('instant', 'async')


class WechatMessasgeTypeEnum:
    """ the Enum for wechat message type.

    """
    allMessageTypeEnum = (TEXT, IMAGE, PROCESS, INSTANTPROCESS, CS) = (
        'text', 'image', 'process', 'instantprocess', 'transfer_customer_service')


class WechatApiEnum:
    """ the Enum for wechat API now supported.

    """
    allAPIEnum = (
        USERLIST, USERINFO, ACCESSTOKEN, CSTEXT, MESSAGEHIS, SCODE, GETSCODEPIC, GENMENU, GENGROUP, BATCHUPDATEUSER,
        TESTWHITELIST, CREATECARD, GET_MATERIALCOUNT, GET_MATERIAL, BATCHGET_MATERIAL, CHECKJIUGONGGECOUNT,
        SAVECARDDATA, CHECKVOTECOUNT, SAVEVOTEDATA, CHECKBUYRIGHT, SAVEAGENTDATA, GETCOUNTAGENTDATA) = \
        ('USERLIST', 'USERINFO', 'ACCESSTOKEN', 'CSTEXT', 'MESSAGEHIS', 'SCODE', 'GETSCODEPIC', 'GENMENU',
         'GENGROUP', 'BATCHUPDATEUSER', 'TESTWHITELIST', 'CREATECARD', 'GET_MATERIALCOUNT', 'GET_MATERIAL',
         'BATCHGET_MATERIAL', 'CHECKJIUGONGGECOUNT', 'SAVECARDDATA', 'CHECKVOTECOUNT', 'SAVEVOTEDATA',
         'CHECKBUYRIGHT', 'SAVEAGENTDATA', 'GETCOUNTAGENTDATA')


class WechatProcessEnum:
    """ the Enum for wechat Process now supported.

    """
    # TODO: how to use this. make same with the config file.
    allAPIEnum = (SENDMESSAGE, SENDSCODE, GETSCODEPIC, MAKEMENU) = ('sendmsg', 'sendscode', 'getscodepic', 'makemenu')


class WechatReturnEnum:
    """ the Enum for wechat API now supported.

    """
    allReturnEnum = (INVALID_APPSCRET, INVALID_TOKEN, INVALID_OPENID, TIMEOUT_ACCESS_TOKEN, BUSY, SUCCESS) = (
        '40001', '40002', '40003', '42001', '-1', '0')


class RESTApiEnum:
    """ the Enum for REST API now supported.

    """
    allAPIEnum = (SAVEAGENTDATA, GETQUIZBEELIST, SAVEQUIZBEEDATA, CHECKVOTECOUNT, SAVEVOTEDATA) = \
        ('SAVEAGENTDATA', 'GETQUIZBEELIST', 'SAVEQUIZBEEDATA', 'CHECKVOTECOUNT', 'SAVEVOTEDATA')


# print ORMSectionEnum.RetDetail
# print ORMSectionEnum.allEnum
#if 'conditionDetail' in ORMSectionEnum.allEnum:
#    print('in')
#else:
#    print('out')

def generateRESTRet(inLogging, inDict, inMesaageEnum, inRetClassDict):
    """generate the rest return data.

    1.  according the config file to generate skelon for return data;
    2.  update the data:if already have the message, update it;if no, add it.
    inLogging -> input logger instance.
    inDict -> input Dictionary data, this data always from the sql result.
    inMessageEum -> enum the return message.
    inRetClassDict -> input the return data dictionary.
    at first: the return dictionary is from config;after executing the sql: the return dictionary data will be updated.
    return inRetClassDict.
    """

    if not isinstance(inDict, dict):
        raise TypeError

    if not isinstance(inRetClassDict, dict):
        raise TypeError

    if not isinstance(inLogging, logging.Logger):
        raise TypeError

    for case in switch(inMesaageEnum):
        if case(SQLStatusEnum.SUCCESS):
            #print log.
            inLogging.debug("%s get success data." % (sys._getframe().f_code.co_name))

            #update return dictionary.add success number and list.
            if 'success' in inRetClassDict:
                if 'datalist' in inRetClassDict['success']:
                    localDatalist = inRetClassDict['success']['datalist']
                    if len(localDatalist) > 0:
                        pass
                    else:
                        #first it is list.
                        localDatalist = []

                    localDataItem = inDict[str(inRetClassDict['success']['listsource'])]
                    localDatalist.append(localDataItem)

                    inRetClassDict['success'].update({'datalist': localDatalist})
                else:
                    raise TypeError
            else:
                raise TypeError
            break
        if case(SQLStatusEnum.FAILURE):
            #print log.
            inLogging.error("%s get failure data ." % (sys._getframe().f_code.co_name))

            #update return dictionary.add error number and list.
            if 'error' in inRetClassDict:
                if 'datalist' in inRetClassDict['error']:
                    localDatalist = inRetClassDict['error']['datalist']
                    if len(localDatalist) > 0:
                        pass
                    else:
                        #first it is list.
                        localDatalist = []

                    localDataItem = inDict[str(inRetClassDict['error']['listsource'])]
                    localDatalist.append(localDataItem)

                    inRetClassDict['error'].update({'datalist': localDatalist})
                else:
                    raise TypeError
            else:
                raise TypeError
            break
        if case():  # default, could also just omit condition or 'if True'
            pass
            # No need to break here, it'll stop anyway


# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    """I got this class from Brian Beck web site.

    """

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


#判断网站来自mobile还是pc
def checkMobile(request):
    """
    demo :
        @app.route('/m')
        def is_from_mobile():
            if checkMobile(request):
                return 'mobile'
            else:
                return 'pc'
    :param request:
    :return:
    """
    userAgent = request.request.headers['User-Agent']
    # userAgent = env.get('HTTP_USER_AGENT')

    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True


def is_from_mobile(method):
    """
    检查是否从手机来的访问，如是则自动跳转到手机端的访问页，否则继续访问pc端页面
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if checkMobile(self):
            self.render("weshop/default.html")
        return method(self, *args, **kwargs)

    return wrapper


##将request所有参数转换为字典返回
def getAllBodyPara(self):
    if len(self.request.body_arguments) != 0:
        parm = {}
        for arg in self.request.body_arguments:
            if len(arg) > 2 and arg[-2:] == "[]":
                parm[arg[:-2]] = self.get_arguments(arg, None)
            else:
                parm[arg] = self.get_argument(arg, None)
    elif len(self.request.body) != 0:
        parm = json.loads(self.request.body)
    else:
        parm = {}

    return parm


dataType = ['int', 'varchar', 'datetime']

# 将值转换成指定类型值
def ToValue(type, v):
    if type in ["int", "bigint"]:
        return int(v) if not isinstance(v, int) and v else v
    elif type in ['float', 'decimal', 'double']:
        return float(v) if not isinstance(v, float) else v
    elif type in ['datetime']:
        return datetime.datetime(v) if not isinstance(v, datetime.datetime) else v
    else:
        return v


# para:参数列表  md:{映射字段参数}
def DataMapping2(para={}, md={}):
    d = dict()
    for p in para:
        if p in md:
            type = md[p]['Type']
            type = type[0:type.find('(')]
            d[p] = ToValue(type, para.get(p))
    return d


def checkTypes(prop, types=[]):
    if len(types) == 0:
        return True

    for t in types:
        if isinstance(prop, t):
            return True

    return False


def getTotalCount(dbObj, tablename, parm, attachWhere=None):
    try:
        # info = dbObj.query("select count(1) totalcount from " + tablename + " where 1=1 "
        # + MakeWhere(arguments, md))
        # db.select("menu", what=Menu.what, where=whereStr, vars=vars)
        where = list()
        where.append("1=1")
        for p in parm:
            # where.append("%s = :%s" % (p, p))
            where.append("%s = %%(%s)s" % (p, p))
        where = " and ".join(where)
        if attachWhere is not None:
            where += attachWhere
        info = dbObj.get("select count(1) totalcount from %s where %s" % (tablename, where % parm))
        retinfo = info
    except Exception as e:
        retinfo = {"totalcount": -1}
    return retinfo


##获取分页信息
def getPager(para={}, records=0):
    if not isinstance(para, dict):
        para = {}
    rows = int(para.pop("rows") if isinstance(para.get("rows"), unicode) else para.pop("rows")[0]) if para.get(
        "rows") else 20  # 请求行数
    page = int(para.pop("page")) if para.has_key("page") else 1  # 请求页码
    start = (page - 1) * rows  # 请求开始行数
    total = int(math.ceil(float(records) / rows))  # 总页数
    return {"page": page, "total": total, "records": records, "start": start, "pagesize": rows, "userdata": para,
            "rows": []}


def MakeWhere2(para={}):
    if not para or len(para) == 0:
        return "1 = 1"
    where = []
    for p in para:
        where.append("%s = %%(%s)s" % (p, p))
    where = ' and '.join(where)
    return where


def MakeInsert2(para={}):
    if not para or len(para) == 0:
        return ""
    field, value = [], []
    for p in para:
        # where.append("%s = :%s" % (p, p))
        field.append(p)
        if isinstance(para[p], datetime.datetime):
            value.append("'" + para[p].strftime("%Y-%m-%d %H:%M:%S") + "'")
        else:
            value.append("'%s'" % para[p])
    return (', '.join(field), ', '.join(value))


def MakeUpdate2(para={}):
    l = []
    for d in para:
        if isinstance(para[d], datetime.datetime):
            l.append(str(d) + "='" + para[d].strftime("%Y-%m-%d %H:%M:%S") + "'")
        # elif isinstance(para[d], int):
        # l.append('%s=%s' % (d, para[d]))
        elif checkTypes(para[d], [int, long]):
            l.append('%s=%s' % (d, para[d]))
        else:
            l.append(str(d) + "='" + para[d] + "'")
    return ",".join(l)


# 检查Insert必填字段
def checkInsertFiled(parm, md):
    error = []
    for p in md:
        if p["Field"] not in parm:
            error.append("param %s is null" % p["Field"])
    return ",".join(error)


def listToLookup(key, list=[]):
    result = {}
    for item in list:
        if not result.has_key(item[key]):
            result[item[key]] = []
        result[item[key]].append(item)
    return result