#!/usr/bin/env python
# coding=utf8
""" the entrance for autoform handler.

# prerequisite:
    1.  based on Python 3.5.x

# usage:
    1)  the url route for autoform
    2)  the handler entrance for autoform

# other:
    None

"""

from lib.route import route
import logging
import json
from handler import BaseHandler
import colander
import deform
from colander import (
    Boolean,
    Integer,
    Length,
    MappingSchema,
    OneOf,
    SchemaNode,
    SequenceSchema,
    String
)

from deform import (
    Form,
    ValidationFailure,
    widget
)

@route(r'/autoformapi', name='autoformapi') #autoform api.
class AUTOFORMAPIHandler(BaseHandler):
    """ autoform api.
    """
    def check_xsrf_cookie(self):
        """
        rest api do not check the xsrf.
        :return:
        """
        pass

    loggerRoot = logging.getLogger('root')
    def get(self):
        self.loggerRoot.info("start autoform get API.")
        retJson = {'errcode':-1,'errmsg':'do nothing'}
        self.write(retJson)

    def post(self):
        self.loggerRoot.info("start autoform post API.")
        retJson = {'errcode':-1,'errmsg':'do nothing'}
        self.write(retJson)

colors = (('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'))

class DateSchema(MappingSchema):
    month = SchemaNode(Integer())
    year = SchemaNode(Integer())
    day = SchemaNode(Integer())

class DatesSchema(SequenceSchema):
    date = DateSchema()

class MySchema(MappingSchema):
    name = SchemaNode(String(),
                      description = 'The name of this thing')
    title = SchemaNode(String(),
                       widget = widget.TextInputWidget(size=40),
                       validator = Length(max=20),
                       description = 'A very short title')
    password = SchemaNode(String(),
                          widget = widget.CheckedPasswordWidget(),
                          validator = Length(min=5))
    is_cool = SchemaNode(Boolean(),
                         default = True)
    dates = DatesSchema()
    color = SchemaNode(String(),
                       widget = widget.RadioChoiceWidget(values=colors),
                       validator = OneOf(('red', 'blue')))


@route(r'/autoformdemo', name='autoformdemo') #autoformdemo page.
class AUTOFORMDEMOHandler(BaseHandler):
    """ autoform demo.
    this is some page.
    """
    loggerRoot = logging.getLogger('root')
    def get(self):
        self.loggerRoot.info("start autoform demo page get.")

        #test time code.
        #import time
        #time.sleep(10)

        #myform = deform.Form(schema, buttons=('submit',))
        #form = myform.render()

        schema = MySchema()
        myform = Form(schema, buttons=('submit',))
        template_values = {}
        template_values.update(myform.get_widget_resources())

        #if 'submit' in request.POST:
        #    controls = request.POST.items()
        #    try:
        #        myform.validate(controls)
        #    except ValidationFailure as e:
        #        template_values['form'] = e.render()
        #    else:
        #        template_values['form'] = 'OK'
        #    return template_values

        template_values['form'] = myform
        #template_values['form'] = myform.render()

        if 'css' in template_values:
            pass
        else:
            template_values['css'] = None

        if 'js' in template_values:
            pass
        else:
            template_values['js'] = None

        self.render("deformdemo/example.zpt",css=template_values['css'],js=template_values['js'],form=template_values['form'])

    def post(self):
        self.loggerRoot.info("start autoform demo page post.")
        pass



@route(r'/test', name='test') #test page.
class TESTHandler(BaseHandler):
    """ test demo.
    this is some page.
    """
    loggerRoot = logging.getLogger('root')
    def get(self):
        self.loggerRoot.info("start test page.")
        self.render("index.html",title='Text',body='This is body')
        #self.render("index.html",body='This is body')
