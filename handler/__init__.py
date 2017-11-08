#!/usr/bin/env python
# coding=utf8
""" the module is for initialize the handler.
"""

import urllib
from tornado.web import RequestHandler
from lib.session import Session
from lib.frameworkcache import Frameworkcache
from common.Cmn import switch
import mako.lookup
import mako.template
from mako import exceptions

class BaseHandler(RequestHandler):

    def initialize(self):
        template_path = self.get_template_path()
        self.lookup = mako.lookup.TemplateLookup(directories=[template_path], input_encoding='utf-8', output_encoding='utf-8')

    def set_default_headers(self):
        self.clear_header('Server')

    def render_string(self, template_name, **context):

        try:
            context.update({
                'xsrf': self.xsrf_form_html,
                'module': self.ui.modules,
                'request': self.request,
                'user': self.current_user,
                'handler': self,}
            )

            template = self.lookup.get_template(template_name)
            namespace = self.get_template_namespace()
            namespace.update(context)
            return template.render(**namespace)
        except:
            #print(exceptions.text_error_template().render())
            #return exceptions.text_error_template().render()
            #print(exceptions.html_error_template().render())
            return exceptions.html_error_template().render()

        #return self._jinja_render(path = self.get_template_path(),filename = template_name,
        #    auto_reload = self.settings['cfg'].get('project','DEBUG'), **context)

    #def _jinja_render(self,path,filename, **context):
    #    template = self.application.jinja_env.get_template(filename,parent=path)
    #    return template.render(**context)

    def render(self,template_name,**context):
        self.finish(self.render_string(template_name,**context))

    @property
    def is_xhr(self):
        return self.request.headers.get('X-Requested-With', '').lower() == 'xmlhttprequest'

    @property
    def memcachedb(self):
        return self.application.memcachedb

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            sessionid = self.get_secure_cookie('sid')
            self._session = Session(self.application.session_store, sessionid, expires_days=1)
            if not sessionid:
                self.set_secure_cookie('sid', self._session.id, expires_days=1)
            return self._session

    @property
    def frameworkcache(self):
        if hasattr(self, '_frameworkcache'):
            return self._frameworkcache
        else:
            cacheid = self.get_secure_cookie('sid')
            self._frameworkcache = Frameworkcache(self.application.frameworkcache_store, cacheid,expires_secondes=7199)
            if not cacheid:
                self.set_secure_cookie('sid', self._frameworkcache.id, expires_days=1)
            return self._frameworkcache

    def get_current_user(self):
        """get the current user from session.

        """
        return self.session['user'] if 'user' in self.session else None

    @property
    def next_url(self):
        return self.get_argument("next", "/")

