"""the classes for Config.

    1.  config  :   the class for ConfigParser

"""
__author__ = 'Long'
#coding=UTF-8
import logging
import platform
import configparser
import os

class Config:
    """get filename to get config."""
    __filename = None
    __gci = None
    def __init__(self,filename=None):
        if not filename:
            return None
        self.__filename = filename
        self.__gci = configparser.ConfigParser()
        sysstr = platform.system()
        if(sysstr =="Windows"):
            self.__gci.read(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\" + filename)
        else:
            self.__gci.read(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/" + filename)

    def getItems(self,section):
        """get the section dictionary items for some section.

        :param section:
        :return: the section dictionary.
        """
        try:
            return self.__gci.items(section)
        except Exception as e:
            logging.error("Config -> get ,error:[%s]" % e)
            return None

    def get(self,section,name):
        """get the value from the config


            Keyword arguments:
            section --  the config section in config file
            name    --  the section name in config section

        """
        try:
            return self.__gci.get(section,name)
        except Exception as e:
            logging.error("Config -> get ,error:[%s]" % e)
            return None

    def getDecypt(self,section,name):
        """get the value from the config,and decrypt string.


            Keyword arguments:
            section --  the config section in config file
            name    --  the section name in config section

        """
        try:
            originStr = self.__gci.get(section,name)
            key = 13    # magic number,encrypt string is : 13;
            decryptStr = decrypt(key,originStr)
            return decryptStr
        except Exception as e:
            logging.error("Config -> get ,error:[%s]" % e)


def encrypt(key, s):
    """encrypt string.
    """
    b = bytearray(str(s).encode("gbk"))
    n = len(b)
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")

def decrypt(key, s):
    """decrypt string
    """
    c = bytearray(str(s).encode("gbk"))
    n = len(c)
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except Exception as e:
        return "failed"

#test code
#key = 13
#s1 = encrypt(key, 'lhzerp')
#s2 = decrypt(key, s1)
#print s1,'\n',s2

#test code
#key = 13
#s1 = encrypt(key, 'rabbitStone')
#s2 = decrypt(key, s1)
#print s1,'\n',s2

#test code
#key = 13
#s1 = encrypt(key, 'shop')
#s2 = decrypt(key, s1)
#print s1,'\n',s2
