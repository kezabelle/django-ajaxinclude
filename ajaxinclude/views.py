from django.core.urlresolvers import resolve, Resolver404
from django.template.response import ContentNotRenderedError
from django.views.generic import TemplateView
from django.http import Http404

class FakeResponse(object):
    status_code = 999
    content = u''

class AjaxIncludeProxy(TemplateView):

    def get_template_names(self):
        return ['ajaxinclude/entries.html']

    def get_files(self):
        data = self.request.GET.get('files')
        if data is None:
            raise Http404('no files')
        safe_files = [f.strip() for f in data.split(',') if f.strip()]
        if len(safe_files) < 1:
            raise Http404('no files')
        return safe_files

    def get_context_data(self, *args, **kwargs):
        data_for_context = {}
        for file in self.files:
            try:
                callback, its_args, its_kwargs = resolve(file)
                response = callback(self.request, *its_args, **its_kwargs)
            except Resolver404:
                # calling resolve() may not work
                response = FakeResponse()
            except Http404:
                # the callback itself might say it shouldn't be found.
                response = FakeResponse()

            if response.status_code == 200:
                try:
                    data = response.content
                except ContentNotRenderedError:
                    data = response.render().content
                data_for_context[file] = data
            else:
                data_for_context[file] = FakeResponse.content
        ctx = super(AjaxIncludeProxy, self).get_context_data(*args, **kwargs)
        ctx.update(files=data_for_context)
        return ctx

    def get(self, request, *args, **kwargs):
        self.files = self.get_files()
        return super(AjaxIncludeProxy, self).get(request, *args, **kwargs)

