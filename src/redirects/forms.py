"""
Redirects application related forms.
"""
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
    """New redirect creation form."""

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = "form-horizontal"
        helper.label_class = "col-md-3"
        helper.field_class = "col-md-9"
        helper.add_input(Submit("submit", "Fake it!", css_class="float-end"))
        return helper

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
