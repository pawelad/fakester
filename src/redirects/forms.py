"""
Redirects application related forms.
"""
from django import forms

from captcha.fields import ReCaptchaField

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
    """Redirect creation form with added 'security' of a ReCaptcha field."""

    captcha = ReCaptchaField()

    field_order = (
        "local_path",
        "destination_url",
        "captcha",
    )

    class Meta:
        model = Redirect
        fields = (
            "local_path",
            "destination_url",
        )
        widgets = {
            "local_path": forms.TextInput(
                attrs={"placeholder": "/2023/01/31/how-is-it-2023-already"}
            ),
            "destination_url": forms.TextInput(
                attrs={"placeholder": "https://youtu.be/I6OXjnBIW-4"}
            ),
        }
