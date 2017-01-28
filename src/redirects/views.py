from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from ratelimit.mixins import RatelimitMixin
from ipware.ip import get_real_ip

from redirects.models import Redirect
from redirects.forms import RedirectModelForm


class RedirectFormView(RatelimitMixin, TemplateView):
    template_name = 'redirects/form.html'
    http_method_names = ['get', 'post']

    ratelimit_key = 'ip'
    ratelimit_rate = '5/m'
    ratelimit_block = True

    def get_context_data(self, **kwargs):
        kwargs['form'] = RedirectModelForm(data=self.request.POST or None)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)

        form = ctx['form']
        if form.is_valid():
            # Add sender IP address
            redirect = form.save(commit=False)
            redirect.sender_ip = get_real_ip(self.request)
            redirect.save()

            # Add saved object to access it in the template
            self.redirect = redirect

        return super().get(request, *args, **kwargs)


class ActualRedirectView(TemplateView):
    template_name = 'redirects/redirect.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        redirect = get_object_or_404(
            Redirect, local_path=self.kwargs['local_path'],
        )
        redirect.clicks += 1
        redirect.save()

        kwargs['redirect'] = redirect

        return super().get_context_data(**kwargs)
