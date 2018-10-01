import re

from django import forms
from django.core import validators
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from . import models


class AccountCreationForm(UserCreationForm):
    """
    A modified UserCreationForm.
    """
    error_messages = {
        'lc_letters': _("Password must contain a lowercase letter."),
        'uc_letters': _("Password must contain a capital letters."),
        'no_num': _("Password must contain a numerical digit."),
        'symbols': _("Password must contain a non-alphanumeric symbol."),
        'password_mismatch': _("The two password fields didn't match."),
        'bio_short': _("Bio must contain at least 10 characters.")
    }
    bio = forms.CharField(label=("User Bio"),
        widget=forms.Textarea)
    email2 = forms.CharField(label=_("Email confirmation"),
        widget=forms.EmailInput,
        help_text=_("To confirm: enter the same email as above."))        
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = models.Account
        fields = ("username", "email", "first_name", "last_name",
                  "birth_date", "country", "website", "avatar")

    def weak_password(self, flaw):
        raise forms.ValidationError(
            self.error_messages[flaw],
            code=flaw,
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # if password1.isalpha() or password1.isdigit():
        #    weak_password()
        if not re.search(r'[_\W]+', password1):
            self.weak_password('symbols')
        if not re.search(r'\d+', password1):
            self.weak_password('no_num')
        if not re.search(r'[a-z]', password1):
            self.weak_password('lc_letters')
        if not re.search(r'[A-Z]', password1):
            self.weak_password('uc_letters')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
        
    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        if len(bio) < 10:
            raise forms.ValidationError(
                self.error_messages['bio_short'],
                code='bio_short',
            )
        return bio

    def save(self, commit=True):
        account = super(UserCreationForm, self).save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        account.bio = self.cleaned_data["bio"]
        if commit:
            account.save()
        return account


class AccountEditForm(AccountCreationForm):
    error_messages = {
        'email_mismatch': _("The two email fields didn't match.")
    }

    class Meta:
        model = models.Account
        fields = ("username", "first_name", "last_name", "email",
                  "email2", "birth_date", "bio", "avatar")

    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        print('*** EMAIL 2 CHECKED ***')
        return email2


class PasswordEditForm(PasswordChangeForm):
    """
    Form for allowing users to edit their passwords.
    IMPORTANT: Please remember this does NOT extend from AccountCreationForm.
    Do not remove logic from here because it is found there.
    """
    error_messages = {
        'password_mismatch': _("New password confirmation doesn't match."),
        'weak_pw': _("New password too weak."),
        'lc_letters': _("Password must contain a lowercase letter."),
        'uc_letters': _("Password must contain a capital letters."),
        'no_num': _("Password must contain a numerical digit."),
        'triplets': _("New password same as old password."),
        'symbols': _("Password must contain a non-alphanumeric symbol."),
        'password_incorrect': _("The original password is incorrect.")
    }

    def weak_password(self, flaw):
        raise forms.ValidationError(
            self.error_messages[flaw],
            code=flaw,
        )

    class Meta:
        model = models.Account
        fields = ("old_password", "new_password1", "new_password2")

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        old_password = self.cleaned_data.get("old_password")
        if not re.search(r'[_\W]+', new_password1):
            print('**** NO SYMBOLS ****')
            self.weak_password('symbols')
        if not re.search(r'\d+', new_password1):
            print('**** NO DIGITS ****')
            self.weak_password('no_num')
        if not re.search(r'[a-z]', new_password1):
            print('**** NO LOWERCASE ****')
            self.weak_password('lc_letters')
        if not re.search(r'[A-Z]', new_password1):
            print('**** NO UPPERCASE ****')
            self.weak_password('uc_letters')
        if new_password1 == old_password:
            print('**** NEW BOSS IS OLD BOSS ****')
            self.weak_password('triplets')
        print('*** PASSWORD 1 CHECKED ***')
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        print('*** PASSWORD 2 CHECKED ***')
        return new_password2