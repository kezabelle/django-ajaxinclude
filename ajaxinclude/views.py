from django.core.urlresolvers import resolve
from django.views.generic import TemplateView
from django.http import Http404

class AjaxIncludeProxy(TemplateView):

    def get_template_names(self):
        return ['ajaxinclude/entries.html']

    def get_files(self):
        data = self.request.GET.getlist('files')
        if data is None:
            raise Http404('no files')
        safe_files = [f.strip() for f in data if f.strip()]
        if len(safe_files) < 1:
            raise Http404('no files')
        return safe_files

    def get_context_data(self, *args, **kwargs):
        data_for_context = {}
        for file in self.files:
            callback, its_args, its_kwargs = resolve(file)
            response = callback(self.request, *its_args, **its_kwargs)
            try:
                for_sending = response.content
            except AttributeError:
                # Didn't return a response, perhaps because the callback
                # detected is_ajax() and fed it something else.
                for_sending = response
            data_for_context[file] = for_sending
        ctx = super(AjaxIncludeProxy, self).get_context_data(*args, **kwargs)
        ctx.update(files=data_for_context)
        return ctx

    def get(self, request, *args, **kwargs):
        self.files = self.get_files()
        return super(AjaxIncludeProxy, self).get(request, *args, **kwargs)
