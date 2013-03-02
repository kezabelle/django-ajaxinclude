#!/usr/bin/env python
from uuid import uuid4
from random import randint
from importd import d

d(INSTALLED_APPS=[
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'ajaxinclude',
])

from django.contrib import admin
admin.autodiscover()
d.urlpatterns += d.patterns('',
    d.url(r'^admin/', include(admin.site.urls))
)

@d("/random/<int:input>/", name='user_number_output')
def randomised(request, input):
    return d.HttpResponse("a number by you: %d" % int(input))

@d("/random/", name='random_output')
def randomised(request):
    return d.HttpResponse("a random number for you: %d" % randint(1, 100))

@d("/hello/world/", name='fixed_output')
def hello_world(request):
    return d.HttpResponse("hello world")

from ajaxinclude.views import AjaxIncludeProxy
d.add_view('/ajaxinclude/', AjaxIncludeProxy.as_view(), name='ajaxinclude')

@d("/<slug:one>/<slug:two>/", name='user_text_output')
def index(request, one, two):
    return d.HttpResponse(u'first parameter was %s, the second was %s' % (one, two))


@d("^$")
def index(request):
    ctx = {
        'random_number': randint(1, 1000),
        'random_text1': str(uuid4()),
        'random_text2': str(uuid4()),
    }
    return d.render_to_response('index.html', ctx, context_instance=d.RequestContext(request))


