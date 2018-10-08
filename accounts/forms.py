import re

from django import forms
from django.core import validators
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm, UserChangeForm,
                                       ReadOnlyPasswordHashField)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from . import models


def v_err(flaw):
    """Raise various validation errors."""
    error_messages = {
        'lc_letters': _("Password must contain a lowercase letter."),
        'uc_letters': _("Password must contain a capital letters."),
        'no_num': _("Password must contain a numerical digit."),
        'symbols': _("Password must contain a non-alphanumeric symbol."),
        'password_mismatch': _("The two password fields didn't match."),
        'pw_short': _("Password must contain at least 14 characters."),
        'bio_short': _("Bio must contain at least 10 characters."),
        'bio_empty':_("Bio must contain non-whitespace."),
        'password_incorrect': _("The password is incorrect."),
        'triplets': _("New password same as old password."),
        'email_mismatch': _("The two email fields didn't match."),
        'not_email': _("This is not a valid email address.")
    }
    raise forms.ValidationError(
        error_messages[flaw],
        code=flaw,
    )
    # Don't need return statement?
    

def pw_valid(pw):
    """Validate new passwords."""
    if not re.search(r'[_\W]+', pw):
        v_err('symbols')
    if not re.search(r'\d+', pw):
        v_err('no_num')
    if not re.search(r'[a-z]', pw):
        v_err('lc_letters')
    if not re.search(r'[A-Z]', pw):
        v_err('uc_letters')
    if len(pw) < 14:
        v_err('pw_short')
        # Don't need return statement?


def bio_good(bio):
    """Validate bio is over 10 characters."""
    if len(bio) < 10:
        v_err('bio_short')
    if not re.search(r'[\S]+', bio):
        v_err('bio_empty')
    # No need to return bio


class AccountCreationForm(UserCreationForm):
    """
    A modified UserCreationForm.
    """
    email2 = forms.CharField(label=_("Email confirmation"),
        widget=forms.EmailInput,
        help_text=_("To confirm: enter the same email as above."))        
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput,
                                validators=[pw_valid])
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        # account = models.Account.objects.get(pk=model.pk) # This line was a mistake?
        fields = ("username", "email", "email2", "first_name", "last_name",
                  "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            v_err('not_email')
        return email
        
    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            v_err('email_mismatch')
        print('*** EMAIL 2 CHECKED ***')
        return email2

    # def clean_password1(self):
    #    password1 = self.cleaned_data.get("password1")
    #    pw_valid(password1)
    #    return password1   ## Don't need clean_password1 because pw1 is validated already above.

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            v_err('password_mismatch')
        return password2


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # account.bio = self.cleaned_data["bio"]
        if commit:
            user.save()
        return user


class AccountEditForm(UserChangeForm):
    """
    Form for editing accounts.
    Extends UserChangeForm.
    NOTE: Does NOT extend my AccountCreationForm.
    """
    email = forms.CharField(label=_("Email"),
        widget=forms.EmailInput)
    email2 = forms.CharField(label=_("Email confirmation"),
        widget=forms.EmailInput,
        help_text=_("To confirm: enter the same email as above."))        
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password."))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",
                  "email2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            v_err('not_email')
        return email
                  
    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            v_err('email_mismatch')
        print('*** EMAIL 2 CHECKED ***')
        return email2

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password


class PasswordEditForm(PasswordChangeForm):
    """
    Form for allowing users to edit their passwords.
    IMPORTANT: Please remember this does NOT extend from AccountCreationForm.
    Do not remove logic from here because it is found there.
    """
    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        old_password = self.cleaned_data.get("old_password")
        if old_password == new_password1:
            v_err('triplets')
        pw_valid(new_password1)
        print('*** PASSWORD 1 CHECKED ***')
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            v_err('password_mismatch')
        print('*** PASSWORD 2 CHECKED ***')
        return new_password2


class AccountExtrasCreationForm(forms.ModelForm):
    """
    A form for adding the non-default attributes to a companion model for Django's User model.
    """
    bio = forms.CharField(label=("User Bio"),
                          widget=forms.Textarea,
                          validators=[bio_good])
    dob = forms.DateField(label=("Date of Birth"))
    ava = forms.ImageField(label=("User Image"))


    class Meta:
        model = models.Account
        fields = ("bio", "dob", "ava")

    def save(self, commit=True):
        account = super(AccountExtrasCreationForm, self).save(commit=False)
        account.bio = self.cleaned_data["bio"]
        ## account.user = how do i target a user that isn't saved yet???
        ## Can i handle this in views?
        if commit:
            account.save()
        return account


class AccountExtrasEditForm(forms.ModelForm):
    bio = forms.CharField(label=("User Bio"),
                          widget=forms.Textarea,
                          validators=[bio_good])

    class Meta:
        model = models.Account
        fields = ("bio", "dob", "ava")
