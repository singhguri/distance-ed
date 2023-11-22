from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Order, Instructor


class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        ("1", "Yes"),
        ("0", "No"),
    ]

    interested = forms.CharField(
        required=True, widget=forms.RadioSelect(choices=INTEREST_CHOICES), initial=0
    )

    levels = forms.IntegerField(min_value=1, initial=1)

    comments = forms.CharField(
        widget=forms.Textarea, required=False, label="Additional Comments"
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["student", "course", "levels", "order_date"]

    widgets = {"student": forms.RadioSelect, "order_date": forms.SelectDateWidget}


class LoginForm(AuthenticationForm):
    class Meta:
        model = None  # No model is associated with this form
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )


# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User

#     username = forms.CharField(
#         label="USERNAME",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         label_suffix="",
#     )
#     password = forms.CharField(
#         label="PASSWORD",
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#         label_suffix="",
#     )

#     error_messages = {
#         "invalid_login": (
#             "Please enter a correct username and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         "inactive": ("This account is inactive."),
#     }
