#!/usr/bin/env python
from random import randint
from importd import d

d(INSTALLED_APPS=[
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'ajaxinclude',
])


@d("/random/<int:input>/")
def randomised(request, input):
    return d.HttpResponse("a number by you: %d" % int(input))

@d("/random/")
def randomised(request):
    return d.HttpResponse("a random number for you: %d" % randint(1, 100))

@d("/<slug:one>/<slug:two>/")
def index(request, one, two):
    return d.HttpResponse(u'first parameter was %s, the second was %s' % (one, two))

@d("/hello/world/")
def hello_world(request):
    return d.HttpResponse("hello world")

@d("^$")
def index(request):
    return d.render_to_response('index.html', {}, context_instance=d.RequestContext(request))

from ajaxinclude.views import AjaxIncludeProxy
d.add_view('/ajaxinclude/', AjaxIncludeProxy.as_view())

