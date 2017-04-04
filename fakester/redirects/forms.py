"""
Redirects module related forms
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
    """
    Form for creating `redirect.Redirect` instances, with added 'security'
    of ReCaptcha field
    """
    captcha = ReCaptchaField()

    class Meta:
        model = Redirect
        fields = ('local_path', 'destination_url')
        labels = {
            'local_path': _("Fake local path"),
            'destination_url': _("Destination URL"),
        }
        widgets = {
            'local_path': forms.TextInput(
                attrs={
                    'placeholder': '/2017/04/04/we-are-all-doomed'
                }
            ),
            'destination_url': forms.TextInput(
                attrs={
                    'placeholder': 'https://github.com/pawelad/fakester'
                }
            ),
        }
