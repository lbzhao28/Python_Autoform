__author__ = 'stone'
#coding=UTF-8
""" this module tries to set the multi support for different environment
"""
import sys

def setArgsProject(project):
    """set the args project.

    """
    sys.argv.append(project)

def getProjectArg():
    """get the project args.

    the project is the first argument.
    return -> the project argu.
    """
    args = sys.argv
    return args[1]

def getArgs():
    """get the args. do not use now.

    """
    args = sys.argv
    dict = {}
    if len(args)-1 >= 1:
        dict1 = {"project":args[1]}
        dict.update(dict1)
    return dict

import os
def testCode():
    p = os.path.dirname(__file__)
    p=os.path.join(os.path.dirname(__file__), 'Templates').replace('\\','/')
    directories=[os.path.join(os.path.dirname(__file__), 'Templates').replace('\\','/'),]

#testCode()

