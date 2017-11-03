#!/usr/bin/env python
# coding=utf8
""" this module is the main entrance for this project.
"""

import time
import signal
import logging
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options
import socket

from bootloader import settings,memcachedb
from lib.route import Route
from lib.session import MemcacheSessionStore
from lib.frameworkcache import MemcacheFrameworkCacheStore
from common.Cmn import switch
from handler import autoform,thirdeval

define('cmd', default='runserver', metavar='runserver|syncdb|syncnewdb')
define('port', default=settings['cfg'].get('port', 'port'), type=int)

from common.Log import LogInit

LogInit("loggingManager.conf")

class Application(tornado.web.Application):
    def __init__(self):
        self.memcachedb = memcachedb
        self.session_store = MemcacheSessionStore(memcachedb)
        self.frameworkcache_store = MemcacheFrameworkCacheStore(memcachedb)

        handlers = [
                       tornado.web.url(r"/static/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=settings['static_path']), name='static_path'),
                       tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=settings['upload_path']), name='upload_path')
                   ] + Route.routes()
        tornado.web.Application.__init__(self, handlers, **settings)

def runserver():
    loggerRoot = logging.getLogger('root')

    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)

    loop = tornado.ioloop.IOLoop.instance()

    def shutdown():
        loggerRoot.info('Server stopping ...')
        http_server.stop()

        loggerRoot.info('IOLoop wil  be terminate in 1 seconds')
        deadline = time.time() + 1

        def terminate():
            now = time.time()

            if now < deadline and (loop._callbacks or loop._timeouts):
                loop.add_timeout(now + 1, terminate)
            else:
                loop.stop()
                loggerRoot.info('Server shutdown')

        terminate()

    def sig_handler(sig, frame):
        loggerRoot.warn('Caught signal:%s', sig)
        loop.add_callback(shutdown)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    ipList = socket.gethostbyname_ex(socket.gethostname())
    localIp = ipList[2][len(ipList[2]) - 1]
    loggerRoot.info('Server running on http://%s:%s' % (localIp, options.port))
    loop.start()


if __name__ == '__main__':
    #import pydevd
    #pydevd.settrace('192.168.176.1', port=51234, stdoutToServer=True, stderrToServer=True)

    loggerRoot = logging.getLogger('root')
    loggerRoot.info("start run manager module.")

    # clear the first arg.
    import sys
    #pop project config.
    poparg0 = sys.argv.pop(1)

    parse_command_line()

    if len(sys.argv) > 1:
        #pop command config.
        poparg1 = sys.argv.pop(1)
    else:
        pass

    #restore the arg.
    #append project config.
    sys.argv.append(poparg0)

    if 'poparg1' in locals().keys():
        #append command config.
        sys.argv.append(poparg1)
    else:
        pass

    #TODO: wrong in linux.
    for case in switch(options.cmd):
        if case('syncdb'):
            break
        if case('syncnewdb'):
            break
        if case('preparedb'):
            break
        if case():
            runserver()
            pass
            # No need to break here, it'll stop anyway
