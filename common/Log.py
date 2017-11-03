"""use logging module
"""
__author__ = 'Long'
#coding=UTF-8
import logging
import logging.config
import traceback
import os
if not os.path.exists("logs"):
    os.mkdir("logs")

def LogInit(file=None):
    """init log

        Keyword arguments:
        file    --  the log config file.
    """
    try:
        if not file:
            return
        #do not disable existing_loggers.
        logging.config.fileConfig(file, disable_existing_loggers=False)
    except:
        f = open('logs/traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()

