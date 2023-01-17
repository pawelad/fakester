"""
Redirects module views
"""
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ipware.ip import get_real_ip
from ratelimit.mixins import RatelimitMixin

from redirects.forms import RedirectModelForm
from redirects.models import Redirect


class RedirectFormView(RatelimitMixin, TemplateView):
    """
    View for creating redirects
    """
    template_name = 'redirects/form.html'
    http_method_names = ['get', 'post']

    ratelimit_key = 'ip'
    ratelimit_rate = '5/m'
    ratelimit_block = True

    def get_context_data(self, **kwargs):
        """
        Extends Django's default `get_context_data()` method and adds
        available domains and `RedirectModelForm` instance to the context
        """
        kwargs['available_domains'] = settings.AVAILABLE_DOMAINS
        kwargs['form'] = RedirectModelForm(data=self.request.POST or None)

        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles redirect form saving and then defaults to `get()` response
        """
        ctx = self.get_context_data(**kwargs)

        form = ctx['form']
        if form.is_valid():
            # Add sender IP address
            redirect = form.save(commit=False)
            redirect.sender_ip = get_real_ip(self.request)
            redirect.save()

            # Add saved object to view in order to access it in the template
            self.redirect = redirect

        return super().get(request, *args, **kwargs)


class ActualRedirectView(TemplateView):
    """
    Simple view that redirects user to redirect destination URL
    """
    template_name = 'redirects/redirect.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        """
        Extends Django's default `get_context_data()` method and adds the
        `Redirect` instance to the context
        """
        redirect = get_object_or_404(
            Redirect, local_path=self.kwargs['local_path'],
        )
        redirect.clicks += 1
        redirect.save()

        kwargs['redirect'] = redirect

        return super().get_context_data(**kwargs)
