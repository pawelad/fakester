from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
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
                    'placeholder': '/2016/06/17/have-you-heard-of-fakester.html'
                }
            ),
            'destination_url': forms.TextInput(
                attrs={
                    'placeholder': 'https://github.com/pawelad/fakester'
                }
            ),
        }
