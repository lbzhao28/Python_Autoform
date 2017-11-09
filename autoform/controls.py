# !/usr/bin/env python
# coding=utf8
__author__ = 'stone'
import re
import logging

class Controls(object):
    """ 根据配置文件和数据生成控件清单.
    *属性*
        data
            控件相关的数据.

        config
            控件相关的配置.

    """

    loggerRoot = logging.getLogger('root')
    def __init__(self,config,data=None,**kw):
        self._config = config
        self._data =data

    @property
    def data(self):
        if self._data is None:
            return None
        return self._data

    @property
    def config(self):
        if self._config is None:
            return None
        return self._config

    @classmethod
    def print_doc(cls):
        pass

    def generateControls():
        """
        generate the controls
        """
        #get the config data

        #check the config page.

        #if have data, show the data.
        localThirdEval_Info = None

        if query_dict is None:
            localThirdEval_Info = None
        else:
            if orderid is not None:
                localThirdEval_Info = getThirdEvalInfo(orderid,configPage)
            else:
                localThirdEval_Info = None
        pass

