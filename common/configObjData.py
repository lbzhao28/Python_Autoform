""" use the configobj
"""
__author__ = 'stone'
#coding=UTF-8
from configobj import ConfigObj
import os

def getConfigFile(filename=None):
    """ get the Static config file

        Keyword arguments:
        filename -- filename can include path
    """
    configFile = {}
    if not filename:
        return None
    configFile = ConfigObj(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/" + filename)
    return configFile

