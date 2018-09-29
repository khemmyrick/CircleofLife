from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts import models


def home(request):
    return render(request, 'home.html')


# def index(request, pk):
#    user = get_object_or_404(models.Account, pk=pk)
#    if user is not None:
#        if user.is_active():
#            return render(request, 'home.html', {'account': account})
#    return render(request, 'home.html')
