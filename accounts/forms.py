import re

from django import forms
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.core.exceptions import ValidationError

from . import models


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = models.Account
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'birth_date',
            'bio',
            'country',
            'website',
            'avatar'
        ]


# class AccountEditForm(AccountCreationForm):
    