from django.core.urlresolvers import resolve
from django.views.generic import TemplateView
from django.http import Http404

class FakeResponse(object):
    status_code = 999
    content = None

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
            callback, its_args, its_kwargs = resolve(file)
            try:
                response = callback(self.request, *its_args, **its_kwargs)
            except Http404:
                response = FakeResponse()
            if response.status_code == 200:
                data = response.content
                data_for_context[file] = data
        ctx = super(AjaxIncludeProxy, self).get_context_data(*args, **kwargs)
        ctx.update(files=data_for_context)
        return ctx

    def get(self, request, *args, **kwargs):
        self.files = self.get_files()
        return super(AjaxIncludeProxy, self).get(request, *args, **kwargs)

