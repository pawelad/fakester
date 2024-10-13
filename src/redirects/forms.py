"""Redirects app forms."""

from typing import Any

from django import forms
from django.http.request import split_domain_port

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from yarl import URL

from redirects.models import Redirect


class RedirectModelForm(forms.ModelForm):
    """New redirect creation form."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize form with extra `request` argument."""
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    @property
    def helper(self) -> FormHelper:
        """Return a `crispy_forms` compatible form helper."""
        helper = FormHelper()
        helper.form_class = "form-horizontal"
        helper.label_class = "col-md-3"
        helper.field_class = "col-md-9"

        host, port = split_domain_port(self.request.get_host())

        url = URL.build(
            scheme=self.request.scheme,
            host=host,
            port=int(port) if port else None,
            path="/",
        )

        helper.layout = Layout(
            PrependedText("local_path", str(url)),
            "destination_url",
            "title",
            "description",
            Submit("submit", "Fake it!", css_class="float-end"),
        )
        return helper

    class Meta:
        model = Redirect
        fields = (
            "local_path",
            "destination_url",
            "title",
            "description",
        )
        widgets = {
            "local_path": forms.TextInput(
                attrs={"placeholder": "2024/10/14/we-re-still-here.html"}
            ),
            "destination_url": forms.TextInput(
                attrs={"placeholder": "https://youtu.be/I6OXjnBIW-4"}
            ),
            "title": forms.TextInput(
                attrs={"placeholder": "Almost 2025 and we're still here."}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "It still feels pretty 2016-ish though.",
                    "rows": 3,
                }
            ),
        }
