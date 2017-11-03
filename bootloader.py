# !/usr/bin/env python
# coding=utf8
""" this module is for load the config file.
    some project initialize.
"""

import os
import memcache
from common.Cfg import Config
import platform

from multiEnv import getProjectArg

sysstr = platform.system()

if(sysstr =="Linux"):
    localCfgPath = "Project_Conf/"+getProjectArg()+"/"
    cfg = Config(filename=localCfgPath+"config4UI.conf")
else:
    localCfgPath = os.path.join("Project_Conf", getProjectArg(), "config4UI.conf")
    cfg = Config(filename=localCfgPath)
# save config data to dictionary.
settings = {'cfg': cfg}

settings.update({
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'style_path': os.path.join(os.path.dirname(__file__), 'style'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'upload_path': os.path.join(os.path.dirname(__file__), 'upload'),
    'cookie_secret': settings['cfg'].get('cookie', 'cookie_secret'),
    'login_url': settings['cfg'].get('login', 'login_url'),
    "xsrf_cookies": True,
    'autoescape': None
})

memcachedb = memcache.Client([settings['cfg'].get('mem', 'MEMCACHE_HOST')])

