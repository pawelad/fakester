"""
Redirects application related forms.
"""
from django import forms

from captcha.fields import ReCaptchaField

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
    """Redirect creation form with added 'security' of a ReCaptcha field."""

    captcha = ReCaptchaField()

    class Meta:
        model = Redirect
        fields = ("local_path", "destination_url")
        labels = {
            "local_path": "Fake local path",
            "destination_url": "Destination URL",
        }
        widgets = {
            "local_path": forms.TextInput(
                attrs={"placeholder": "/2017/04/04/we-are-all-doomed"}
            ),
            "destination_url": forms.TextInput(
                attrs={"placeholder": "https://github.com/pawelad/fakester"}
            ),
        }
