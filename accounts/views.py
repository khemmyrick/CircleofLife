from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm, UserChangeForm)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from . import forms, models


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """Register basic user profile."""
    print("*** SIGN UP VIEW ***")
    form = forms.AccountCreationForm()
    if request.method == 'POST':
        form = forms.AccountCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "Almost there! Just a few more steps to finish registering."
            )
            return HttpResponseRedirect(reverse('accounts:clickthrough'))
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_up_account(request):
    """Register details of profile."""
    print("*** REGISTER VIEW ***")
    form = forms.AccountExtrasCreationForm()
    if request.method == 'POST':
        print('**** REQ METHOD IS POST ****')
        form = forms.AccountExtrasCreationForm(data=request.POST,
                                               files=request.FILES,
                                               user=request.user)
        if form.is_valid():
            print('**** FORM IS VALID ****')
            form.save()
            print('** CALL "save" ON FORM **')
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            print("**** LOADED SUCCESS MESSAGE ****")
            return HttpResponseRedirect(reverse('home'))
    print('** THIS SHOULD LOAD / RELOAD THE REGISTER VIEW **')
    return render(request, 'accounts/sign_up_account.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


def profile(request, pk):
    account = get_object_or_404(models.Account, pk=pk)
    return render(request, 'accounts/user_profile.html', {
            'account': account,
        })


def profile_bio(request, pk):
    account = get_object_or_404(models.Account, pk=pk)
    return render(request, 'accounts/user_bio.html', {
            'account': account
        })


def clickthrough(request):
    print("**** CLICKTHROUGH VIEW only calls template with a button"
          "for the express purpose of escaping SIGN_UP VIEW ****")
    return render(request, 'accounts/clickthrough.html')


def profile_list(request):
    accounts = models.Account.objects.all()
    return render(request, 'accounts/user_list.html', {'accounts': accounts})


@login_required
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    account = get_object_or_404(models.Account, user=user)
    form = forms.AccountEditForm(instance=user)
    formplus = forms.AccountExtrasEditForm(instance=account)

    if request.method == 'POST':
        print('**** EDIT METHOD IS POST ****')
        form = forms.AccountEditForm(instance=user,
                                     data=request.POST,
                                     files=request.FILES)
        formplus = forms.AccountExtrasEditForm(instance=account,
                                               data=request.POST,
                                               files=request.FILES,
                                               user=request.user)

        if form.is_valid() and formplus.is_valid():
            print('**** BOTH FORMS VALID ****')
            form.save()
            formplus.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             "Updated {}".format(
                                form.cleaned_data['username'])
            )
            print('**** SUCCESS MESSAGE LOADED.  ACCOUNT SHOULD BE SAVED. ****')
            return HttpResponseRedirect(reverse('accounts:list'))
    return render(request, 'accounts/user_form.html',
                  {'form': form,
                   'formplus': formplus,
                   'user': user,
                   'account': account})


@login_required
def pw_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        print("*** REQUEST METHOD IS POST ***")
        form = forms.PasswordEditForm(request.user, request.POST)
        if form.is_valid():
            print("*** VIEW THINKS FORM IS VALID! ***")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        # IDK what this is doing or why it wants the default form?
    return render(request, 'accounts/new_password.html', {
        'form': form
    })
